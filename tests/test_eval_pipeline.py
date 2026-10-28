"""Pytest automated test suite for Cross-Border E-Commerce AI Agent Eval Pipeline."""

import pytest
from deep_research.eval.golden_dataset import ALL_GOLDEN_CASES, CASE_SONY_HEADPHONE, CASE_ESPRESSO_MAKER, CASE_OFFICE_CHAIR
from deep_research.eval.metrics import (
    verify_financial_math,
    verify_fba_classification,
    verify_structural_integrity,
    calculate_voc_recall,
)
from deep_research.eval.evaluator import AgentEvaluator


def test_golden_dataset_structure():
    assert len(ALL_GOLDEN_CASES) == 3
    for case in ALL_GOLDEN_CASES:
        assert case.case_id
        assert case.name
        assert case.ground_truth_weight_lbs > 0
        assert len(case.ground_truth_dimensions_inches) == 3
        assert len(case.ground_truth_voc_clusters) >= 3
        assert case.expected_fba_tier in ["Large Standard", "Small Standard", "Small Oversize / Bulky"]
        assert case.sample_state, f"Case {case.case_id} must have a valid sample_state"


def test_financial_math_accuracy_pass():
    sample_fin = CASE_SONY_HEADPHONE.sample_state["financial_model"]
    result = verify_financial_math(sample_fin)
    assert result.passed, f"Valid financial model failed check: {result.details}"
    assert result.score == 1.0


def test_financial_math_accuracy_detects_tampering():
    tampered_fin = dict(CASE_SONY_HEADPHONE.sample_state["financial_model"])
    # Artificially alter total landed cost so Sourcing + Freight + Tariff != Landed Cost
    tampered_fin["total_landed_cost_usd"] = 99.99
    result = verify_financial_math(tampered_fin)
    assert not result.passed, "Math checker failed to detect altered landed cost!"
    assert "Landed Cost discrepancy" in result.details


def test_fba_classification_metric():
    headphone_fin = CASE_SONY_HEADPHONE.sample_state["financial_model"]
    res1 = verify_fba_classification(headphone_fin, CASE_SONY_HEADPHONE)
    assert res1.passed
    assert res1.score == 1.0

    chair_fin = CASE_OFFICE_CHAIR.sample_state["financial_model"]
    res2 = verify_fba_classification(chair_fin, CASE_OFFICE_CHAIR)
    assert res2.passed
    assert res2.score == 1.0


def test_voc_recall_benchmark():
    headphone_voc = CASE_SONY_HEADPHONE.sample_state["voc_defects"]
    res = calculate_voc_recall(headphone_voc, CASE_SONY_HEADPHONE)
    assert res.passed
    assert res.score == 1.0  # Recalled all 3: Hinge snap, Mic wind noise, Earpad sweat
    assert len(res.metadata["recalled_themes"]) == 3


def test_structural_integrity_metric():
    state = CASE_SONY_HEADPHONE.sample_state
    res = verify_structural_integrity(state, CASE_SONY_HEADPHONE)
    assert res.passed
    assert res.score >= 0.8


def test_full_eval_suite_deterministic_pass():
    """Verify that full benchmark suite runs across all 3 golden cases with 100% pass rate."""
    evaluator = AgentEvaluator(run_judge=False)
    report = evaluator.run_suite(cases=ALL_GOLDEN_CASES, mode="state", save_report=False)

    assert report.total_cases == 3
    assert report.passed_cases == 3
    assert report.pass_rate_pct == 100.0
    assert report.math_integrity_rate_pct == 100.0
    assert report.fba_accuracy_rate_pct == 100.0
    assert report.avg_voc_recall_pct >= 85.0
    assert report.avg_overall_score >= 85.0
