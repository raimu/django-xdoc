"""
Django settings for testproject project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i0k9j@-*a%nx2^xkp^6)f6$w78!v7(!xn$&*=$zuzu@tywzedw'

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
    # my apps
    'xdoc',
    'rest_framework',
    'guardian',
    'crispy_forms',
    'testapp',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'testproject.urls'

WSGI_APPLICATION = 'testproject.wsgi.application'


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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

# my config
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
    'PAGINATE_BY': 10
}

CRISPY_TEMPLATE_PACK = 'bootstrap3'

ANONYMOUS_USER_ID = -1

XDOC_NODE_MAP = {
    'Node': {
        'label': 'Directory',
        'node': 'xdoc.models.Node',
        'form': 'xdoc.models.NodeForm',
        'thumbnail': '/static/xdoc/lib/icons/places/folder.png'
    },
    'Document': {
        'label': 'Document',
        'node': 'xdoc.models.Document',
        'form': 'xdoc.models.DocumentForm',
        'thumbnail': '/static/xdoc/lib/icons/mimetypes/text-plain.png'
    },
    'BusinessCard': {
        'label': 'Businesscard',
        'node': 'testapp.models.BusinessCard',
        'form': 'testapp.models.BusinessCardForm',
        'thumbnail': '/static/xdoc/lib/icons/mimetypes/text-x-vcard.png',
        'edit': {
            'template': 'testapp/edit.html',
        },
    },
}