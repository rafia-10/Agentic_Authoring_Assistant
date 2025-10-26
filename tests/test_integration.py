import pytest
from main import run_all_agents

def test_full_pipeline():
    text = "AI is revolutionizing technology."
    result = run_all_agents(text)
    assert "title" in result
    assert "tags" in result
    assert "summary" in result
    assert "references" in result
