import spacy
from transformers import pipeline

# Load spaCy model for NER
nlp = spacy.load("en_core_web_sm")

# Load GPT-Neo via HuggingFace
text_generator = pipeline("text-generation", model="EleutherAI/gpt-neo-1.3B")


def generate_titles(description: str):
    """Generate 3 potential project titles from description using GPT-Neo."""
    prompt = f"Generate 3 concise, catchy titles for this AI project:\n\n{description}\n\nTitles:\n1."
    response = text_generator(prompt, max_length=60, num_return_sequences=1, do_sample=True)

    generated_text = response[0]['generated_text']
    titles = []
    for line in generated_text.split("\n"):
        if line.strip().startswith(tuple("123")):
            titles.append(line.strip().lstrip("123. "))
    return titles[:3] if titles else [generated_text.strip()]


def generate_summary(description: str):
    """Generate a concise project summary from description."""
    prompt = f"Summarize this AI project in 2–3 sentences:\n\n{description}\n\nSummary:"
    response = text_generator(prompt, max_new_tokens=80, num_return_sequences=1, do_sample=True)
    raw_summary = response[0]['generated_text']

    # Clean up: remove echoes & keep first 3 sentences max
    cleaned = raw_summary.replace(prompt, "").strip()
    sentences = cleaned.split(".")
    summary = ". ".join(sentences[:3]).strip() + "."
    return summary



def extract_tags(description: str, summary: str):
    """Hybrid: combine LLM-suggested tags + spaCy NER entities."""
    
    # spaCy tags
    doc = nlp(description + " " + summary)
    spacy_tags = [ent.text for ent in doc.ents]

    # LLM tags
    prompt = f"List 8–10 relevant tags/keywords for this AI project:\n\n{description}\n\nTags:"
    response = text_generator(prompt, max_new_tokens=60, num_return_sequences=1, do_sample=True)
    llm_text = response[0]['generated_text']

    # Parse into clean tags
    llm_tags = []
    for line in llm_text.split("\n"):
        tag = line.strip(" ,.-")
        if tag and not tag.lower().startswith(("tags", "extract", "list of")):
            # only keep short keyword-like outputs
            if len(tag.split()) <= 4:
                llm_tags.append(tag)

    # Merge + dedup
    combined_tags = list(set(spacy_tags + llm_tags))
    return combined_tags

def generate_metadata(description: str) -> dict:
    """Generate titles, summary, and tags for a project description."""
    titles = generate_titles(description)
    summary = generate_summary(description)
    tags = extract_tags(description, summary)

    return {
        "titles": titles,
        "summary": summary,
        "tags": tags
    }
