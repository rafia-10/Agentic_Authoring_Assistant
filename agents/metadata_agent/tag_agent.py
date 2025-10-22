# agents/tag_agent.py
from tools.nlp_tool import NLPTool
from typing import List

class TagAgent:
    def __init__(self, nlp_tool: NLPTool):
        self.nlp_tool = nlp_tool
        

    def extract_tags(self, description: str, summary: str) -> List[str]:
        tags = self.nlp_tool.extract_tags(description, summary)
        return tags
