import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *  # noqa
from .base import env


DEBUG = False

SENTRY_DSN = env("SENTRY_DSN")

sentry_sdk.init(
    dsn=SENTRY_DSN, integrations=[DjangoIntegration()]
)  # noqa F405


SECRET_KEY = env("DJANGO_SECRET")

ALLOWED_HOSTS = [
    "localhost",
    "0.0.0.0",
    "127.0.0.1",
    "wilber.social",
    ".wilber.social",
]

ADMIN_URL = env("DJANGO_ADMIN_URL")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}
