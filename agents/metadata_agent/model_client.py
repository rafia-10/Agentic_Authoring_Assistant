from transformers import pipeline

class ModelClient:
    def __init__(self, model_name="EleutherAI/gpt-neo-1.3B", device=-1):
        self.gen = pipeline("text-generation", model=model_name, device=device)

    def generate(self, prompt: str, max_new_tokens: int = 80, do_sample: bool = True, num_return_sequences: int = 1):
        # This sends our "prompt" (input text) into the model to get generated text back.
        result = self.gen(
            prompt,
            max_new_tokens=max_new_tokens,
            do_sample=do_sample,
            num_return_sequences=num_return_sequences
        )
        # result is a list of dicts; we take the first one and return only the generated text part.
        return result[0]["generated_text"]