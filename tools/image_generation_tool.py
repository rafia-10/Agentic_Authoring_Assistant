import requests
import os
from typing import Optional

class ImageGenerationTool:
    """
    Simple wrapper for NanoBanana image generation API.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("NANOBANANA_API_KEY")
        self.api_url = "https://api.nanobanana.ai/v1/generate"
        if not self.api_key:
            raise ValueError("Missing NANOBANANA_API_KEY in environment.")

    def generate_image(self, prompt: str, size: str = "1024x1024", output_path: str = "generated_image.png") -> str:
        """
        Generate an image from text using NanoBanana API.
        """
        payload = {
            "prompt": prompt,
            "size": size
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        response = requests.post(self.api_url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Some NanoBanana endpoints return 'image_base64' or 'url'
        if "image_base64" in data:
            import base64
            with open(output_path, "wb") as f:
                f.write(base64.b64decode(data["image_base64"]))
        elif "url" in data:
            img_data = requests.get(data["url"]).content
            with open(output_path, "wb") as f:
                f.write(img_data)
        else:
            raise ValueError("Unexpected response structure from NanoBanana API.")

        return output_path
