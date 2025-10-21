# agents/tag_agent.py
from tools.nlp_tool import NLPTool
from tools.refiner_tool import RefinerTool
from typing import List

class TagAgent:
    def __init__(self, nlp_tool: NLPTool, refiner: RefinerTool):
        self.nlp_tool = nlp_tool
        self.refiner = refiner

    def extract_tags(self, description: str, summary: str) -> List[str]:
        tags = self.nlp_tool.extract_tags(description, summary)
        return self.refiner.refine_tags(tags)
