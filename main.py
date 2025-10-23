# main.py
from langgraph.graph import StateGraph
from agents.metadata_agent.metadata_agent_langgraph import generate_metadata
from agents.refiner_agent.refiner_agent_langgraph import build_refiner_graph
from agents.reference_agent.reference_agent import ReferenceAgent
from tools.web_search_tool import WebSearchTool
from typing import Dict

# ------------------ Initialize tools & agents ------------------
web_tool = WebSearchTool()
reference_agent = ReferenceAgent(web_tool)
refiner_graph = build_refiner_graph()

# ------------------ Node functions ------------------
def metadata_node(state: Dict):
    """Generate raw metadata."""
    state["raw_metadata"] = generate_metadata(state["description"])
    return state

def refiner_node(state: Dict):
    """Refine metadata using the refiner graph."""
    state["metadata"] = refiner_graph.invoke(state["raw_metadata"])
    return state

def reference_node(state: Dict):
    """Fetch references for the description."""
    state["references"] = reference_agent.fetch_references(state["description"], max_results=5)
    return state

# ------------------ Build LangGraph workflow ------------------
def build_main_graph():
    graph = StateGraph(dict)

    # Add nodes
    graph.add_node("metadata", metadata_node)
    graph.add_node("refiner", refiner_node)
    graph.add_node("references", reference_node)

    # Define execution flow
    graph.set_entry_point("metadata")
    graph.add_edge("metadata", "refiner")
    graph.add_edge("refiner", "references")

    return graph.compile()

# ------------------ Entry point ------------------
def run_all_agents(description: str):
    main_graph = build_main_graph()
    initial_state = {"description": description}
    final_state = main_graph.invoke(initial_state)
    return final_state

# ------------------ Run script ------------------
if __name__ == "__main__":
    description = input("Enter your project description: ")
    result = run_all_agents(description)

    print("\n🎯 Final Orchestrated Output:\n")
    print("📘 Metadata Titles:", result["metadata"]["titles"])
    print("📝 Summary:", result["metadata"]["summary"])
    print("🏷️ Tags:", result["metadata"]["tags"])

    print("\n🔗 References:")
    for ref in result["references"]:
        print(f"- {ref['title']}: {ref['url']}")
