from typing import Optional

from src.Config import Config
from dataclasses import dataclass


@dataclass
class UserModel:
    model: str


class UserModelManager:
    def __init__(self):
        self.user_models: dict[int, UserModel] = {}

    def get_model(self, chat_id: int, caption: str = None) -> str:
        caption_model = self._validate_model(caption) if caption else None

        if caption_model:
            if not Config.IS_STATELESS:
                self.set_model(chat_id, caption_model)
            return caption_model

        # no caption, use stored or default
        return self.user_models.setdefault(chat_id, UserModel(Config.DEFAULT_MODEL)).model

    def set_model(self, chat_id: int, model: str) -> bool:
        if Config.IS_STATELESS:
            return False

        valid_model = self._validate_model(model)
        if not valid_model:
            return False

        self.user_models.setdefault(chat_id, UserModel(Config.DEFAULT_MODEL)).model = valid_model
        return True

    def _validate_model(self, model_text: str) -> Optional[str]:
        if not model_text:
            return None

        model = model_text.lstrip('/').strip().lower()
        return model if model in Config.MODEL_PATHS else None
