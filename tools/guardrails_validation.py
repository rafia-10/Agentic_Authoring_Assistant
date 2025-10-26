# from guardrails import Guard
# from guardrails.validators import ToxicLanguage
# from guardrails.hub import UnusualPrompt

# # Initialize Guard for content safety
# content_safety_guard = Guard().use(
#     ToxicLanguage(threshold=0.5, on_fail="reject")
# )

# def validate_content_safety(output_text: str):
#     """
#     Checks generated text for toxic or profane content.
#     Raises ValueError if validation fails.
#     """
#     result = content_safety_guard.validate(output_text)
#     if result.validation_passed:
#         return result.validated_output
#     else:
#         raise ValueError("⚠️ Generated text failed content safety check.")


    
# prompt_injection_guard = Guard().use(
#     UnusualPrompt(on_fail="reject")
# )

# def validate_prompt_injection(document_text: str):
#     """
#     Blocks suspicious prompt-injection content dynamically using Guardrails' UnusualPrompt.
#     Raises ValueError if validation fails.
#     """
#     result = prompt_injection_guard.validate(document_text)
#     if result.validation_passed:
#         return result.validated_output
#     else:
#         raise ValueError(
#             "Sorry, this request contains language that may trigger safety filters. "
#             "Please try rephrasing or simplifying it."
#         )
    
# # tools/guardrails_validation.py



class ToxicLanguage:
    """Mock replacement for Guardrails toxic language detector."""
    def __call__(self, value: str):
        bad_words = ["hate", "kill", "stupid", "idiot"]
        if any(bad in value.lower() for bad in bad_words):
            return {"valid": False, "error": "Toxic language detected."}
        return {"valid": True}

class UnusualPrompt:
    """Mock replacement for Guardrails unusual prompt detector."""
    def __call__(self, value: str):
        if "ignore previous" in value.lower() or "system prompt" in value.lower():
            return {"valid": False, "error": "Prompt injection attempt detected."}
        return {"valid": True}

def validate_content_safety(text):
    
    validator = ToxicLanguage()
    return validator(text)["valid"]

def validate_prompt_injection(prompt):

    validator = UnusualPrompt()
    return validator(prompt)["valid"]
