"""Settings used to run tests."""

from base import *


## Test runner
# See: https://docs.djangoproject.com/en/1.5/ref/settings/#test-runner
TEST_RUNNER = '%s.settings.testrunner.NoseCoverageTestRunner' % SITE_NAME


# Use an in-memory sqlite database to speed up tests.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}


INSTALLED_APPS += (
    # django-nose
    'django_nose',
)


# Skip South migrations
SOUTH_TESTS_MIGRATE = False
