import spacy
from transformers import pipeline

# Load spaCy model for NER / tag extraction
nlp = spacy.load("en_core_web_sm")

# Load GPT-Neo via HuggingFace pipeline
text_generator = pipeline("text-generation", model="EleutherAI/gpt-neo-1.3B")

def generate_metadata(description: str) -> dict:
    """
    Generate project titles, summary, and tags from user-provided description.
    """

    # 1️⃣ Title Generation
    # TODO: Call GPT-Neo with prompt to generate 3 catchy titles
    titles = []

    # 2️⃣ Summary Generation
    # TODO: Call GPT-Neo with prompt to generate summary
    summary = ""

    # 3️⃣ Tag Extraction using spaCy NER
    doc = nlp(description + " " + summary)
    tags = list(set([ent.text for ent in doc.ents]))  # Unique named entities

    return {
        "titles": titles,
        "summary": summary,
        "tags": tags
    }
