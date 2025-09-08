# inside reference_agent.py
from tools.web_search_tool import WebSearchTool

class ReferenceAgent:
    def __init__(self):
        self.web_tool = WebSearchTool()

    def fetch_references(self, description: str, min_results=3):
        arxiv_refs = self.query_arxiv(description)

        if len(arxiv_refs) < min_results:
            web_refs = self.web_tool.search(description, max_results=5)
            return arxiv_refs + web_refs
        return arxiv_refs