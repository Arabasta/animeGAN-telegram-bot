import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    MAX_CONCURRENT_REQUESTS = 10
    MODEL_PATHS = {
        "hayao": "../model/AnimeGANv3_Hayao_36.onnx",
        "shinkai": "../model/AnimeGANv3_Shinkai_37.onnx"
    }
    DEFAULT_MODEL = "hayao"
    IS_STATELESS = False  # set to True for serverless (lambda) deployment
