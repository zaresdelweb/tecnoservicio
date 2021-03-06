# -*- coding: utf-8 -*-
'''
Production Configurations

- Use djangosecure
- Use Amazon's S3 for storing static files and uploaded media
- Use sendgrid to send emails
- Use MEMCACHIER on Heroku
'''
from __future__ import absolute_import, unicode_literals


from boto.s3.connection import OrdinaryCallingFormat
from django.utils import six

from .common import *  # noqa

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Raises ImproperlyConfigured exception if DJANO_SECRET_KEY not in os.environ
SECRET_KEY = VAR_SECRET_KEY

# SITE CONFIGURATION
# ------------------------------------------------------------------------------
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.6/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["*"]
# END SITE CONFIGURATION

INSTALLED_APPS += ("gunicorn", )

# STORAGE CONFIGURATION
# ------------------------------------------------------------------------------
# Uploaded Media Files
# ------------------------
# See: http://django-storages.readthedocs.org/en/latest/index.html
INSTALLED_APPS += (
    'storages',
)
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

AWS_ACCESS_KEY_ID = VAR_DJANGO_AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = VAR_AWS_SECRET_ACCESS_KEY
AWS_STORAGE_BUCKET_NAME = VAR_AWS_STORAGE_BUCKET_NAME
AWS_AUTO_CREATE_BUCKET = False
AWS_QUERYSTRING_AUTH = False
AWS_S3_CALLING_FORMAT = OrdinaryCallingFormat()

# AWS cache settings, don't change unless you know what you're doing:
AWS_EXPIRY = 60 * 60 * 24 * 7

# TODO See: https://github.com/jschneier/django-storages/issues/47
# Revert the following and use str after the above-mentioned bug is fixed in
# either django-storage-redux or boto
AWS_HEADERS = {
    'Cache-Control': six.b('max-age=%d, s-maxage=%d, must-revalidate' % (
        AWS_EXPIRY, AWS_EXPIRY))
}

# URL that handles the media served from MEDIA_ROOT, used for managing stored files.
MEDIA_URL = 'https://s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME

# Static Assests
# ------------------------

STATICFILES_STORAGE = DEFAULT_FILE_STORAGE
STATIC_URL = MEDIA_URL

# See: https://github.com/antonagestam/collectfast
# For Django 1.7+, 'collectfast' should come before 'django.contrib.staticfiles'
AWS_PRELOAD_METADATA = True
INSTALLED_APPS = ('collectfast', ) + INSTALLED_APPS

# EMAIL
# ------------------------------------------------------------------------------
DEFAULT_FROM_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_HOST = VAR_EMAIL_HOST
EMAIL_HOST_PASSWORD = VAR_EMAIL_HOST_PASSWORD
EMAIL_HOST_USER = VAR_EMAIL_HOST_USER
EMAIL_PORT = VAR_EMAIL_PORT
EMAIL_SUBJECT_PREFIX = EMAIL_SUBJECT_PREFIX
EMAIL_USE_TLS = True
SERVER_EMAIL = EMAIL_HOST_USER

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/templates/api/#django.template.loaders.cached.Loader
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ]),
]

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
DATABASES['default'] = VAR_DATABASES

# Your production stuff: Below this line define 3rd party library settings
