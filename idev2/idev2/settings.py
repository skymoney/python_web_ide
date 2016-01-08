"""
Django settings for idev2 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hkfi#fow4h+f_4av7^9@9v#+8x*=&%b2tcg_@h%19t!8$3-$@0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account',
    'contest',
    'problem',
    'submission',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'idev2.urls'

WSGI_APPLICATION = 'idev2.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'py_ide',
        'HOST':  'localhost', #'121.41.106.89'
        'PORT': 3306,
        'USER': 'root',
        'PASSWORD':  '123456', #'Sydar10',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATIC_PATH = os.path.join(BASE_DIR, 'static').replace('\\', '/')

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'static').replace('\\', '/'),
)

TEMPLATE_DIRS = (os.path.join(BASE_DIR,  'templates'),)

#Code setting
CODE_ROOT_PATH = os.path.join(BASE_DIR, 'code_data').replace("\\", "/")
CASE_ROOT_PATH = os.path.join(CODE_ROOT_PATH, 'case_data').replace("\\", "/")

#DOCKER SETTING
DOCKER_HOST = 'tcp://192.168.99.100:2376'
DOCKER_TLS_VERIFY = "1"
DOCKER_CERT_PATH = '/Users/cheng/.docker/machine/machines/default/'

DOCKER_CODE_PATH = "/mnt/code_data"
DOCKER_CASE_PATH = "/mnt/case_data"