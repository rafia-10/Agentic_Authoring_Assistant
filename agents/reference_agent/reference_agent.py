import arxiv
from tools.web_search_tool import WebSearchTool

class ReferenceAgent:
    def __init__(self):
        self.web_tool = WebSearchTool()

        
    def query_arxiv(self, description: str, max_results=3):
        search = arxiv.Search(
            query=description,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        return [
            {
                "title": result.title,
                "summary": result.summary,
                "url": result.entry_id,
                "published": result.published,
                "authors": [author.name for author in result.authors]
            }
            for result in search.results()
        ]

    def find_references(self, description: str, min_results=3):
        arxiv_refs = self.query_arxiv(description)

        if len(arxiv_refs) < min_results:
            web_refs = self.web_tool.search(description, max_results=5)
            return arxiv_refs + web_refs
        return arxiv_refs