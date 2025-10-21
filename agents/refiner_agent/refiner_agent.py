# agents/refiner_agent.py
from tools.refiner_tool import RefinerTool
from typing import List, Dict

class RefinerAgent:
    def __init__(self, refiner_tool: RefinerTool):
        self.refiner_tool = refiner_tool

    def refine_titles(self, titles: List[str]) -> List[str]:
        return self.refiner_tool.refine_titles(titles)

    def refine_summary(self, summary: str) -> str:
        return self.refiner_tool.refine_summary(summary)

    def refine_tags(self, tags: List[str]) -> List[str]:
        return self.refiner_tool.refine_tags(tags)

    def refine_metadata(self, metadata: Dict) -> Dict:
        return {
            "titles": self.refine_titles(metadata.get("titles", [])),
            "summary": self.refine_summary(metadata.get("summary", "")),
            "tags": self.refine_tags(metadata.get("tags", []))
        }
