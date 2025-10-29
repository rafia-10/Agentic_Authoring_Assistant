# tools/guardrails_validation.py

class ToxicLanguage:
    """Mock replacement for Guardrails toxic language detector."""
    def __call__(self, value: str):
        bad_words = ["hate", "stupid", "idiot"]
        if any(bad in value.lower() for bad in bad_words):
            return {"valid": False, "error": "Toxic language detected."}
        return {"valid": True}

class UnusualPrompt:
    """Mock replacement for Guardrails unusual prompt detector."""
    def __call__(self, value: str):
        if "ignore previous" in value.lower() or "system prompt" in value.lower():
            return {"valid": False, "error": "Prompt injection attempt detected."}
        return {"valid": True}


def validate_content_safety(text: str) -> str:
    """
    Validate generated text for toxic content.
    Returns original string if safe, raises ValueError if unsafe.
    """
    validator = ToxicLanguage()
    result = validator(text)
    if result["valid"]:
        return text  # keep original string
    else:
        raise ValueError(f"⚠️ Generated text failed content safety check: {text}")


def validate_prompt_injection(prompt: str) -> str:
    """
    Validate input text to block suspicious prompt injections.
    Returns original string if safe, raises ValueError if unsafe.
    """
    validator = UnusualPrompt()
    result = validator(prompt)
    if result["valid"]:
        return prompt  # keep original string
    else:
        raise ValueError(
            "⚠️ Prompt injection detected. Please rephrase your input."
        )
