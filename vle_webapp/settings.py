"""
Django settings for vle_webapp project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import sys

import dj_database_url
from django.utils.translation import gettext_lazy as _

VERSION_NUMBER = 'v0.10.0'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'webapp/static/webapp/PWA/', 'serviceWorker.js')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'm792=#*_(5x5c80&z+i0u80rj+0kn!f94i!*z^xwiy5zb#6a&1')
SECURE_SSL_REDIRECT = bool(os.environ.get('FORCE_SSL', False))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not os.environ.get('ON_HEROKU', False)

ALLOWED_HOSTS = ['.herokuapp.com', 'learn.alumnica.org', 'www.alumnica.org', 'localhost', '127.0.0.1', '10.29.107.68']
CORS_ORIGIN_ALLOW_ALL = True
# Application definition

INSTALLED_APPS = [
    'django_db_prefix',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'webapp.apps.WebappConfig',
    'django_use_email_as_username.apps.DjangoUseEmailAsUsernameConfig',
    'alumnica_model.apps.AlumnicaModelConfig',
    'sweetify',
    'storages',
    'rest_framework',
    'pwa',
    'corsheaders',
    'social_django',
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'vle_webapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

WSGI_APPLICATION = 'vle_webapp.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {'default': {}}

if not os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES['default'] = dj_database_url.config()

# noinspection PyTypeChecker
DATABASES['default']['ATOMIC_REQUESTS'] = True
DB_PREFIX = 'alumnica_'

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

LANGUAGES = [
    ('en', _('English')),
    ('es', _('Spanish')),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

# noinspection PyUnresolvedReferences
MEDIA_ROOT = 'media'
MEDIA_URL = '/media/'
# noinspection PyUnresolvedReferences
STATIC_ROOT = 'static'
STATIC_URL = '/static/'

XAPI_URL = os.environ.get('XAPI_URL')
XAPI_VERSION = os.environ.get('XAPI_VERSION')
XAPI_KEY = os.environ.get('XAPI_KEY')

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

SOCIAL_AUTH_FACEBOOK_KEY = 'update me'
SOCIAL_AUTH_FACEBOOK_SECRET = 'update me'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'update me'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'update me'

LOGIN_URL = 'login_view'
LOGIN_REDIRECT_URL = 'first-login-info_view'
LOGOUT_URL = 'logout_view'

if all([AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME]):
    # Use S3 from Amazon Web Services to store uploaded files
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_AUTO_CREATE_BUCKET = True
    AWS_S3_FILE_OVERWRITE = True
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }

AUTH_USER_MODEL = 'alumnica_model.AuthUser'

admin_names = os.environ.get('ADMIN_NAMES')
admin_emails = os.environ.get('ADMIN_EMAILS')

if admin_names and admin_emails:
    admin_names = admin_names.split(';')
    admin_emails = admin_emails.split(';')

    ADMINS = list(zip(admin_names, admin_emails))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s [%(levelname)s] [%(module)s.%(funcName)s:%(lineno)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'stream': sys.stdout,
        },
        'mail': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'studio': {
            'handlers': ['console', 'mail'],
            'level': os.getenv('STUDIO_LOG_LEVEL', 'DEBUG'),
            'propagate': False
        }
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [],
}


# PWA stuff

PWA_APP_NAME = 'Alumnica'
PWA_APP_DESCRIPTION = "Alumnica EVA"
PWA_APP_THEME_COLOR = '#655dc6'
PWA_APP_DISPLAY = 'fullscreen'
PWA_APP_START_URL = '/learn'
PWA_APP_ICONS = [
    {
        "src": "/static/webapp/media/pwa-icons/icon-72x72.png",
        "sizes": "72x72",
        "type": "image/png"
    },
    {
        "src": "/static/webapp/media/pwa-icons/icon-96x96.png",
        "sizes": "96x96",
        "type": "image/png"
    },
    {
        "src": "/static/webapp/media/pwa-icons/icon-128x128.png",
        "sizes": "128x128",
        "type": "image/png"
    },
    {
        "src": "/static/webapp/media/pwa-icons/icon-144x144.png",
        "sizes": "144x144",
        "type": "image/png"
    },
    {
        "src": "/static/webapp/media/pwa-icons/icon-152x152.png",
        "sizes": "152x152",
        "type": "image/png"
    },
    {
        "src": "/static/webapp/media/pwa-icons/icon-192x192.png",
        "sizes": "192x192",
        "type": "image/png"
    },
    {
        "src": "/static/webapp/media/pwa-icons/icon-384x384.png",
        "sizes": "384x384",
        "type": "image/png"
    },
    {
        "src": "/static/webapp/media/pwa-icons/icon-512x512.png",
        "sizes": "512x512",
        "type": "image/png"
    }
]
