import os
import tempfile
import asyncio
from telegram import File
from src.model.AnimeGANConverter import AnimeGANConverter


class ImageProcessor:
    def __init__(self, model_paths: dict[str, str]):
        self.converter = AnimeGANConverter(model_paths)

    async def process_image(self, file: File, model_type: str) -> str:
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as input_file:
            input_path = input_file.name
        await file.download_to_drive(input_path)

        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as output_file:
            output_path = output_file.name

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            self.converter.convert_to_anime,
            input_path,
            output_path,
            model_type
        )

        os.unlink(input_path)
        return output_path
