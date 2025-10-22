import os, json, requests
from tavily import TavilyClient

class WebSearchTool:
    def __init__(self):
        self.tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        self.llm_key = os.getenv("OPENROUTER_API_KEY")

    def search(self, query, max_results=5):
        res = self.tavily.search(query=query, max_results=max_results)
        return [{"title": r.get("title",""), "url": r.get("url",""), "snippet": r.get("snippet","")} for r in res.get("results", [])]

    def summarize_and_rank(self, query, results):
        prompt = f"""Summarize and score each result (0–1) for relevance to the query.
Query: {query}
Return JSON like: [{{"title":..., "url":..., "summary":..., "score":...}}]
Results: {json.dumps(results[:5], indent=2)}"""

        try:
            r = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.llm_key}", "Content-Type": "application/json"},
                json={"model": "openai/gpt-4o-mini", "messages": [{"role": "user", "content": prompt}], "temperature": 0.2},
                timeout=40
            )
            data = json.loads(r.json()["choices"][0]["message"]["content"])
            return sorted(data, key=lambda x: x.get("score", 0), reverse=True)
        except Exception as e:
            print(f"⚠️ LLM failed: {e}")
            return [{"title": r["title"], "url": r["url"], "summary": r["snippet"], "score": 0.5} for r in results]

    def search_and_rank(self, query, max_results=5):
        return self.summarize_and_rank(query, self.search(query, max_results))
