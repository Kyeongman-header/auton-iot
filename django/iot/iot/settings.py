"""
Django settings for iot project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#ROOT_DIR=os.path.dirname(BASE_DIR)


STATIC_URL='/static/'
#STATIC_DIR=os.path.join(BASE_DIR,'static')
#STATICFILES_DIRS=[STATIC_DIR,]
STATIC_ROOT=os.path.join(BASE_DIR,'static')

# Quick-start development settings - unsuitable f ssh -i "Seoul_testServer.pem" ubuntu@ec2-3-34-78-172.ap-northeast-2.compute.amazonaws.comor production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-58p$i(9qx0*ehb7b$l5!z!gp_5q)^znfftc$6kd6$@(%b_iiw^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['15.164.39.105','127.0.0.1','ec2-54-180-141-52.ap-northeast-2.compute.amazonaws.com','auton-iot.com']
ALLOWED_HOSTS.append(['10.0.5.%d' for x in range(256)])
ALLOWED_HOSTS.append(['10.0.15.%d' for x in range(256)])

# Application definition
CRONJOBS=[
        ('0 0 * * *','airfilter.cron.deleter','>> /tmp/cron.log'),
 ]

INSTALLED_APPS = [
    'corsheaders',
    'django_crontab',
    'django_filters',
    'rest_auth',
    'rest_framework.authtoken',
    'airfilter.apps.AirfilterConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'rest_framework',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_auth.registration',
]
#JWT_AUTH={
#    'JWT_SECRET_KEY' : SECRET_KEY,
#    'JWT_ALGORITHM' : 'HS256',
#    'JWT_AUTH_HEADER_PREFIX' : 'Token',
#    'JWT_EXPIRATION_DELTA' : datetime.timedelta(days=7),
#
#}
SITE_ID=1

AUTH_USER_MODEL='airfilter.MyUser'


#ACCOUNT_UNIQUE_EMAIL=False
#ACCOUNT_USERNAME_REQUIRED=True
#ACCOUNT_AUTHENTICATION_METHOD='username'
#ACCOUNT_LOGOUT_ON_GET=True



REST_FRAMEWORK={
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',],
    'DEFAULT_PERMISSION_CLASSES':[
            'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        ],
    'DEFUALT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        ]
}


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True
#CORS_ORIGIN_WHITELIST = ()

ROOT_URLCONF = 'iot.urls'

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

WSGI_APPLICATION = 'iot.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'iot',
        'USER': 'auton',
        'PASSWORD' : 'mypassword',
        'HOST' : '10.0.10.161',
        'PORT' : '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
