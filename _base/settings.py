"""
Django settings for _base project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-6-)5#072=$qkb8no^i4l!swehy(x-!im1c*x^mvq5+!s(uvlp!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'chat',
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

ROOT_URLCONF = '_base.urls'

# # auth
# AUTH_USER_MODEL = 'chat.User'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = '_base.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SERVER_PORT = 7005
POLL_PORT = 7010

with open('_base/client_keys/private.key', mode='rb') as privatefile:
    keydata = privatefile.read()
PRIVATE_KEY = rsa.PrivateKey.load_pkcs1(keydata)

with open('_base/client_keys/public.key', 'rb') as publicfile:
    pkeydata = publicfile.read()
PUBLIC_KEY = rsa.PublicKey.load_pkcs1(pkeydata)

with open("_base/client_keys/private.dh.key.pem", "rb") as private_key_file:
    dh_private_key_data = private_key_file.read()

DH_PRIVATE_KEY = serialization.load_pem_private_key(
    dh_private_key_data,
    password=None,
    backend=default_backend()
)

DH_PRIVATE_KEY_BYTES = DH_PRIVATE_KEY.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption(),
)

with open("_base/client_keys/public.dh.key.pem", "rb") as public_key_file:
    dh_public_key_data = public_key_file.read()

DH_PUBLIC_KEY = serialization.load_pem_public_key(
    dh_public_key_data,
    backend=default_backend()
)

DH_PUBLIC_KEY_BYTES = DH_PUBLIC_KEY.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
)

# pub_string = rsa.PublicKey.save_pkcs1(PUBLIC_KEY, format='PEM').decode()
# print(pub_string)
# pub_object = rsa.PublicKey.load_pkcs1(pub_string.encode())
# print(pub_object)
# print(pub_object == PUBLIC_KEY)

with open('_base/server_public.key', 'rb') as publicfile:
    pkeydata = publicfile.read()

SERVER_PUB = rsa.PublicKey.load_pkcs1(pkeydata)
