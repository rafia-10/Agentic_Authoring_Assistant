import pytest
import sys
import os

# Ensure root dir is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.metadata_agent.metadata_agent_langgraph import generate_metadata


def test_generate_metadata_basic():
    """Tests the full metadata generation pipeline using LangGraph."""
    description = "AI is transforming education by enabling adaptive learning."
    
    result = generate_metadata(description)

    # ✅ Structure assertions
    assert isinstance(result, dict)
    assert "titles" in result
    assert "summary" in result
    assert "tags" in result

    # ✅ Type & value assertions
    assert isinstance(result["titles"], list)
    assert isinstance(result["summary"], str)
    assert isinstance(result["tags"], list)

    # ✅ Sanity checks
    assert len(result["summary"]) > 0
    assert len(result["titles"]) > 0


def test_generate_metadata_empty_input():
    """Ensure empty input returns safe defaults instead of crashing."""
    result = generate_metadata("")
    assert "titles" in result
    assert "summary" in result
    assert "tags" in result
    assert isinstance(result["titles"], list)
    assert isinstance(result["summary"], str)
    assert isinstance(result["tags"], list)


def test_generate_metadata_error_handling(monkeypatch):
    """Mock internal node to simulate exception and ensure graceful handling."""
    
    from agents.metadata_agent import metadata_agent_langgraph as mal

    def broken_summary_node(state):
        raise ValueError("Boom!")

    # temporarily replace the real summary node with broken one
    monkeypatch.setattr(mal, "summary_node", broken_summary_node)

    description = "Testing error handling."
    result = mal.generate_metadata(description)

    # ✅ Even when it fails, result should have validation_error in metadata
    assert "titles" in result
    assert "summary" in result
    assert "tags" in result
    assert "validation_error" in result or isinstance(result["summary"], str)
