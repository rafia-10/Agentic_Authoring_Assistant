import os
from tavily import TavilyClient

class WebSearchTool:
    def __init__(self):
        self.tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    def search(self, query, max_results=5):
        res = self.tavily.search(query=query, max_results=max_results)
        return [{"title": r.get("title",""), "url": r.get("url","")} for r in res.get("results", [])]

    
    def search_and_rank(self, query, max_results=5):
        return self.search(query, max_results)
