"""
Django settings for hoopoe project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
from email.policy import default
import os
from pathlib import Path
import datetime

import logging
from decouple import config
import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.redis import RedisIntegration

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", default="", cast=lambda v: v.split(" "))
CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS", default="", cast=lambda v: v.split(" ")
)
CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS", default="", cast=lambda v: v.split(" ")
)

# Application definition
INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Rest framework apps
    "rest_framework",
    "rest_framework.authtoken",
    # Third party apps
    "django_extensions",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "rest_framework_api_key",
    "corsheaders",
    "drf_yasg",
    "imagekit",
    "storages",
    # Hoopoe apps
    "core.apps.CoreConfig",
    "users.apps.UsersConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "hoopoe.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = "hoopoe.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB", "hoopoe"),
        "USER": config("POSTGRES_USER", "hoopoe"),
        "PASSWORD": config("POSTGRES_PASSWORD", "hoopoe"),
        "HOST": config("POSTGRES_HOST", "localhost"),
        "PORT": config("POSTGRES_PORT", "5432"),
        "TEST": {
            "MIRROR": "default",
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

USE_S3 = config("USE_S3", default=False, cast=bool)
if USE_S3:
    # aws settings
    AWS_ACCESS_KEY_ID = config("S3_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = config("S3_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = config("S3_STORAGE_BUCKET_NAME")
    AWS_S3_ENDPOINT_URL = config("S3_ENDPOINT_URL")
    AWS_DEFAULT_ACL = None
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}

    # s3 static settings
    STATIC_LOCATION = "static"
    STATIC_URL = f"{AWS_S3_ENDPOINT_URL}/{STATIC_LOCATION}/"
    STATICFILES_STORAGE = "hoopoe.storage_backends.StaticStorage"

    # s3 public media settings
    PUBLIC_MEDIA_LOCATION = "media"
    MEDIA_URL = f"{AWS_S3_ENDPOINT_URL}/{PUBLIC_MEDIA_LOCATION}/"
    DEFAULT_FILE_STORAGE = "hoopoe.storage_backends.PublicMediaStorage"
else:
    STATIC_URL = "/staticfiles/"
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

    MEDIA_URL = "/mediafiles/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")

# STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 20,
}


EMAIL_HOST = config("EMAIL_HOST")
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=False, cast=bool)

EMAIL_UPUPA_USER = config("EMAIL_UPUPA_USER")
EMAIL_UPUPA_PASSWORD = config("EMAIL_UPUPA_PASSWORD")


API_KEY_CUSTOM_HEADER = "HTTP_X_API_KEY"


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(minutes=5)
    if not DEBUG
    else datetime.timedelta(days=5),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=1)
    if not DEBUG
    else datetime.timedelta(weeks=4),
}


# CELERY STUFF
REDIS_HOST = config("REDIS_HOST", default="localhost")
REDIS_PORT = config("REDIS_PORT", default=6379, cast=int)
REDIS_PASSWORD = config("REDIS_PASSWORD", default="")
REDIS_BROKER_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_BROKER_URL,
    }
}


CELERY_BROKER_URL = REDIS_BROKER_URL
CELERY_RESULT_BACKEND = REDIS_BROKER_URL
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Tehran"
CELERY_TRANSPORT_OPTIONS = {
    "fanout_prefix": True,
    "fanout_patterns": True,
    "socket_timeout": 10,
    "visibility_timeout": 10,
}


SENTRY_DSN = config("SENTRY_DSN", default="")
if SENTRY_DSN:
    SENTRY_LOG_LEVEL = config("SENTRY_LOG_LEVEL", default=logging.INFO, cast=int)

    sentry_logging = LoggingIntegration(
        level=SENTRY_LOG_LEVEL,  # Capture info and above as breadcrumbs
        event_level=logging.ERROR,  # Send errors as events
    )
    integrations = [
        sentry_logging,
        DjangoIntegration(),
        CeleryIntegration(),
        RedisIntegration(),
    ]
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=integrations,
        environment=config("SENTRY_ENVIRONMENT", default="prod"),
        traces_sample_rate=config("SENTRY_TRACES_SAMPLE_RATE", default=1.0, cast=float),
        release="hoopoe-core@latest",
        send_default_pii=True,
    )

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Token": {"type": "apiKey", "name": "Authorization", "in": "header"},
        "API Key": {"type": "apiKey", "name": "X-API-KEY", "in": "header"},
    }
}
