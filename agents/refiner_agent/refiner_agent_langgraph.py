# agents/refiner_agent/refiner_agent_langgraph.py
from langgraph.graph import StateGraph
from ..metadata_agent.metadata_agent_langgraph import generate_metadata  # original metadata generator
from tools.refiner_tool import RefinerTool
from typing import Dict

# ------------------ Initialize refiner ------------------
refiner = RefinerTool()

# ------------------ Node functions ------------------
def refine_titles_node(state: Dict):
    if "titles" in state:
        state["titles"] = refiner.refine_titles(state["titles"])
    return state

def refine_summary_node(state: Dict):
    if "summary" in state:
        state["summary"] = refiner.refine_summary(state["summary"])
    return state

def refine_tags_node(state: Dict):
    if "tags" in state:
        state["tags"] = refiner.refine_tags(state["tags"])
    return state

def aggregator_node(state: Dict):
    # Just passes metadata along (already refined)
    state["metadata"] = {
        "titles": state.get("titles", []),
        "summary": state.get("summary", ""),
        "tags": state.get("tags", [])
    }
    return state

# ------------------ Build the StateGraph ------------------
def build_refiner_graph():
    graph = StateGraph(dict)

    # Add nodes
    graph.add_node("refine_titles", refine_titles_node)
    graph.add_node("refine_summary", refine_summary_node)
    graph.add_node("refine_tags", refine_tags_node)
    graph.add_node("aggregator", aggregator_node)

    # Define flow
    graph.set_entry_point("refine_titles")
    graph.add_edge("refine_titles", "refine_summary")
    graph.add_edge("refine_summary", "refine_tags")
    graph.add_edge("refine_tags", "aggregator")

    return graph.compile()

# ------------------ Entry point function ------------------
def generate_refined_metadata(description: str) -> Dict:
    # First generate raw metadata
    raw_metadata = generate_metadata(description)

    app = build_refiner_graph()
    final_state = app.invoke(raw_metadata)
    return final_state.get("metadata", {})
