from .base import *  # noqa

from .secrets import *

DEBUG = False

SECRET_KEY = DJANGO_SECRET

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1", "wilber.social", ".wilber.social"]

ADMIN_URL = DJANGO_ADMIN_URL

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}
