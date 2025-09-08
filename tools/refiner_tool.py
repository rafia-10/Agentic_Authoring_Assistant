
import re

class RefinerTool:
    def __init__(self, llm=None):
        """
        llm: optional language model for polishing text (GPT-Neo, GPT-2, etc.)
        """
        self.llm = llm

    # ----------------- Titles -----------------
    def refine_titles(self, titles):
        """Remove duplicates, shorten, and optionally refine with LLM."""
        unique_titles = list(set([t.strip() for t in titles if t.strip()]))
        refined_titles = []

        for title in unique_titles:
            # ensure <= 10 words
            words = title.split()
            if len(words) > 10:
                title = " ".join(words[:10])
            
            # optional LLM rephrase
            if self.llm:
                title = self.llm_refine(f"Make this a catchy project title: {title}")
            
            refined_titles.append(title)

        return refined_titles

    # ----------------- Summary -----------------
    def refine_summary(self, summary):
        """Polish summary with LLM, ensure 2–3 sentences max."""
        if not summary.strip():
            return "No summary provided."
        
        if self.llm:
            return self.llm_refine(
                f"Rewrite this summary in 2–3 clear sentences:\n{summary}"
            )
        return summary

    # ----------------- Tags -----------------
    def refine_tags(self, tags):
        """Deduplicate and keep concise tags (max 8–10)."""
        clean_tags = []
        for tag in tags:
            if len(tag.split()) > 4:
                continue
            clean_tags.append(tag.strip())

        return list(set(clean_tags))[:10]

    # ----------------- References -----------------
    def refine_references(self, references):
        """Ensure consistent reference style."""
        formatted = []
        seen = set()

        for ref in references:
            if ref in seen:
                continue
            seen.add(ref)
            ref = re.sub(r"\s+", " ", ref.strip())
            formatted.append(ref)

        return formatted

    # ----------------- LLM Wrapper -----------------
    def llm_refine(self, prompt):
        """Helper to call the LLM (if provided)."""
        if not self.llm:
            return prompt
        return self.llm(prompt)

    # ----------------- Main -----------------
    def refine(self, inputs):
        """Refine a raw output dictionary from any agent."""
        return {
            "titles": self.refine_titles(inputs.get("titles", [])),
            "summary": self.refine_summary(inputs.get("summary", "")),
            "tags": self.refine_tags(inputs.get("tags", [])),
            "references": self.refine_references(inputs.get("references", []))
        }
