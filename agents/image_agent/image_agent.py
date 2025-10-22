from tools.image_generation_tool import ImageGenerationTool

class ImageAgent:
    def __init__(self, image_tool: ImageGenerationTool):
        self.image_tool = image_tool

    def create_project_image(self, project_summary: str, theme: str = "modern AI automation") -> str:
        """
        Generates a project cover image based on metadata summary or concept.
        """
        prompt = f"Generate a visually stunning image representing: {project_summary}. Style: {theme}"
        print(f"🎨 Generating image for: {prompt}")
        image_path = self.image_tool.generate_image(prompt)
        print(f"✅ Image saved to: {image_path}")
        return image_path
