# agents/summary_agent.py
from tools.nlp_tool import NLPTool
from tools.refiner_tool import RefinerTool

class SummaryAgent:
    def __init__(self, nlp_tool: NLPTool, refiner: RefinerTool):
        self.nlp_tool = nlp_tool
        self.refiner = refiner

    def generate_summary(self, description: str) -> str:
        summary = self.nlp_tool.generate_summary(description)
        return self.refiner.refine_summary(summary)
