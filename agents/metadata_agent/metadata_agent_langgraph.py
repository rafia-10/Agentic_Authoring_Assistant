from langgraph import graph
from .title_agent import TitleAgent
from .summary_agent import SummaryAgent
from .tag_agent import TagAgent
from tools.nlp_tool import NLPTool
from tools.refiner_tool import RefinerTool
from pydantic import BaseModel
from typing import List, Dict
import os

# Metadata model
class Metadata(BaseModel):
    titles: List[str]
    summary: str
    tags: List[str]


# Initialize tools
api_key = os.getenv("OPENROUTER_API_KEY")
nlp_tool = NLPTool(api_key=api_key)
refiner = RefinerTool()

# Initialize agents
title_agent = TitleAgent(nlp_tool, refiner)
summary_agent = SummaryAgent(nlp_tool, refiner)
tag_agent = TagAgent(nlp_tool, refiner)

# Modern LangGraph function-based graph
@graph
def metadata_graph(state: Dict) -> Dict:
    state["titles"] = title_agent.generate_titles(state["description"])
    state["summary"] = summary_agent.generate_summary(state["description"])
    state["tags"] = tag_agent.extract_tags(state["description"], state["summary"])

    try:
        metadata = Metadata(
            titles=state["titles"],
            summary=state["summary"],
            tags=state["tags"]
        )
        state["metadata"] = metadata.dict()
    except Exception as e:
        state["metadata"] = {
            "titles": state["titles"],
            "summary": state["summary"],
            "tags": state["tags"],
            "validation_error": str(e)
        }

    return state

# Entry point function
def generate_metadata(description: str) -> Dict:
    initial_state = {
        "description": description,
        "titles": [],
        "summary": "",
        "tags": []
    }
    final_state = metadata_graph(initial_state)
    return final_state.get("metadata", {})
