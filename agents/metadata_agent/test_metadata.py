from metadata_agent import generate_metadata

if __name__ == "__main__":
    print("🧠 Agentic Authoring Assistant (A3)")
    description = input("\n👉 Enter your project description:\n> ")

    metadata = generate_metadata(description)

    print("\n🎯 Generated Metadata:")
    print(f"\n📘 Titles: {', '.join(metadata['titles'])}")
    print(f"\n📝 Summary: {metadata['summary']}")
    print(f"\n🏷️ Tags: {', '.join(metadata['tags'])}")
