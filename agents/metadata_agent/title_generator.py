import re, json
from typing import List
from .model_client import ModelClient
from .parsers import parse_numbered_items

class TitleAgent:
    def __init__(self, model_client=None):
        self.model = model_client or ModelClient()

    def generate_titles(self, description: str) -> List[str]:
        prompt = (
            "Return a JSON object: {\"titles\": [\"t1\",\"t2\",\"t3\"]}\n"
            "Generate 3 concise catchy titles for the following AI/ML project description:\n\n"
            f"{description}\n\nJSON:"
        )

        raw = self.model.generate(prompt, max_new_tokens=120, do_sample=False)
        try:
            json_text = re.search(r"\{.*\}", raw, flags=re.DOTALL).group(0)
            data = json.loads(json_text)
            titles = data.get("titles", [])
        except Exception:
            titles = parse_numbered_items(raw)[:3]
        return titles[:3]
