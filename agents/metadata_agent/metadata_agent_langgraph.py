from langgraph import Node, Graph
from agents.title_agent import TitleAgent
from agents.summary_agent import SummaryAgent
from agents.tag_agent import TagAgent
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

# LangGraph nodes
class TitleNode(Node):
    def run(self, description: str):
        return title_agent.generate_titles(description)

class SummaryNode(Node):
    def run(self, description: str):
        return summary_agent.generate_summary(description)

class TagNode(Node):
    def run(self, description: str, summary: str):
        return tag_agent.extract_tags(description, summary)

class MetadataAggregatorNode(Node):
    def run(self, titles, summary, tags):
        try:
            metadata = Metadata(titles=titles, summary=summary, tags=tags)
            return metadata.dict()
        except Exception as e:
            return {"titles": titles, "summary": summary, "tags": tags, "validation_error": str(e)}

# Build Graph
graph = Graph()
title_node = TitleNode()
summary_node = SummaryNode()
tag_node = TagNode()
aggregator_node = MetadataAggregatorNode()

graph.add_nodes([title_node, summary_node, tag_node, aggregator_node])
graph.connect(title_node, aggregator_node)
graph.connect(summary_node, aggregator_node)
graph.connect(tag_node, aggregator_node)

# Entry point
def generate_metadata(description: str) -> Dict:
    outputs = graph.run({"description": description})
    return outputs.get(aggregator_node, {})
