from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")

DATA_BASE = os.environ.get("DATA_BASE")
DATA_BASE_NAME = os.environ.get("DATA_BASE_NAME")
USER_NAME = os.environ.get("USER_NAME")
USER_PASSWORD = os.environ.get("USER_PASSWORD")
HOST = os.environ.get("HOST")
