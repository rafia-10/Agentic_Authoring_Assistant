from metadata_agent import generate_metadata

if __name__ == "__main__":
    print("🚀 Testing Metadata Agent...\n")
    
    # Example input
    description = input("Enter your project description: ")

    # Generate metadata
    metadata = generate_metadata(description)

    # Display results
    print("\n✅ Metadata Generated:\n")
    print("Titles:")
    for t in metadata['titles']:
        print(" -", t)

    print("\nSummary:\n", metadata['summary'])

    print("\nTags:")
    print(", ".join(metadata['tags']))
