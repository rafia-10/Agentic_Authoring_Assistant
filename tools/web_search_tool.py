from duckduckgo_search import DDGS

class WebSearchTool:
    def __init__(self):
        self.ddg = DDGS()

    def search(self, query: str, max_results=5):
        """Return list of search results with title + link."""
        results = self.ddg.text(query, max_results=max_results)
        return [{"title": r["title"], "link": r["href"], "snippet": r["body"]} for r in results]
