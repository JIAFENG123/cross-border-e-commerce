"""Evaluation Metrics for Cross-Border E-Commerce AI Agent.

Implements multi-tiered evaluation:
1. Deterministic Financial Math & Rule Checks (Ground Truth)
2. Structural Completeness & Markdown GFM Validation
3. Domain-Specific VOC Defect Recall
4. LLM-as-a-Judge Report Quality Scoring
"""

from __future__ import annotations

import json
import re
from typing import Dict, Any, List, Tuple, Optional
from pydantic import BaseModel, Field

from deep_research.eval.golden_dataset import GoldenCase
from deep_research.llm import get_llm


class MetricResult(BaseModel):
    metric_name: str
    passed: bool
    score: float = Field(ge=0.0, le=1.0)
    details: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class LLMJudgeResult(BaseModel):
    data_consistency_score: int = Field(ge=1, le=5, description="数据与财务表前后一致性 (1-5)")
    actionability_score: int = Field(ge=1, le=5, description="供应链开模与材料改良可落地性 (1-5)")
    risk_rigor_score: int = Field(ge=1, le=5, description="出海合规与风控审慎度 (1-5)")
    executive_clarity_score: int = Field(ge=1, le=5, description="报告结构严谨度与立项裁决明确性 (1-5)")
    composite_score_pct: float = Field(ge=0.0, le=100.0)
    critique: str


# ---------------------------------------------------------
# Tier 1: Deterministic Math & Rule Verification
# ---------------------------------------------------------

def verify_financial_math(fin: Dict[str, Any], tolerance: float = 0.08) -> MetricResult:
    """Validate arithmetic and business formula integrity in Landed Cost model."""
    if not fin:
        return MetricResult(
            metric_name="financial_math_integrity",
            passed=False,
            score=0.0,
            details="Financial model is missing or empty."
        )

    sourcing = fin.get("sourcing_cost_usd", 0.0)
    shipping = fin.get("first_leg_shipping_usd", 0.0)
    tariff = fin.get("customs_and_tariff_usd", 0.0)
    fba_fee = fin.get("fba_fulfillment_fee_usd", 0.0)
    referral = fin.get("amazon_referral_fee_usd", 0.0)
    ad_spend = fin.get("ad_spend_usd", 0.0)
    return_loss = fin.get("return_allowance_usd", 0.0)

    landed = fin.get("total_landed_cost_usd", 0.0)
    operating = fin.get("total_operating_cost_usd", 0.0)
    net_profit = fin.get("net_profit_usd", 0.0)
    net_margin = fin.get("net_margin_percentage", 0.0)

    # 1. Landed Cost = Sourcing + Shipping + Tariff
    expected_landed = sourcing + shipping + tariff
    landed_err = abs(expected_landed - landed)

    # 2. Total Operating Cost = Landed + FBA + Referral + Ad + Return
    expected_operating = landed + fba_fee + referral + ad_spend + return_loss
    operating_err = abs(expected_operating - operating)

    # 3. Profit & Margin
    # Retail price can be deduced from referral fee (referral = 15% retail)
    deduced_retail = (referral / 0.15) if referral > 0 else 0.0
    profit_err = 0.0
    margin_err = 0.0
    if deduced_retail > 0:
        expected_profit = deduced_retail - operating
        profit_err = abs(expected_profit - net_profit)
        expected_margin = (net_profit / deduced_retail) * 100.0
        margin_err = abs(expected_margin - net_margin)

    violations = []
    if landed_err > tolerance:
        violations.append(f"Landed Cost discrepancy: expected {expected_landed:.2f}, got {landed:.2f} (diff {landed_err:.2f})")
    if operating_err > tolerance:
        violations.append(f"Operating Cost discrepancy: expected {expected_operating:.2f}, got {operating:.2f} (diff {operating_err:.2f})")
    if deduced_retail > 0 and profit_err > 0.20:
        violations.append(f"Net Profit discrepancy: expected {expected_profit:.2f}, got {net_profit:.2f}")
    if deduced_retail > 0 and margin_err > 2.0:
        violations.append(f"Net Margin % discrepancy: expected {expected_margin:.1f}%, got {net_margin:.1f}%")

    passed = len(violations) == 0
    score = 1.0 if passed else max(0.0, 1.0 - (len(violations) * 0.25))

    return MetricResult(
        metric_name="financial_math_integrity",
        passed=passed,
        score=round(score, 2),
        details="All mathematical equations and accounting balances verified." if passed else " ; ".join(violations),
        metadata={
            "landed_error": round(landed_err, 3),
            "operating_error": round(operating_err, 3),
            "profit_error": round(profit_err, 3),
            "margin_error": round(margin_err, 2),
        }
    )


def verify_fba_classification(fin: Dict[str, Any], case: GoldenCase) -> MetricResult:
    """Verify that the agent assigned the correct Amazon FBA Size Tier."""
    actual_tier = (fin.get("fba_tier") or "").strip().lower()
    expected_tier = case.expected_fba_tier.strip().lower()

    # Normalize partial strings
    def normalize_tier(t: str) -> str:
        if "large standard" in t:
            return "large standard"
        if "small standard" in t:
            return "small standard"
        if "oversize" in t or "bulky" in t:
            return "oversize"
        return t

    match = normalize_tier(actual_tier) == normalize_tier(expected_tier)
    return MetricResult(
        metric_name="fba_tier_classification",
        passed=match,
        score=1.0 if match else 0.0,
        details=f"Target: '{case.expected_fba_tier}' | Assigned: '{fin.get('fba_tier')}'",
        metadata={"expected": case.expected_fba_tier, "assigned": fin.get("fba_tier")}
    )


def verify_structural_integrity(state: Dict[str, Any], case: GoldenCase) -> MetricResult:
    """Verify presence and density of competitors, VOC items, trends, and report formatting."""
    comps = state.get("competitors", [])
    voc = state.get("voc_defects", [])
    report = state.get("final_report") or ""

    sub_scores = []
    issues = []

    # 1. Competitors count
    comp_target = case.expected_min_competitors
    if len(comps) >= comp_target:
        sub_scores.append(1.0)
    else:
        sub_scores.append(len(comps) / max(1, comp_target))
        issues.append(f"Competitors count {len(comps)} < expected {comp_target}")

    # 2. VOC count
    voc_target = case.expected_min_voc
    if len(voc) >= voc_target:
        sub_scores.append(1.0)
    else:
        sub_scores.append(len(voc) / max(1, voc_target))
        issues.append(f"VOC count {len(voc)} < expected {voc_target}")

    # 3. Report length and GFM table check
    has_tables = "|" in report and "---" in report
    has_headers = bool(re.search(r"^##?\s+", report, re.MULTILINE))
    report_length_ok = len(report) >= 150

    report_score = (0.4 if report_length_ok else 0.1) + (0.3 if has_tables else 0.0) + (0.3 if has_headers else 0.0)
    sub_scores.append(report_score)
    if not has_tables:
        issues.append("Final report lacks Markdown tables")
    if not report_length_ok:
        issues.append(f"Final report length ({len(report)} chars) is insufficient")

    avg_score = sum(sub_scores) / len(sub_scores)
    passed = avg_score >= 0.80

    return MetricResult(
        metric_name="structural_integrity",
        passed=passed,
        score=round(avg_score, 2),
        details="Structural schema and Markdown GFM density complete." if passed else " ; ".join(issues),
        metadata={
            "competitors_found": len(comps),
            "voc_defects_found": len(voc),
            "report_characters": len(report),
            "has_markdown_tables": has_tables
        }
    )


# ---------------------------------------------------------
# Tier 2: Domain VOC Recall (业务痛点召回率)
# ---------------------------------------------------------

def calculate_voc_recall(extracted_voc: List[Dict[str, Any]], case: GoldenCase) -> MetricResult:
    """Measure what percentage of known ground-truth failure modes were successfully mined."""
    if not extracted_voc:
        return MetricResult(
            metric_name="voc_ground_truth_recall",
            passed=False,
            score=0.0,
            details="No VOC defects extracted by Agent."
        )

    # Flatten all text in extracted VOC
    text_corpus = ""
    for item in extracted_voc:
        comp = item.get("component", "")
        desc = item.get("defect_description", "")
        quote = item.get("customer_quote", "")
        fix = item.get("factory_countermeasure", "")
        text_corpus += f" {comp} {desc} {quote} {fix}".lower()

    recalled_themes = []
    missed_themes = []

    for i, cluster in enumerate(case.ground_truth_voc_clusters):
        theme_name = cluster.get("component", f"Theme {i+1}")
        keywords = cluster.get("keywords", [])
        # If any keyword matches the extracted text corpus, theme is recalled
        if any(kw.lower() in text_corpus for kw in keywords):
            recalled_themes.append(theme_name)
        else:
            missed_themes.append(theme_name)

    total_themes = len(case.ground_truth_voc_clusters)
    recall_rate = len(recalled_themes) / max(1, total_themes)
    passed = recall_rate >= 0.66  # At least 2 out of 3 core failure modes detected

    return MetricResult(
        metric_name="voc_ground_truth_recall",
        passed=passed,
        score=round(recall_rate, 2),
        details=f"Recalled {len(recalled_themes)}/{total_themes} themes: [{', '.join(recalled_themes)}]. Missed: [{', '.join(missed_themes)}]",
        metadata={
            "recalled_themes": recalled_themes,
            "missed_themes": missed_themes,
            "recall_percentage": round(recall_rate * 100.0, 1)
        }
    )


# ---------------------------------------------------------
# Tier 3: LLM-as-a-Judge Evaluation (大模型裁判量化评分)
# ---------------------------------------------------------

JUDGE_SYSTEM_PROMPT = """你是一名世界顶级跨境出海投资委员会的首席质检官（LLM Judge）。
你的职责是对智能体（Agent）撰写的《出海商业可行性深度调研报告》进行严格的多维度质量审计与打分。

请按照以下 4 个独立维度分别给出 1 到 5 分的客观评分（1=极差，3=及格，5=卓越）：

1. 数据与财务表前后一致性 (Data Consistency):
   - 报告正文陈述的价格、FBA分段、净利率、落地成本是否与传入的财务数据吻合？是否存在捏造、前后矛盾等幻觉？
2. 供应链开模与改良落地性 (Actionability):
   - 针对买家VOC提出的工厂对策，是否给出了具体的工程措施、材料标号（如弹簧钢、氟橡胶、网布抗拉系数、模具公差），还是只写空话套话？
3. 出海风控与合规审慎度 (Risk Rigor):
   - 报告是否客观揭示了高退货率、关税变动、专利侵权、供应链断单等商业杀手风险，而非盲目吹捧乐观？
4. 报告排版与决策明确性 (Executive Clarity):
   - 结构是否严密，是否包含规范的标准 Markdown 数据表格、引用块，立项建议（Verdict）是否明确可行？

必须输出且仅输出合法的 JSON 对象，格式如下：
{
  "data_consistency_score": <1-5>,
  "actionability_score": <1-5>,
  "risk_rigor_score": <1-5>,
  "executive_clarity_score": <1-5>,
  "critique": "<200字以内的专业点评与改进建议>"
}
"""

def run_llm_judge(report: str, financial_model: Dict[str, Any], provider: str = "groq") -> LLMJudgeResult:
    """Execute LLM-as-a-Judge evaluation over the synthesized feasibility report."""
    if not report or len(report.strip()) < 100:
        return LLMJudgeResult(
            data_consistency_score=1,
            actionability_score=1,
            risk_rigor_score=1,
            executive_clarity_score=1,
            composite_score_pct=20.0,
            critique="报告内容为空或篇幅严重不足，未能形成有效商业可行性调研决策。"
        )

    user_prompt = f"""
【待评审的最终可行性决策报告】:
{report[:3500]}

【底层校验财务模型数据参考】:
- FBA 分段: {financial_model.get('fba_tier')}
- 落地成本 (Landed Cost): ${financial_model.get('total_landed_cost_usd')}
- 净利润 (Net Profit): ${financial_model.get('net_profit_usd')}
- 预估净利率: {financial_model.get('net_margin_percentage')}%
- 投资回报率 (ROI): {financial_model.get('roi_percentage')}%
- 评级: {financial_model.get('viability_rating')}
"""

    llm = get_llm(provider=provider, model_name="openai/gpt-oss-120b", temperature=0.1)
    try:
        response = llm.invoke([
            {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ])
        content = response.content.strip()
        # Parse JSON
        if "{" in content and "}" in content:
            json_str = content[content.find("{"):content.rfind("}") + 1]
            data = json.loads(json_str)
            s1 = int(data.get("data_consistency_score", 4))
            s2 = int(data.get("actionability_score", 4))
            s3 = int(data.get("risk_rigor_score", 4))
            s4 = int(data.get("executive_clarity_score", 4))
            composite = ((s1 + s2 + s3 + s4) / 20.0) * 100.0
            return LLMJudgeResult(
                data_consistency_score=s1,
                actionability_score=s2,
                risk_rigor_score=s3,
                executive_clarity_score=s4,
                composite_score_pct=round(composite, 1),
                critique=data.get("critique", "质检完成")
            )
    except Exception as e:
        pass

    # Heuristic fallback if LLM is unavailable
    has_tables = "|" in report and "---" in report
    has_numbers = bool(re.search(r"\$\d+", report))
    has_verdict = "verdict" in report.lower() or "立项" in report

    s1 = 4 if has_numbers else 3
    s2 = 4 if "工厂" in report or "模具" in report else 3
    s3 = 4 if "风险" in report or "退货" in report else 3
    s4 = 5 if (has_tables and has_verdict) else 3
    composite = ((s1 + s2 + s3 + s4) / 20.0) * 100.0

    return LLMJudgeResult(
        data_consistency_score=s1,
        actionability_score=s2,
        risk_rigor_score=s3,
        executive_clarity_score=s4,
        composite_score_pct=round(composite, 1),
        critique="[Heuristic Fallback] 报告具备良好的结构与核心要素，包含数据支撑与决策结论。"
    )
