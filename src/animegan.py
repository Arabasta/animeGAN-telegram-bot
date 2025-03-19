import cv2
import numpy as np
import onnxruntime as ort

from src.env import MODEL_PATH

# load model
session = ort.InferenceSession(MODEL_PATH)


def preprocess_image(image, multiple_of=8):
    """Preprocess the image for AnimeGANv3."""
    # Get the original dimensions
    h, w = image.shape[:2]

    # Resize the image to a multiple of 8 (or 16)
    def to_multiple(x, multiple):
        return x if x % multiple == 0 else x + multiple - (x % multiple)

    new_w = to_multiple(w, multiple_of)
    new_h = to_multiple(h, multiple_of)
    image = cv2.resize(image, (new_w, new_h))

    # Ensure the image has 3 channels (RGB)
    if len(image.shape) == 2:  # Grayscale image
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    elif image.shape[2] == 4:  # RGBA image
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)

    # Normalize the image to [-1, 1]
    image = (image.astype(np.float32) / 127.5) - 1.0

    # Add a batch dimension (NHWC format)
    image = np.expand_dims(image, axis=0)  # Shape: [1, height, width, 3]

    return image


def convert_to_anime(input_path, output_path):
    """Convert an image to anime style using AnimeGANv3"""
    # Load image
    image = cv2.imread(input_path)
    original_shape = image.shape[:2]  # Save the original dimensions

    # Preprocess
    input_image = preprocess_image(image)

    # Run inference
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    print(f"Input name {input_name}, shape: {session.get_inputs()[0].shape}")
    result = session.run([output_name], {input_name: input_image})

    # Postprocess
    anime_image = np.squeeze(result[0], axis=0)  # Remove batch dimension
   #  anime_image = np.transpose(anime_image, (1, 2, 0))  # CHW to HWC
    #anime_image = (anime_image * 255).astype(np.uint8)
    anime_image = postprocess_image(anime_image, original_shape)

    # Save the anime image
    cv2.imwrite(output_path, anime_image)


def postprocess_image(anime_image, original_shape):
    """Postprocess the anime-style image."""
    # Scale the image back to [0, 255]
    anime_image = (anime_image + 1.0) * 127.5
    anime_image = np.clip(anime_image, 0, 255).astype(np.uint8)

    # Resize the image to the original dimensions
    anime_image = cv2.resize(anime_image, (original_shape[1], original_shape[0]))

    return anime_image
