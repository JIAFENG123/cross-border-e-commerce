import pytest
from deep_research.graph import build_research_graph


def test_research_graph_execution():
    graph = build_research_graph()

    initial_state = {
        "niche_query": "Portable Camping Espresso Maker",
        "target_market": "US",
        "resolved_product": None,
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

    final_state = graph.invoke(initial_state)

    assert final_state["current_step"] == "completed"
    assert len(final_state["competitors"]) > 0
    assert len(final_state["voc_defects"]) > 0
    assert final_state["financial_model"] is not None
    assert final_state["final_report"] is not None
    assert "报告" in final_state["final_report"] or "Report" in final_state["final_report"]
