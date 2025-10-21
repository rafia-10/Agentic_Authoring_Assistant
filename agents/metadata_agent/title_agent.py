# agents/title_agent.py
from tools.nlp_tool import NLPTool
from tools.refiner_tool import RefinerTool
from typing import List

class TitleAgent:
    def __init__(self, nlp_tool: NLPTool, refiner: RefinerTool):
        self.nlp_tool = nlp_tool
        self.refiner = refiner

    def generate_titles(self, description: str) -> List[str]:
        titles = self.nlp_tool.generate_titles(description)
        return self.refiner.refine_titles(titles)
