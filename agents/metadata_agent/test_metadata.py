# test_metadata_agent.py
import os
from metadata_agent_langgraph import generate_metadata

if __name__ == "__main__":
    print("🧠 Agentic Authoring Assistant (3A)")

    # Make sure your OpenRouter API key is set in environment variables
    if not os.getenv("OPENROUTER_API_KEY"):
        raise ValueError("Please set your OpenRouter API key in the environment variable OPENROUTER_API_KEY")

    description = input("\n👉 Enter your project description:\n> ")

    # Call the LangGraph orchestrator
    metadata = generate_metadata(description)

    print("\n🎯 Generated Metadata:")
    print(f"\n📘 Titles: {', '.join(metadata.get('titles', []))}")
    print(f"\n📝 Summary: {metadata.get('summary', '')}")
    print(f"\n🏷️ Tags: {', '.join(metadata.get('tags', []))}")
