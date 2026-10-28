"""Evaluator Engine for Cross-Border E-Commerce AI Agent.

Executes deterministic tests, VOC recall benchmark, and LLM-as-a-judge scoring
against either cached states or live LangGraph executions.
"""

from __future__ import annotations

import os
import json
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from deep_research.eval.golden_dataset import GoldenCase, ALL_GOLDEN_CASES, get_golden_case
from deep_research.eval.metrics import (
    MetricResult,
    LLMJudgeResult,
    verify_financial_math,
    verify_fba_classification,
    verify_structural_integrity,
    calculate_voc_recall,
    run_llm_judge,
)


class CaseEvalResult(BaseModel):
    case_id: str
    case_name: str
    query: str
    mode: str  # "state" or "live"
    passed: bool
    overall_score: float = Field(ge=0.0, le=100.0)
    latency_seconds: float = 0.0

    # Detailed metrics
    math_metric: MetricResult
    fba_metric: MetricResult
    structure_metric: MetricResult
    voc_metric: MetricResult
    judge_result: Optional[LLMJudgeResult] = None

    # Diagnostic metadata
    diagnostic_summary: str = ""


class EvaluationSuiteReport(BaseModel):
    timestamp: str
    mode: str
    total_cases: int
    passed_cases: int
    pass_rate_pct: float
    avg_overall_score: float
    math_integrity_rate_pct: float
    fba_accuracy_rate_pct: float
    avg_voc_recall_pct: float
    avg_judge_score_pct: float
    avg_latency_seconds: float
    results: List[CaseEvalResult]


class AgentEvaluator:
    """Core evaluation engine for evaluating agent outputs and regression benchmarks."""

    def __init__(self, run_judge: bool = True, provider: str = "groq"):
        self.run_judge = run_judge
        self.provider = provider

    def evaluate_state(self, case: GoldenCase, state: Dict[str, Any], latency: float = 0.0, mode: str = "state") -> CaseEvalResult:
        """Evaluate an existing or pre-cached ResearchState against ground truth."""
        fin = state.get("financial_model") or {}
        report = state.get("final_report") or ""

        # 1. Deterministic Math & Classification
        math_res = verify_financial_math(fin)
        fba_res = verify_fba_classification(fin, case)
        structure_res = verify_structural_integrity(state, case)

        # 2. VOC Recall Benchmark
        voc_res = calculate_voc_recall(state.get("voc_defects", []), case)

        # 3. LLM-as-a-Judge
        judge_res = None
        if self.run_judge:
            judge_res = run_llm_judge(report, fin, provider=self.provider)

        # 4. Compute Weighted Overall Score (0 - 100)
        # Weights: Math (25%), FBA (20%), VOC Recall (25%), Structure (10%), Judge (20%)
        if judge_res:
            score = (
                (math_res.score * 25.0) +
                (fba_res.score * 20.0) +
                (voc_res.score * 25.0) +
                (structure_res.score * 10.0) +
                ((judge_res.composite_score_pct / 100.0) * 20.0)
            )
        else:
            # Rebalance without judge: Math (35%), FBA (25%), VOC Recall (30%), Structure (10%)
            score = (
                (math_res.score * 35.0) +
                (fba_res.score * 25.0) +
                (voc_res.score * 30.0) +
                (structure_res.score * 10.0)
            )

        # A case passes if overall score >= 75.0, math is strictly valid, and FBA tier matches
        passed = (score >= 75.0) and math_res.passed and fba_res.passed

        summary = f"[{'PASS' if passed else 'FAIL'}] Score: {score:.1f}/100 | Math: {'OK' if math_res.passed else 'ERR'} | FBA Tier: {'OK' if fba_res.passed else 'MISMATCH'} | VOC Recall: {voc_res.score*100:.1f}%"
        if judge_res:
            summary += f" | Judge: {judge_res.composite_score_pct:.1f}%"

        return CaseEvalResult(
            case_id=case.case_id,
            case_name=case.name,
            query=case.query,
            mode=mode,
            passed=passed,
            overall_score=round(score, 1),
            latency_seconds=round(latency, 2),
            math_metric=math_res,
            fba_metric=fba_res,
            structure_metric=structure_res,
            voc_metric=voc_res,
            judge_result=judge_res,
            diagnostic_summary=summary
        )

    def evaluate_live(self, case: GoldenCase) -> CaseEvalResult:
        """Run the real LangGraph workflow end-to-end and evaluate the live execution output."""
        from deep_research.graph import build_research_graph

        initial_state = {
            "niche_query": case.query,
            "target_market": case.market,
            "resolved_product": None,
            "llm_provider": self.provider,
            "llm_model": "openai/gpt-oss-120b",
            "max_iterations": 1,
            "iteration_count": 0,
            "competitors": [],
            "voc_defects": [],
            "market_trends": [],
            "critic_notes": [],
            "is_sufficient": False,
            "plan_overview": "",
            "subtasks": [],
            "current_step": "init",
            "financial_model": None,
            "final_report": None,
        }

        graph = build_research_graph()
        t0 = time.time()
        final_state = graph.invoke(initial_state)
        latency = time.time() - t0

        return self.evaluate_state(case, final_state, latency=latency, mode="live")

    def run_suite(
        self,
        cases: Optional[List[GoldenCase]] = None,
        mode: str = "state",
        save_report: bool = True,
        output_dir: str = "artifacts/eval"
    ) -> EvaluationSuiteReport:
        """Execute full benchmark suite across all golden cases and compute macro metrics."""
        target_cases = cases or ALL_GOLDEN_CASES
        results: List[CaseEvalResult] = []

        for case in target_cases:
            if mode == "live":
                res = self.evaluate_live(case)
            else:
                # Use cached representative sample state
                res = self.evaluate_state(case, case.sample_state, latency=0.05, mode="state")
            results.append(res)

        total = len(results)
        passed = sum(1 for r in results if r.passed)
        pass_rate = (passed / max(1, total)) * 100.0
        avg_score = sum(r.overall_score for r in results) / max(1, total)
        math_ok_rate = (sum(1 for r in results if r.math_metric.passed) / max(1, total)) * 100.0
        fba_ok_rate = (sum(1 for r in results if r.fba_metric.passed) / max(1, total)) * 100.0
        avg_voc_recall = (sum(r.voc_metric.score for r in results) / max(1, total)) * 100.0
        
        judge_scores = [r.judge_result.composite_score_pct for r in results if r.judge_result]
        avg_judge = (sum(judge_scores) / len(judge_scores)) if judge_scores else 0.0
        avg_latency = sum(r.latency_seconds for r in results) / max(1, total)

        suite_report = EvaluationSuiteReport(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            mode=mode,
            total_cases=total,
            passed_cases=passed,
            pass_rate_pct=round(pass_rate, 1),
            avg_overall_score=round(avg_score, 1),
            math_integrity_rate_pct=round(math_ok_rate, 1),
            fba_accuracy_rate_pct=round(fba_ok_rate, 1),
            avg_voc_recall_pct=round(avg_voc_recall, 1),
            avg_judge_score_pct=round(avg_judge, 1),
            avg_latency_seconds=round(avg_latency, 2),
            results=results
        )

        if save_report:
            os.makedirs(output_dir, exist_ok=True)
            ts_slug = datetime.now().strftime("%Y%m%d_%H%M%S")
            json_path = os.path.join(output_dir, f"eval_report_{ts_slug}.json")
            md_path = os.path.join(output_dir, f"eval_summary_{ts_slug}.md")

            with open(json_path, "w", encoding="utf-8") as f:
                f.write(suite_report.model_dump_json(indent=2))

            with open(md_path, "w", encoding="utf-8") as f:
                f.write(self.generate_markdown_summary(suite_report))

        return suite_report

    @staticmethod
    def generate_markdown_summary(report: EvaluationSuiteReport) -> str:
        """Render evaluation suite results into an executive Markdown report."""
        lines = [
            f"# 跨境电商 AI Agent 系统化评测报告 (Evaluation Pipeline)",
            f"\n- **执行时间**: `{report.timestamp}`",
            f"- **评测模式**: `{report.mode}` (Ground-Truth Golden Benchmark)",
            f"- **总测试案例数**: `{report.total_cases}`",
            f"- **综合通过率 (Pass Rate)**: **{report.pass_rate_pct}%** ({report.passed_cases}/{report.total_cases})",
            f"- **综合加权得分**: **{report.avg_overall_score} / 100**",
            f"\n## 一、 核心层级指标汇总 (Metric Cards)",
            f"\n| 评测维度 | 指标类型 | 达成率 / 平均分 | 工业标准红线 | 判定 |",
            f"|:---|:---|:---|:---|:---:|",
            f"| **财务公式与数学闭环率** | 确定性规则 | **{report.math_integrity_rate_pct}%** | 100% | {'✅ 达标' if report.math_integrity_rate_pct == 100.0 else '❌ 报警'} |",
            f"| **FBA 尺寸分段精准度** | 确定性分类 | **{report.fba_accuracy_rate_pct}%** | ≥ 95% | {'✅ 达标' if report.fba_accuracy_rate_pct >= 95.0 else '❌ 偏离'} |",
            f"| **买家真实痛点 (VOC) 召回率** | 领域基准对齐 | **{report.avg_voc_recall_pct}%** | ≥ 75% | {'✅ 达标' if report.avg_voc_recall_pct >= 75.0 else '⚠️ 需关注'} |",
            f"| **LLM-as-a-Judge 研报评分** | 主观语义评审 | **{report.avg_judge_score_pct} / 100** | ≥ 80 | {'✅ 优秀' if report.avg_judge_score_pct >= 80.0 else '⚠️ 及格'} |",
            f"| **单用例端到端耗时** | 基础设施性能 | **{report.avg_latency_seconds}s** | ≤ 25s | {'⚡ 极佳' if report.avg_latency_seconds <= 25.0 else '⚠️ 偏慢'} |",
            f"\n## 二、 分案例详细评审矩阵 (Case Matrix)",
            f"\n| 案例 ID | 产品品类 | 模式 | 综合得分 | 财务平衡 | FBA 分段 | VOC 召回 | 裁决 |",
            f"|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|",
        ]

        for r in report.results:
            status_badge = "✅ PASS" if r.passed else "❌ FAIL"
            math_badge = "✓ 严格平衡" if r.math_metric.passed else "✕ 偏差"
            fba_badge = f"✓ {r.fba_metric.metadata.get('assigned', 'OK')}" if r.fba_metric.passed else f"✕ {r.fba_metric.metadata.get('assigned')}"
            voc_badge = f"{r.voc_metric.score * 100:.0f}%"

            lines.append(
                f"| `{r.case_id}` | {r.case_name} | `{r.mode}` | **{r.overall_score}** | {math_badge} | {fba_badge} | {voc_badge} | {status_badge} |"
            )

        lines.append("\n## 三、 质检官深度评审点评 (Judge Critiques)")
        for r in report.results:
            if r.judge_result:
                lines.append(f"\n### 📌 案例: {r.case_name}")
                lines.append(f"- **一致性得分**: {r.judge_result.data_consistency_score}/5 | **工程可落地性**: {r.judge_result.actionability_score}/5 | **风控审慎度**: {r.judge_result.risk_rigor_score}/5 | **结构清晰度**: {r.judge_result.executive_clarity_score}/5")
                lines.append(f"- **质检官裁决意见**: {r.judge_result.critique}")

        return "\n".join(lines)
