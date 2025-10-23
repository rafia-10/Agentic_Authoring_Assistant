# agents/image_agent/test_image_generation.py

import os
from tools.image_generation_tool import ImageTool  
from agents.image_agent import ImageAgent  

# ------------------ Setup ------------------
def main():
    print("🎨 Testing Image Generation Agent\n")

    api_key = os.getenv("NANOBANANA_API_KEY")
    if not api_key:
        print("❌ Missing API key. Please set 'NANOBANANA_API_KEY' in your environment.")
        return

    # Initialize the tool + agent
    image_tool = ImageTool(api_key=api_key)
    agent = ImageAgent(image_tool)

    # ------------------ Test Prompt ------------------
    prompt = "A futuristic AI-powered workspace with glowing neural circuits and code holograms"

    print(f"🧠 Prompt: {prompt}\n")
    print("⚙️ Generating image, please wait...\n")

    # ------------------ Generate Image ------------------
    image_url = agent.generate_image(prompt)

    if image_url:
        print("✅ Image successfully generated!")
        print(f"🖼️ Image URL: {image_url}")
    else:
        print("❌ Image generation failed. Check your API key or prompt.")

# ------------------ Run ------------------
if __name__ == "__main__":
    main()
