# agents/summary_agent.py
from tools.nlp_tool import NLPTool


class SummaryAgent:
    def __init__(self, nlp_tool: NLPTool):
        self.nlp_tool = nlp_tool
        

    def generate_summary(self, description: str) -> str:
        summary = self.nlp_tool.generate_summary(description) 
        return summary
