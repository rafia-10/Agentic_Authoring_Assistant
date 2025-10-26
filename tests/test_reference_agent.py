import sys
import os

# Ensure the root directory is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.reference_agent.reference_agent import ReferenceAgent
from tools.web_search_tool import WebSearchTool


def test_fetch_references():

    web_tool = WebSearchTool(api_key=os.getenv("TAVILY_API_KEY"))
    agent = ReferenceAgent(web_search_tool=web_tool)

    # Test fetching references
    query = "Artificial Intelligence"
    refs = agent.fetch_references(query)

    # Assertions
    assert isinstance(refs, list)
    assert all(isinstance(r, dict) for r in refs)
    assert all("title" in r and "url" in r for r in refs)
