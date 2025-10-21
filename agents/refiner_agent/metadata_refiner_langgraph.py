# agents/metadata_refiner_langgraph.py
from langgraph.graph import StateGraph
from ..metadata_agent.metadata_agent_langgraph import generate_metadata
from .refiner_agent import RefinerAgent
from tools.refiner_tool import RefinerTool
from typing import Dict

# Initialize Refiner
refiner_tool = RefinerTool()
refiner_agent = RefinerAgent(refiner_tool)

# Modern function-based LangGraph
@StateGraph
def metadata_refiner_graph(state: Dict) -> Dict:
    # Step 1: generate metadata
    raw_metadata = generate_metadata(state["description"])
    state.update(raw_metadata)  # adds titles, summary, tags

    # Step 2: refine metadata
    refined = refiner_agent.refine_metadata(raw_metadata)
    state["titles_refined"] = refined["titles"]
    state["summary_refined"] = refined["summary"]
    state["tags_refined"] = refined["tags"]

    return state

# Entry point function
def generate_refined_metadata(description: str) -> Dict:
    initial_state = {"description": description}
    final_state = metadata_refiner_graph(initial_state)
    return {
        "titles": final_state.get("titles_refined", []),
        "summary": final_state.get("summary_refined", ""),
        "tags": final_state.get("tags_refined", [])
    }
