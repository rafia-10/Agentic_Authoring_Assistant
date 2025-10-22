# agents/title_agent.py
from tools.nlp_tool import NLPTool
from typing import List

class TitleAgent:
    def __init__(self, nlp_tool: NLPTool):
        self.nlp_tool = nlp_tool
        

    def generate_titles(self, description: str) -> List[str]:
        titles = self.nlp_tool.generate_titles(description)
        return titles
