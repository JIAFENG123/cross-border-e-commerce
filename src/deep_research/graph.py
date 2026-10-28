from __future__ import annotations

from typing import Literal
from langgraph.graph import StateGraph, START, END

from deep_research.state import ResearchState
from deep_research.nodes.planner import planner_node
from deep_research.nodes.researcher import researcher_node
from deep_research.nodes.critic import critic_node
from deep_research.nodes.synthesizer import synthesizer_node


def should_continue(state: ResearchState) -> Literal["synthesizer", "researcher"]:
    """Conditional router based on Critic judgment."""
    if state.get("is_sufficient", True):
        return "synthesizer"
    return "researcher"


def build_research_graph() -> StateGraph:
    """Build and compile the Cross-Border Deep Research LangGraph StateMachine."""
    workflow = StateGraph(ResearchState)

    # 1. Add Nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("critic", critic_node)
    workflow.add_node("synthesizer", synthesizer_node)

    # 2. Add Edges
    workflow.add_edge(START, "planner")
    workflow.add_edge("planner", "researcher")
    workflow.add_edge("researcher", "critic")

    # 3. Conditional Reflection Edge
    workflow.add_conditional_edges(
        "critic",
        should_continue,
        {
            "synthesizer": "synthesizer",
            "researcher": "researcher"
        }
    )

    workflow.add_edge("synthesizer", END)

    return workflow.compile()
