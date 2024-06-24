import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
DJANGO_ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS")

DATA_BASE = os.environ.get("DATA_BASE")
DATA_BASE_NAME = os.environ.get("DATA_BASE_NAME")
USER_NAME = os.environ.get("USER_NAME")
USER_PASSWORD = os.environ.get("USER_PASSWORD")
HOST = os.environ.get("HOST")

MAIL_RU_POST = os.environ.get("MAIL_RU_POST")
MAIL_RU_PASSWORD = os.environ.get("MAIL_RU_PASSWORD")

STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
STRIPE_API_VERSION = os.environ.get("STRIPE_API_VERSION")

STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET")
