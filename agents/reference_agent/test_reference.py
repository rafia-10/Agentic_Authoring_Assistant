from .reference_agent import ReferenceAgent
from tools.web_search_tool import WebSearchTool

if __name__ == "__main__":
    print("🚀 Testing Reference Agent...\n")

    web_tool = WebSearchTool()
    # Create the agent
    ref_agent = ReferenceAgent(web_tool)

    # Get project description
    description = input("Enter your project description: ")

    # Fetch references properly
    references = ref_agent.fetch_references(description)

    print("\n✅ References Found:\n")
    for ref in references:
        print(f"- {ref['title']}")
        print(f"  Link: {ref.get('url')}")
        

