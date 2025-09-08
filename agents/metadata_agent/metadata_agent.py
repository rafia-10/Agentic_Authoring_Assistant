from transformers import pipeline
from tools.nlp_tool import NLPTool   # ✅ custom tool

class MetadataAgent:
    def __init__(self):
        # Load GPT-Neo for text generation
        self.text_generator = pipeline(
            "text-generation", model="EleutherAI/gpt-neo-1.3B"
        )
        # Initialize our spaCy-based NLP tool
        self.nlp_tool = NLPTool()

    def generate_titles(self, description: str):
        """Generate 3 potential project titles using GPT-Neo."""
        prompt = (
            f"Generate 3 concise, catchy titles for this AI project:\n\n"
            f"{description}\n\nTitles:\n1."
        )
        response = self.text_generator(
            prompt, max_length=60, num_return_sequences=1, do_sample=True
        )
        generated_text = response[0]["generated_text"]

        titles = []
        for line in generated_text.split("\n"):
            if line.strip().startswith(tuple("123")):
                titles.append(line.strip().lstrip("123. "))
        return titles[:3] if titles else [generated_text.strip()]

    def generate_summary(self, description: str):
        """Generate a concise project summary using GPT-Neo."""
        prompt = f"Summarize this AI project in 2–3 sentences:\n\n{description}\n\nSummary:"
        response = self.text_generator(
            prompt, max_new_tokens=80, num_return_sequences=1, do_sample=True
        )
        raw_summary = response[0]["generated_text"]

        # Clean output
        cleaned = raw_summary.replace(prompt, "").strip()
        sentences = cleaned.split(".")
        summary = ". ".join(sentences[:3]).strip() + "."
        return summary

    def extract_tags(self, description: str, summary: str):
        """Hybrid approach: GPT-Neo + spaCy (via NLPTool)."""
        # spaCy keywords
        spacy_tags = self.nlp_tool.extract_keywords(description + " " + summary)

        # LLM-generated tags
        prompt = f"List 8–10 relevant tags/keywords for this AI project:\n\n{description}\n\nTags:"
        response = self.text_generator(
            prompt, max_new_tokens=60, num_return_sequences=1, do_sample=True
        )
        llm_text = response[0]["generated_text"]

        llm_tags = []
        for line in llm_text.split("\n"):
            tag = line.strip(" ,.-")
            if tag and not tag.lower().startswith(("tags", "extract", "list of")):
                if len(tag.split()) <= 4:
                    llm_tags.append(tag)

        # Merge + dedup
        return list(set(spacy_tags + llm_tags))

    def generate_metadata(self, description: str) -> dict:
        """Run the full metadata pipeline."""
        titles = self.generate_titles(description)
        summary = self.generate_summary(description)
        tags = self.extract_tags(description, summary)

        return {
            "titles": titles,
            "summary": summary,
            "tags": tags
        }
