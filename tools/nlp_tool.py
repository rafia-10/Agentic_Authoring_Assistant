import spacy

class NLPTool:
    def __init__(self, model="en_core_web_sm"):
        self.nlp = spacy.load(model)

    def extract_entities(self, text: str):
        """Return list of named entities (ORG, PERSON, etc.)."""
        doc = self.nlp(text)
        return [(ent.text, ent.label_) for ent in doc.ents]

    def extract_keywords(self, text: str):
        """Naive keyword extraction: nouns and proper nouns."""
        doc = self.nlp(text)
        return [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]]
