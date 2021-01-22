"""
Django settings for sportaj_core project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import environ
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

root = environ.Path(__file__) - 2

# Fetch env vars
os.environ.setdefault("ENV_FILE", root(".env"))
env = environ.Env(DEBUG=(bool, False))
if os.path.isfile(os.environ["ENV_FILE"]):
    env.read_env(os.environ["ENV_FILE"])

SECRET_KEY = env("SECRET_KEY", default="NOT_NEEDED_FOR_DOCKER_BUILDS")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "sportaj_app",
    "taggit",
    "analytical",
    "mathfilters",
    "location_field.apps.DefaultConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "world",
    "static_precompiler",
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

ROOT_URLCONF = "sportaj_core.urls"

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
            ],
        },
    },
]

WSGI_APPLICATION = "sportaj_core.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": env("DATABASE_NAME", default=None),
        "USER": env("DATABASE_USER", default=None),
        "PASSWORD": env("POSTGRES_PASSWORD", default=None),
        "HOST": env("DATABASE_HOST", default="localhost"),
        "PORT": env("DATABASE_PORT", default="5432"),
    }
}

CACHES = {
    "default": {
        "BACKEND": "redis_cache.RedisCache",
        "LOCATION": env("REDIS_URL", default="localhost:6379"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = root(env("STATIC_DIR", default="../static"))

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    # other finders..
    "static_precompiler.finders.StaticPrecompilerFinder",
]

STATIC_PRECOMPILER_COMPILERS = (
    (
        "static_precompiler.compilers.libsass.SCSS",
        {
            "sourcemap_enabled": False,
            "load_paths": ["/path"],
            "precision": 8,
        },
    ),
    (
        "static_precompiler.compilers.libsass.SASS",
        {
            "sourcemap_enabled": False,
            "load_paths": ["/path"],
            "precision": 8,
            "output_style": "compressed",
        },
    ),
)

LOCATION_FIELD = {
    "provider.google.api": "//maps.google.com/maps/api/js?sensor=false",
    "provider.google.api_key": env("GOOGLE_API_KEY", default=None),
    "provider.google.api_libraries": "",
    "provider.google.map.type": "ROADMAP",
}
