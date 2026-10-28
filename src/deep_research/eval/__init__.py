"""Cross-Border E-Commerce AI Agent Evaluation Package."""

from deep_research.eval.golden_dataset import (
    GoldenCase,
    ALL_GOLDEN_CASES,
    get_golden_case,
    CASE_SONY_HEADPHONE,
    CASE_ESPRESSO_MAKER,
    CASE_OFFICE_CHAIR,
)
from deep_research.eval.metrics import (
    MetricResult,
    LLMJudgeResult,
    verify_financial_math,
    verify_fba_classification,
    verify_structural_integrity,
    calculate_voc_recall,
    run_llm_judge,
)
from deep_research.eval.evaluator import (
    CaseEvalResult,
    EvaluationSuiteReport,
    AgentEvaluator,
)

__all__ = [
    "GoldenCase",
    "ALL_GOLDEN_CASES",
    "get_golden_case",
    "CASE_SONY_HEADPHONE",
    "CASE_ESPRESSO_MAKER",
    "CASE_OFFICE_CHAIR",
    "MetricResult",
    "LLMJudgeResult",
    "verify_financial_math",
    "verify_fba_classification",
    "verify_structural_integrity",
    "calculate_voc_recall",
    "run_llm_judge",
    "CaseEvalResult",
    "EvaluationSuiteReport",
    "AgentEvaluator",
]
