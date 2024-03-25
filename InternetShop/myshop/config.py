import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")

DATA_BASE = os.environ.get("DATA_BASE")
DATA_BASE_NAME = os.environ.get("DATA_BASE_NAME")
USER_NAME = os.environ.get("USER_NAME")
USER_PASSWORD = os.environ.get("USER_PASSWORD")
HOST = os.environ.get("HOST")

MAIL_RU_POST = os.environ.get("MAIL_RU_POST")
MAIL_RU_PASSWORD = os.environ.get("MAIL_RU_PASSWORD")

STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
