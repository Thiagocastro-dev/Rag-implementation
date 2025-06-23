import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        self.MPC_PORTARIAS_URL = os.environ.get("MPC_PORTARIAS_URL", "https://www.mpc.pa.gov.br/transparencia/portarias")
        self.QDRANT_URL = os.environ.get("QDRANT_URL", "http://qdrant:6333")
        self.QDRANT_COLLECTION = os.environ.get("QDRANT_COLLECTION", "portarias_mpc")
        self.GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
        self.LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

settings = Settings()