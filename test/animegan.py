import os
import unittest
import onnxruntime as ort
from dotenv import load_dotenv
import cv2
from src.animegan import convert_to_anime
from src.env import MODEL_PATH

session = ort.InferenceSession(MODEL_PATH)


if __name__ == '__main__':
    # Load environment variables from .env file
    load_dotenv()

    # Path to the AnimeGANv3 model
    MODEL_PATH = os.getenv("MODEL_PATH", "../model/AnimeGANv3_H.onnx")
    input_image_path = "./imgs/in/v3_0.jpg"
    image = cv2.imread(input_image_path)
    print(image.shape)

    output_image_path = "./imgs/out/v3_0.jpg"

    # Convert the image to anime style
    convert_to_anime(input_image_path, output_image_path)

    print(f"Anime-style image saved to {output_image_path}")