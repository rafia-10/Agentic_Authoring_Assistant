import re, json
from typing import List
from .model_client import ModelClient
from tools.nlp_tool import NLPTool
from .parsers import parse_numbered_items

class TagAgent:
    def __init__(self, model_client=None):
        self.model = model_client or ModelClient()
        self.nlp_tool = NLPTool()

    def extract_tags(self, description: str, summary: str) -> List[str]:
        spacy_tags = self.nlp_tool.extract_keywords(f"{description}\n{summary}")
        prompt = (
            "Return a JSON object: {\"tags\": [\"t1\",\"t2\", ...]}.\n"
            "List 8-10 relevant short tags for this project:\n\n"
            f"{description}\n\nTags JSON:"
        )

        raw = self.model.generate(prompt, max_new_tokens=100, do_sample=True)
        try:
            json_text = re.search(r"\{.*\}", raw, flags=re.DOTALL).group(0)
            data = json.loads(json_text)
            llm_tags = data.get("tags", [])
        except Exception:
            llm_tags = parse_numbered_items(raw)

        merged = list(dict.fromkeys([*spacy_tags, *llm_tags]))
        normalized = []
        for t in merged:
            tt = re.sub(r"[^\w\s\-]", "", t).strip().lower()
            if tt and tt not in normalized:
                normalized.append(tt)
        return normalized[:12]
