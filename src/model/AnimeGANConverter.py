import cv2
import numpy as np
import onnxruntime as ort


class AnimeGANConverter:
    def __init__(self, model_paths: dict[str, str]):
        self.models = {
            model: ort.InferenceSession(path)
            for model, path in model_paths.items()
        }

    def convert_to_anime(self, input_path: str, output_path: str, model_type: str):
        if model_type not in self.models:
            raise ValueError(f"Invalid model type: {model_type}")

        # read image
        image = cv2.imread(input_path)
        original_shape = image.shape[:2]  # save original dimensions

        input_image = self._preprocess(image)

        # convert to anime
        session = self.models[model_type]
        input_name = session.get_inputs()[0].name
        output_name = session.get_outputs()[0].name
        result = session.run([output_name], {input_name: input_image})

        # postprocess
        anime_image = np.squeeze(result[0], axis=0)  # remove batch dimension
        anime_image = self._postprocess(anime_image, original_shape)

        # save anime image
        cv2.imwrite(output_path, anime_image)

    def _preprocess(self, image: np.ndarray, multiple_of: int = 8) -> np.ndarray:
        h, w = image.shape[:2]

        # resize image to multiple of 8
        def to_multiple(x, multiple):
            return x if x % multiple == 0 else x + multiple - (x % multiple)

        new_w = to_multiple(w, multiple_of)
        new_h = to_multiple(h, multiple_of)
        image = cv2.resize(image, (new_w, new_h))

        # ensure 3 channels
        if len(image.shape) == 2:  # grayscale
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        elif image.shape[2] == 4:  # RGBA
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)

        # normalize image to [-1, 1]
        image = (image.astype(np.float32) / 127.5) - 1.0

        # add batch dimension (NHWC format)
        image = np.expand_dims(image, axis=0)  # shape: [1, height, width, 3]

        return image

    def _postprocess(self, anime_image: np.ndarray, original_shape: tuple) -> np.ndarray:
        # scale image back to [0, 255]
        anime_image = (anime_image + 1.0) * 127.5
        anime_image = np.clip(anime_image, 0, 255).astype(np.uint8)

        # resize to original dimensions
        return cv2.resize(anime_image, (original_shape[1], original_shape[0]))
