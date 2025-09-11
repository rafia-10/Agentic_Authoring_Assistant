from langgraph.graph import StateGraph, END
from agents.metadata_agent.metadata_agent import MetadataAgent
from agents.reference_agent.reference_agent import ReferenceAgent
from agents.image_agent.image_agent import ImageAgent
from agents.refiner_agent.refiner_agent import RefinerAgent


# ----------------- State Definition -----------------
class ProjectState(dict):
    """Shared state passed between nodes."""
    description: str
    repo: str
    dataset: str
    results: str
    metadata: dict
    references: list
    images: list
    final_outputs: dict


# ----------------- Initialize Agents -----------------
metadata_agent = MetadataAgent()
reference_agent = ReferenceAgent()
image_agent = ImageAgent()
refiner_agent = RefinerAgent()


# ----------------- Node Functions -----------------
def generate_metadata(state: ProjectState):
    state["metadata"] = metadata_agent.generate_metadata(state["description"])
    return state

def find_references(state: ProjectState):
    state["references"] = reference_agent.find_references(state["description"])
    return state

def generate_image(state: ProjectState):
    state["images"] = image_agent.generate_image(state["description"])
    return state

def refine_outputs(state: ProjectState):
    raw_outputs = {
        **state.get("metadata", {}),
        "references": state.get("references", []),
        "images": state.get("images", []),
    }
    state["final_outputs"] = refiner_agent.refine(raw_outputs)
    return state


# ----------------- Graph Construction -----------------
def build_graph():
    graph = StateGraph(ProjectState)

    # Add nodes
    graph.add_node("metadata", generate_metadata)
    graph.add_node("references", find_references)
    graph.add_node("images", generate_image)
    graph.add_node("refine", refine_outputs)

    # Orchestration
    graph.set_entry_point("metadata")
    graph.add_edge("metadata", "references")
    graph.add_edge("references", "images")
    graph.add_edge("images", "refine")
    graph.add_edge("refine", END)

    return graph.compile()


# ----------------- Run -----------------
def main():
    description = input("Enter your project description: ").strip()
    repo = input("Enter repository link (optional): ").strip()
    dataset = input("Enter dataset info (optional): ").strip()
    results = input("Enter experiment results (optional): ").strip()

    initial_state = ProjectState(
        description=description,
        repo=repo,
        dataset=dataset,
        results=results
    )

    app = build_graph()
    final_state = app.invoke(initial_state)

    print("\n✅ Final Project Metadata:")
    for key, value in final_state["final_outputs"].items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
