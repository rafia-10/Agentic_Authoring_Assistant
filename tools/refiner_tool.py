# tools/refiner_tool.py
from typing import List

class RefinerTool:
    def refine_titles(self, titles: List[str]) -> List[str]:
        # Can add more sophisticated cleaning or LLM-based refinement if needed
        return [t.strip().capitalize() for t in titles]

    def refine_summary(self, summary: str) -> str:
        return summary.strip()

    def refine_tags(self, tags: List[str]) -> List[str]:
        # Remove duplicates
        seen = set()
        refined = []
        for tag in tags:
            t = tag.strip().lower()
            if t not in seen and t:
                refined.append(t)
                seen.add(t)
        return refined
