"""
Django settings for myshop project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

from .config import SECRET_KEY
from .config import (
    DATA_BASE,
    DATA_BASE_NAME,
    USER_NAME,
    USER_PASSWORD,
    HOST,
    MAIL_RU_POST,
    MAIL_RU_PASSWORD,
    STRIPE_SECRET_KEY,
    STRIPE_API_VERSION,
    STRIPE_WEBHOOK_SECRET,
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "shop.apps.ShopConfig",
    "cart.apps.CartConfig",
    "orders.apps.OrdersConfig",
    "payment.apps.PaymentConfig",
    "coupons.apps.CouponsConfig",

    "rosetta",
    "parler",
    "localflavor",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "myshop.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",

                "cart.context_processors.cart",
            ],
        },
    },
]

WSGI_APPLICATION = "myshop.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": f"django.db.backends.{DATA_BASE}",
        "NAME": DATA_BASE_NAME,
        "USER": USER_NAME,
        "PASSWORD": USER_PASSWORD,
        "HOST": HOST,
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en"

LANGUAGES = [
    ("en", _("English")),
    ("ru", _("Русский")),
]

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = []

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

CART_SESSION_ID = "cart"

EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 2525
EMAIL_HOST_USER = MAIL_RU_POST
EMAIL_HOST_PASSWORD = MAIL_RU_PASSWORD
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

STRIPE_PUBLIC_KEY = "pk_test_51OyEugD5aN92fFHet0ryTmmeaYWr9x7gzC8ttqiIdzmr9muho52rUo7XIZeoP6voTKG5YP62Cf7N3NBfBiUMOp6K00qLip2oqF"
STRIPE_SECRET_KEY = STRIPE_SECRET_KEY
STRIPE_API_VERSION = STRIPE_API_VERSION

STRIPE_WEBHOOK_SECRET = STRIPE_WEBHOOK_SECRET

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 1

LOCALE_PATHS = [
    BASE_DIR / "locale",
]

PARLER_LANGUAGES = {
    None: (
        {"code": "en"},
        {"code": "ru"},
    ),
    "default": {
        "fallback": "en",
        "hide_untranslated": False,
    }
}
