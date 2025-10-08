from .metadata_agent import MetadataAgent 

if __name__ == "__main__":
    print("🧠 Agentic Authoring Assistant (A3)")
    description = input("\n👉 Enter your project description:\n> ")
    agent = MetadataAgent()
    metadata = agent.generate_metadata(description)

    print("\n🎯 Generated Metadata:")
    print(f"\n📘 Titles: {', '.join(metadata['titles'])}")
    print(f"\n📝 Summary: {metadata['summary']}")
    print(f"\n🏷️ Tags: {', '.join(metadata['tags'])}")
