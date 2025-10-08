# agent/metadata_agent.py
from typing import Dict,List
from pydantic import ValidationError, BaseModel
from .title_generator import TitleAgent
from .summary_generator import SummaryAgent
from .tag_extractor import TagAgent

class Metadata(BaseModel):
    titles: List[str]
    summary: str
    tags: List[str]


class MetadataAgent:
    def __init__(self):
        self.title_agent = TitleAgent()
        self.summary_agent = SummaryAgent()
        self.tag_agent = TagAgent()

    def generate_metadata(self, description: str) -> Dict:
        titles = self.title_agent.generate_titles(description)
        summary = self.summary_agent.generate_summary(description)
        tags = self.tag_agent.extract_tags(description, summary)

        try:
            metadata = Metadata(titles=titles, summary=summary, tags=tags)
            return metadata.dict()
        except ValidationError as e:
            return {"titles": titles, "summary": summary, "tags": tags, "validation_error": str(e)}




   