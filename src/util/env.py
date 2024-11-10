from pathlib import Path

import os
import dotenv



class Env:
    def __init__(self):
        dotenv.load_dotenv()

    def __getattr__(self, name: str) -> str:
        return os.getenv(name)
