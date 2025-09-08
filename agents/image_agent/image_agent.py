from tools.image_generation_tool import ImageGenerationTool

class ImageAgent:
    def __init__(self):
        self.img_tool = ImageGenerationTool()

    def generate_image(self, description: str):
        prompt = f"An illustration for: {description}"
        return self.img_tool.generate(prompt, num_images=1)
