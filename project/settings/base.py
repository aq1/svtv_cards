from pathlib import Path

import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

env = environ.Env()
env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

IMAGES_DIR = BASE_DIR / 'assets'

SECRET_KEY = env('SECRET_KEY', default='django-insecure-sdlz*06c_701ly--j8^#l!au&&4t1j)_e_@jkg#e^a&*w+tv39')

DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 'online',
    'webhooks',
    'cards',
    'notifications',
    'youtube',
    'test_constructor',
    'currencies',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

DATABASES = {
    'default': env.db(default='sqlite:///db.sqlite3')
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/webhook/static/'
STATIC_ROOT = BASE_DIR / 'static'
if DEBUG:
    STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

WEBHOOK_KEY = env('WEBHOOK_KEY')
GHOST_URL = env('GHOST_URL')
GHOST_API_KEY = env('GHOST_API_KEY')
GHOST_ADMIN_KEY = env('GHOST_ADMIN_KEY')
GHOST_CURRENCY_POST_ID = env('GHOST_CURRENCY_POST_ID')
TELEGRAM_TOKEN = env('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = env('TELEGRAM_CHAT_ID')
TELEGRAM_ADMIN_ID = env('TELEGRAM_ADMIN_ID')
TELEGRAM_USER = env('TELEGRAM_USER')

YOUTUBE_CHANNEL_ID = env('YOUTUBE_CHANNEL_ID')
YOUTUBE_BANNER_POST_ID = env('YOUTUBE_BANNER_POST_ID')
YOUTUBE_API_KEY = env('YOUTUBE_API_KEY')

# Celery
if USE_TZ:
    CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_URL = env('REDIS_URL')
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_TIME_LIMIT = 5 * 60
CELERY_TASK_SOFT_TIME_LIMIT = 60

SENTRY_URL = env('SENTRY_URL')

if not DEBUG:
    sentry_sdk.init(
        dsn=SENTRY_URL,
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
    )

# Tweepy
TWITTER_CONSUMER_KEY = env('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = env('TWITTER_CONSUMER_SECRET')
TWITTER_REDIRECT_URI = env('TWITTER_REDIRECT_URI')
TWITTER_ACCESS_TOKEN = env('TWITTER_ACCESS_TOKEN')
TWITTER_SECRET_TOKEN = env('TWITTER_SECRET_TOKEN')

