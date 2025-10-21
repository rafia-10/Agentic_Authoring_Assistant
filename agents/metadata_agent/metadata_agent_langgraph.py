from langgraph.graph import StateGraph
from .title_agent import TitleAgent
from .summary_agent import SummaryAgent
from .tag_agent import TagAgent
from tools.nlp_tool import NLPTool
from tools.refiner_tool import RefinerTool
from pydantic import BaseModel
from typing import List, Dict
import os


# ✅ Metadata schema
class Metadata(BaseModel):
    titles: List[str]
    summary: str
    tags: List[str]


# ✅ Initialize tools and agents
api_key = os.getenv("OPENROUTER_API_KEY")
nlp_tool = NLPTool(api_key=api_key)
refiner = RefinerTool()

title_agent = TitleAgent(nlp_tool, refiner)
summary_agent = SummaryAgent(nlp_tool, refiner)
tag_agent = TagAgent(nlp_tool, refiner)


# Define node functions
def title_node(state: Dict):
    state["titles"] = title_agent.generate_titles(state["description"])
    return state


def summary_node(state: Dict):
    state["summary"] = summary_agent.generate_summary(state["description"])
    return state


def tag_node(state: Dict):
    state["tags"] = tag_agent.extract_tags(state["description"], state["summary"])
    return state


def aggregator_node(state: Dict):
    try:
        metadata = Metadata(
            titles=state["titles"],
            summary=state["summary"],
            tags=state["tags"]
        )
        state["metadata"] = metadata.dict()
    except Exception as e:
        state["metadata"] = {
            "titles": state.get("titles", []),
            "summary": state.get("summary", ""),
            "tags": state.get("tags", []),
            "validation_error": str(e)
        }
    return state


# ✅ Build the LangGraph workflow
def build_metadata_graph():
    graph = StateGraph(dict)

    graph.add_node("title", title_node)
    graph.add_node("summary", summary_node)
    graph.add_node("tags", tag_node)
    graph.add_node("aggregator", aggregator_node)

    # Define the execution flow
    graph.set_entry_point("title")
    graph.add_edge("title", "summary")
    graph.add_edge("summary", "tags")
    graph.add_edge("tags", "aggregator")

    return graph.compile()


# ✅ Entry point function
def generate_metadata(description: str) -> Dict:
    app = build_metadata_graph()
    initial_state = {
        "description": description,
        "titles": [],
        "summary": "",
        "tags": []
    }
    final_state = app.invoke(initial_state)
    return final_state.get("metadata", {})

