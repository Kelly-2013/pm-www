"""Settings used in the production environment."""

import os

from memcacheify import memcacheify
from postgresify import postgresify
from boto.s3.connection import ProtocolIndependentOrdinaryCallingFormat

from base import *


## Email configuration
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-password
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'your_email@example.com')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = os.environ.get('EMAIL_PORT', 587)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-use-tls
EMAIL_USE_TLS = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = EMAIL_HOST_USER


## Database configuration
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = postgresify()


## Cache configuration
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
if CACHES is None:
    CACHES = dict()
CACHES.update(memcacheify())


## Secret key configuration
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Use the value set in the Heroku configuration.
SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)


## Gunicorn configuration
# See: http://gunicorn.org/run.html
# See: https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/gunicorn/
INSTALLED_APPS += (
    'gunicorn',
)


## django-storages and AWS configuration
# See: http://django-storages.readthedocs.org/en/latest/index.html
# See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings

INSTALLED_APPS += (
    'storages',
)

# The following values should be set via `heroku config'.
# Values are based on the ones found here:
# http://balzerg.blogspot.com/2012/09/staticfiles-on-heroku-with-django.html
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_S3_CALLING_FORMAT = ProtocolIndependentOrdinaryCallingFormat()
AWS_QUERYSTRING_AUTH = False


## Static files configuration
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
# Serve static content out of S3.
STATIC_URL = '//s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATICFILES_STORAGE = '%s.storage.S3PipelineStorage' % SITE_NAME


## Template configuration
# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
if not DEBUG:
    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )),
    )


## Raven / Sentry configuration
# See: https://www.getsentry.com/docs/python/django/
# See: http://raven.readthedocs.org/en/latest/config/django.html
INSTALLED_APPS += (
    'raven.contrib.django',
)

SENTRY_DSN = os.environ.get('SENTRY_DSN')

SENTRY_LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

# Augment the existing LOGGING configuration.
if LOGGING is None:
    LOGGING = dict()
LOGGING.update(SENTRY_LOGGING)

# The documenation recommend placing Sentry middleware as high as possible.
MIDDLEWARE_CLASSES = (
    'raven.contrib.django.middleware.SentryResponseErrorIdMiddleware',
    'raven.contrib.django.middleware.SentryLogMiddleware',
) + MIDDLEWARE_CLASSES