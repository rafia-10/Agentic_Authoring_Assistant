# agents/refiner_agent/test_metadata_refiner.py
from .metadata_refiner_langgraph import generate_refined_metadata

if __name__ == "__main__":
    print("🧠 Testing Metadata Refiner Agent (Refiner + Metadata)")
    
    # Sample project description
    description = (
        "Agentic AI is an emerging field with a lot of opportunities. "
        "Freelancers on Upwork can leverage autonomous workflows to build innovative projects."
    )

    # Run the agent
    refined_metadata = generate_refined_metadata(description)

    # Print the outputs
    print("\n🎯 Refined Metadata:")
    print(f"\n📘 Titles: {', '.join(refined_metadata['titles'])}")
    print(f"\n📝 Summary: {refined_metadata['summary']}")
    print(f"\n🏷️ Tags: {', '.join(refined_metadata['tags'])}")
