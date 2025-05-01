import os
import tempfile
import asyncio
from typing import Literal
from telegram import File
from src.model.ImageProcessor import ImageProcessor

ModelType = Literal["hayao", "shinkai"]


class AnimeGANConverter:
    def __init__(self, model_paths: dict[str, str]):
        self.processor = ImageProcessor(model_paths)

    async def process_image(self, file: File, model_type: ModelType) -> str:
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as input_file:
            input_path = input_file.name
        await file.download_to_drive(input_path)

        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as output_file:
            output_path = output_file.name

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            self.processor.convert_to_anime,
            input_path,
            output_path,
            model_type
        )

        os.unlink(input_path)
        return output_path
