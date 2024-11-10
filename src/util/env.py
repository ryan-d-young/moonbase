from collections import UserString

import os
import dotenv


dotenv.load_dotenv()


class Var(UserString):
    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return os.getenv(self.name)
