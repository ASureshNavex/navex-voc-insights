"""load_batch -> score -> summarise -> publish. Fixed order; the model never chooses a step."""

from typing import Any, cast

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from account_scoring_agent.graphs.account_scoring.edges import after_load
from account_scoring_agent.graphs.account_scoring.nodes import Dependencies, Nodes
from account_scoring_agent.graphs.account_scoring.state import ScoringState

RECURSION_LIMIT = 10

type ScoringGraph = CompiledStateGraph[ScoringState, Any, ScoringState, ScoringState]


def build_graph(deps: Dependencies) -> ScoringGraph:
    nodes = Nodes(deps)
    graph = StateGraph(ScoringState)
    graph.add_node("load_batch", nodes.load_batch)
    graph.add_node("fail_empty", nodes.fail_empty)
    graph.add_node("score", nodes.score)
    graph.add_node("summarise", nodes.summarise)
    graph.add_node("publish", nodes.publish)

    graph.add_edge(START, "load_batch")
    graph.add_conditional_edges("load_batch", after_load)
    graph.add_edge("score", "summarise")
    graph.add_edge("summarise", "publish")
    graph.add_edge("publish", END)
    graph.add_edge("fail_empty", END)
    return graph.compile()


async def run_scoring(deps: Dependencies, run_id: str) -> ScoringState:
    graph = build_graph(deps)
    try:
        result = await graph.ainvoke({"run_id": run_id}, {"recursion_limit": RECURSION_LIMIT})
        return cast(ScoringState, result)
    except Exception as exc:
        # The previously published run stays in place.
        await deps.store.fail_run(run_id, f"Scoring failed: {type(exc).__name__}")
        raise
