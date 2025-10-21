# tools/nlp_tool.py
from typing import List
import re   
from llama_index.llms.openrouter import OpenRouter


class NLPTool:
    def __init__(self, api_key: str):
        self.client = OpenRouter(api_key=api_key)

    def clean_text(self, text: str) -> str:
        return re.sub(r"\s+", " ", text).strip()

    def generate_titles(self, description: str, max_titles: int = 3) -> List[str]:
        prompt = f"Generate {max_titles} creative, relevant titles for this text:\n{description}"
        response = self.client.completion(prompt)
        titles = [t.strip() for t in response.split("\n") if t.strip()]
        return titles[:max_titles]

    def generate_summary(self, description: str) -> str:
        prompt = f"Write a concise, informative summary of this text:\n{description}"
        summary = self.client.completion(prompt)
        return summary.strip()

    def extract_tags(self, description: str, summary: str, max_tags: int = 10) -> List[str]:
        prompt = (
            f"Extract up to {max_tags} highly relevant tags/keywords from this description "
            f"and summary:\nDescription: {description}\nSummary: {summary}"
        )
        response = self.client.completion(prompt)
        tags = [t.strip("# ").lower() for t in re.split(r",|\n", response) if t.strip()]
        return tags[:max_tags]
