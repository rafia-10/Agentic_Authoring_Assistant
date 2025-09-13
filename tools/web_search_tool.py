from tavily import TavilyClient

class WebSearchTool:
    def __init__(self, api_key: str):
        self.client = TavilyClient(api_key=api_key)

    def search(self, query: str, max_results: int = 5):
        """Return list of search results with title + link + snippet/content."""
        # using Tavily search
        resp = self.client.search(query=query, max_results=max_results)
        # resp structure depends on API, but from docs it includes 'results'
        results = resp.get("results", [])  # or however Tavily returns
        output = []
        for r in results:
            item = {
                "title": r.get("title"),
                "link": r.get("url") or r.get("link"),
                "snippet": r.get("content") or r.get("snippet") or r.get("preview")
            }
            output.append(item)
        return output
