from guardrails import Guard
from guardrails.hub import ToxicLanguage
from guardrails.hub import UnusualPrompt

# Initialize Guard for content safety
content_safety_guard = Guard().use(
    ToxicLanguage(threshold=0.5, on_fail="reject")
)

def validate_content_safety(output_text: str):
    """
    Checks generated text for toxic or profane content.
    Raises ValueError if validation fails.
    """
    result = content_safety_guard.validate(output_text)
    if result.validation_passed:
        return result.validated_output
    else:
        raise ValueError("⚠️ Generated text failed content safety check.")


    
prompt_injection_guard = Guard().use(
    UnusualPrompt(on_fail="reject")
)

def validate_prompt_injection(document_text: str):
    """
    Blocks suspicious prompt-injection content dynamically using Guardrails' UnusualPrompt.
    Raises ValueError if validation fails.
    """
    result = prompt_injection_guard.validate(document_text)
    if result.validation_passed:
        return result.validated_output
    else:
        raise ValueError(
            "Sorry, this request contains language that may trigger safety filters. "
            "Please try rephrasing or simplifying it."
        )