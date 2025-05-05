import logging


class LoggerFactory:
    @staticmethod
    def get_logger(name: str = None) -> logging.Logger:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),  # Console output
                logging.FileHandler('app.log')  # File output
            ]
        )
        return logging.getLogger(name or __name__)