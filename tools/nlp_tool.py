# tools/nlp_tool.py
import re
from collections import Counter
from typing import List
import spacy

class NLPTool:
    def __init__(self, model_name: str = "en_core_web_sm"):
        """
        Load a small spaCy model that knows how to split sentences and tag words.
        If you don't have the model installed, run:
        python -m spacy download en_core_web_sm
        """
        self.nlp = spacy.load(model_name)

    def clean_text(self, text: str) -> str:
        # simple cleaning: collapse whitespace and strip edges
        return re.sub(r"\s+", " ", text).strip()

    def clean_and_truncate(self, text: str, max_sentences: int = 3) -> str:
        """
        Return up to `max_sentences` sentences from `text`, cleaned.
        Uses spaCy's sentence splitting which avoids breaking on 'e.g.' or 'U.S.'.
        """
        text = self.clean_text(text)
        doc = self.nlp(text)
        sents = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
        return " ".join(sents[:max_sentences])

    def extract_keywords(self, text: str, top_k: int = 10) -> List[str]:
        """
        A simple keyword extractor:
         - keeps nouns, proper nouns, and adjectives
         - lemmatizes (so 'networks' -> 'network')
         - also adds noun chunks (multi-word phrases like 'neural network')
         - returns the top `top_k` by frequency
        """
        text = self.clean_text(text.lower())
        doc = self.nlp(text)

        # candidate tokens: words that are useful (nouns, proper nouns, adjectives)
        candidates = [token.lemma_ for token in doc if token.pos_ in ("NOUN", "PROPN", "ADJ") and not token.is_stop and token.is_alpha]

        # add noun chunks (multi-word phrases)
        chunks = [chunk.text.strip() for chunk in doc.noun_chunks]
        candidates += chunks

        counts = Counter(candidates)
        most_common = [k for k, _ in counts.most_common(top_k)]

        # final cleaning: remove duplicates while preserving order
        final = []
        for k in most_common:
            kk = re.sub(r"[^\w\s\-]", "", k).strip()
            if kk and kk not in final:
                final.append(kk)
        return final
