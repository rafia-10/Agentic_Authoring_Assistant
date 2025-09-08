

from agents.metadata_agent.metadata_agent import MetadataAgent
from agents.reference_agent.reference_agent import ReferenceAgent
from agents.image_agent.image_agent import ImageAgent
from agents.refiner_agent.refiner_agent import RefinerAgent

def main():
    # 1️⃣ Collect user input
    description = input("Enter your project description: ").strip()
    repo = input("Enter repository link (optional): ").strip()
    dataset = input("Enter dataset info (optional): ").strip()
    results = input("Enter experiment results (optional): ").strip()

    project_input = {
        "description": description,
        "repo": repo,
        "dataset": dataset,
        "results": results
    }

    # 2️⃣ Initialize agents
    metadata_agent = MetadataAgent()
    reference_agent = ReferenceAgent()
    image_agent = ImageAgent()
    refiner_agent = RefinerAgent()

    # 3️⃣ Generate metadata
    metadata = metadata_agent.generate_metadata(description)

    # 4️⃣ Find references
    references = reference_agent.find_references(description)

    # 5️⃣ Generate image
    images = image_agent.generate_image(metadata["summary"], metadata["tags"])

    # 6️⃣ Combine all raw outputs
    raw_outputs = {
        **metadata,
        "references": references,
        "images": images
    }

    # 7️⃣ Refine everything
    final_outputs = refiner_agent.refine(raw_outputs)

    # 8️⃣ Print or save final structured project info
    print("\n✅ Final Project Metadata:")
    for key, value in final_outputs.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
