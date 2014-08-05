# Most all of this is linked to what you put on "options.py". I don't recommend changing anything,
# unless you know what you are doing.

from options import *

"""
Django settings for OpenSource project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

ADMINS = (('Alex', 'wolfa97@comcast.net')) #I'll get an email if you have an error, and so know to fix it.

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'crt@q-4ekx9hu!k3h_f!ns@&unb-ifzfl0clbgz(#3gb@mle6&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = debug

ALLOWED_HOSTS = [
    "."+site_url,
    "."+site_url+".",
]

TEMPLATE_DEBUG = True

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Login',
    'Base',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'OpenSource.urls'

WSGI_APPLICATION = 'OpenSource.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = time_zone

USE_I18N = True

USE_L10N = True

USE_TZ = True

EMAIL_HOST = email_host
EMAIL_HOST_USER = email_username
EMAIL_HOST_PASSWORD = email_password
EMAIL_PORT = email_port

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
