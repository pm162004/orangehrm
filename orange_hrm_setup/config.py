import os
from dotenv import load_dotenv

load_dotenv()


class EnvVariables:

    WEB_URL:str = os.getenv("WEB_URL")
    USER_NAME:str = os.getenv("USER_NAME")
    PASSWORD:str = os.getenv("PASSWORD")


config = EnvVariables()
