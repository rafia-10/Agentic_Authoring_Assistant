from .model_client import ModelClient
from tools.nlp_tool import NLPTool

class SummaryAgent:
    def __init__(self, model_client=None):
        self.model = model_client or ModelClient()
        self.nlp_tool = NLPTool()

    def generate_summary(self, description: str) -> str:
        prompt = (
            "Summarize the following AI/ML project in 2-3 short sentences. "
            "Return only the summary text:\n\n"
            f"{description}\n\nSummary:"
        )
        raw = self.model.generate(prompt, max_new_tokens=100, do_sample=False)
        summary = raw.split("Summary:")[-1].strip()
        return self.nlp_tool.clean_and_truncate(summary, max_sentences=3)
