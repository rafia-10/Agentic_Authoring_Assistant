# tools/image_generation_tool.py
"""
Image Generation Tool using diffusers + Stable Diffusion.
Handles loading pipeline, prompt building, and image saving.
"""

import os
from typing import List
import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler


MODEL_ID = os.getenv("SD_MODEL_ID", "runwayml/stable-diffusion-v1-5")

# Device config
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# safe default params
DEFAULT_NUM_IMAGES = 1
DEFAULT_GUIDANCE_SCALE = 7.5
DEFAULT_NUM_INFERENCE_STEPS = 30
DEFAULT_HEIGHT = 512
DEFAULT_WIDTH = 512


class ImageGenerationTool:
    def __init__(self, model_id: str = MODEL_ID):
        self.model_id = model_id
        self.pipe = None  # lazy load for performance

    def _load_pipeline(self):
        """Load Stable Diffusion pipeline (lazy init)."""
        if self.pipe is None:
            self.pipe = StableDiffusionPipeline.from_pretrained(
                self.model_id,
                torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32,
                safety_checker=None,
                revision="fp16" if DEVICE == "cuda" else None,
            )
            # faster scheduler
            self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
                self.pipe.scheduler.config
            )
            self.pipe = self.pipe.to(DEVICE)
            try:
                self.pipe.enable_xformers_memory_efficient_attention()
            except Exception:
                pass
        return self.pipe

    def make_prompt(self, summary: str, tags: List[str]) -> str:
        """Build a prompt from metadata (summary + tags)."""
        tags_part = ", ".join(tags) if tags else ""
        return (
            f"Illustration of: {summary}. "
            f"Keywords: {tags_part}. "
            f"Clean, minimal, modern infographic style, high detail."
        )

    def generate(
        self,
        prompt: str,
        out_dir: str = "outputs/images",
        num_images: int = DEFAULT_NUM_IMAGES,
        guidance_scale: float = DEFAULT_GUIDANCE_SCALE,
        num_inference_steps: int = DEFAULT_NUM_INFERENCE_STEPS,
        height: int = DEFAULT_HEIGHT,
        width: int = DEFAULT_WIDTH,
    ):
        """Generate images and return list of file paths."""
        os.makedirs(out_dir, exist_ok=True)
        pipe = self._load_pipeline()

        results = []
        for i in range(num_images):
            image = pipe(
                prompt,
                guidance_scale=guidance_scale,
                num_inference_steps=num_inference_steps,
                height=height,
                width=width,
            ).images[0]

            filename = f"image_{i+1}.png"
            path = os.path.join(out_dir, filename)
            image.save(path)
            results.append({"filename": filename, "path": path, "prompt": prompt})

        return results
