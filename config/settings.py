from pathlib import Path
import environ
import re
import platform
from .utils.constants import Config, LogLevel

BASE_DIR = Path(__file__).resolve().parent.parent
APPS_DIR = BASE_DIR / "apps"

env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("DJANGO_SECRET_KEY")

DEBUG = env.bool("DJANGO_DEBUG", default=False)

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "rest_framework",
    "drf_spectacular",
    "config",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "config/templates", APPS_DIR / "user/templates"],
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

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

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

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

ASSETS_DIR = BASE_DIR / "config/assets"
Path(ASSETS_DIR).mkdir(parents=True, exist_ok=True)

STATICFILES_DIRS = [ASSETS_DIR]
STATIC_ROOT = BASE_DIR / "/assets"

STATIC_URL = "static/"

MEDIA_ROOT = BASE_DIR / "config/media"
Path(MEDIA_ROOT).mkdir(parents=True, exist_ok=True)
MEDIA_URL = "/media/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
    "EXCEPTION_HANDLER": "config.drf_exception_handler.custom_exception_handler",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Your Project API",
    "DESCRIPTION": "Your project description",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
}

ADMIN_EMAIL = env.list("ADMIN_EMAIL")
DEV_EMAIL = env.list("DEV_EMAIL")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS")
EMAIL_HOST = env("EMAIL_HOST", None)
EMAIL_PORT = env.int("EMAIL_PORT", None)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", None)
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", None)

LOG_DIR = BASE_DIR / "logs"
Path(LOG_DIR).mkdir(parents=True, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "generic": {
            "format": "%(asctime)s - %(levelname)s - %(lineno)s - %(pathname)s - %(module)s\n%(message)s"
        }
    },
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"},
    },
    "handlers": {
        "console": {
            "class": Config.LOG_STREAM_HANDLER_CLASS,
        },
        "api": {
            "level": LogLevel.INFO[0],
            "class": Config.LOG_ROTATING_FILE_HANDLER_CLASS,
            "filename": BASE_DIR / "logs/api.log",
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 5,
            "formatter": "generic",
        },
        "app": {
            "level": LogLevel.INFO[0],
            "class": Config.LOG_ROTATING_FILE_HANDLER_CLASS,
            "filename": BASE_DIR / "logs/app.log",
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 5,
            "formatter": "generic",
        },
        "command_log": {
            "level": LogLevel.INFO[0],
            "class": Config.LOG_ROTATING_FILE_HANDLER_CLASS,
            "filename": BASE_DIR / "logs/commands.log",
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 5,
            "formatter": "generic",
        },
    },
    "loggers": {
        "api": {"handlers": ["console", "api"], "level": "INFO", "propogate": True},
        "command": {
            "handlers": ["console", "command_log"],
            "level": LogLevel.INFO[0],
            "propogate": True,
        },
        "app": {
            "handlers": ["console", "app"],
            "level": LogLevel.INFO[0],
            "propogate": True,
        },
    },
}

path_re = re.compile("(.*)/lib/python(\d)\.(\d)+$")
python_path = list(filter(path_re.match, platform.sys.path))
if python_path:
    python_path = f"{ '/'.join(python_path[0].split('/')[:-2])}/bin/python"
else:
    python_path = ""

PYTHON_PATH = python_path
