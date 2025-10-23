from tools.web_search_tool import WebSearchTool
from typing import List, Dict

class ReferenceAgent:
    def __init__(self, web_search_tool: WebSearchTool):
        self.web_search_tool = web_search_tool

    def fetch_references(self, topic: str, max_results: int = 5) -> List[Dict]:
        """Search the web and return ranked, summarized references."""
        print(f"🔎 Searching references for: {topic}")
        results = self.web_search_tool.search_and_rank(topic, max_results)
        references = [
            {
                "title": r.get("title"),
                "url": r.get("url"),
  
            }
            for r in results
        ]
        return references
