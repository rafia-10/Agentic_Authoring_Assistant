from agents.refiner_agent.refiner_agent_langgraph import generate_refined_metadata

def test_refine_metadata():
    metadata = {
        "title": "Old Title",
        "tags": ["old", "tag"],
        "summary": "Old summary text."
    }
    refined = generate_refined_metadata(metadata)
    assert "title" in refined
    assert "tags" in refined
    assert "summary" in refined
    assert isinstance(refined["tags"], list)
