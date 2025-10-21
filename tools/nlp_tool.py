from typing import List
import re
from llama_index.llms.openrouter import OpenRouter


class NLPTool:
    def __init__(self, api_key: str):
        self.client = OpenRouter(api_key=api_key)

    def clean_text(self, text: str) -> str:
        return re.sub(r"\s+", " ", text).strip()

    def _get_text(self, response) -> str:
    # Try multiple common attributes
      if hasattr(response, "completion"):
          return response.completion
      elif hasattr(response, "text"):
          return response.text
      elif hasattr(response, "choices") and len(response.choices) > 0:
          return getattr(response.choices[0], "text", "")
      return ""

    def generate_titles(self, description: str, max_titles: int = 3) -> List[str]:
        prompt = f"Generate {max_titles} creative, relevant titles for this text:\n{description}"
        response = self.client.complete(prompt)
        text = self._get_text(response)
        titles = [t.strip() for t in text.split("\n") if t.strip()]
        return titles[:max_titles]

    def generate_summary(self, description: str) -> str:
        prompt = f"Write a concise, informative summary of this text:\n{description}"
        response = self.client.complete(prompt)
        summary = self._get_text(response)
        return summary.strip()

    def extract_tags(self, description: str, summary: str, max_tags: int = 10) -> List[str]:
        prompt = (
            f"Extract up to {max_tags} highly relevant tags/keywords from this description "
            f"and summary:\nDescription: {description}\nSummary: {summary}"
        )
        response = self.client.complete(prompt)
        text = self._get_text(response)
        tags = [t.strip("# ").lower() for t in re.split(r",|\n", text) if t.strip()]
        return tags[:max_tags]
