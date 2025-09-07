from reference_agent import generate_references

if __name__ == "__main__":
    print("🚀 Testing Reference Agent...\n")

    description = input("Enter your project description: ")
    references = generate_references(description, max_results=3)

    print("\n✅ References Found:\n")
    for ref in references:
        print(f"- {ref['title']} ({ref['year']})")
        print(f"  Authors: {', '.join(ref['authors'])}")
        print(f"  Link: {ref['link']}\n")
