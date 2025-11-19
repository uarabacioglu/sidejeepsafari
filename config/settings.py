from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-5a%ja*rp_p%haoyd4ieummm2nk(m%lq+_7egju@tgdwa=($*8)"

DEBUG = False

ALLOWED_HOSTS = [
    "https://seventours.eu.pythonanywhere.com/",
    "seventours.eu.pythonanywhere.com",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "corsheaders",
    "django.contrib.staticfiles",
    "core",
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

CORS_ALLOWED_ORIGINS = [
    "https://sidejeepsafari.com",
    "https://www.sidejeepsafari.com",
]

CSRF_TRUSTED_ORIGINS = [
    "https://sidejeepsafari.com",
    "https://www.sidejeepsafari.com",
]

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "OPTIONS",
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

if DEBUG:
    CORS_ALLOWED_ORIGINS += [
        "http://localhost:4321",
        "http://127.0.0.1:4321",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    CSRF_TRUSTED_ORIGINS += [
        "http://localhost:4321",
        "http://127.0.0.1:4321",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

# Eğer ileride cookie/tabanlı login (session) kullanırsan bunu True yapman gerekecek
# CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
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

STATIC_URL = "static/"

if DEBUG:
    STATIC_ROOT = "static"

STATIC_ROOT = "/home/SevenTours/sidejeepsafari/static"

MEDIA_URL = "media/"

if DEBUG:
    MEDIA_ROOT = "media"

MEDIA_ROOT = "/home/SevenTours/sidejeepsafari/media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
