from datetime import timedelta
import os
import sys
import yaml

####################################################################
## a little reflection...  alter settings based on on how
## Django is being invoked

SERVICE_NAME = 'tlsmd'

sys_argv_0 = sys.argv[0]
try:
    sys_argv_1 = sys.argv[1]
except IndexError:
    sys_argv_1 = ''

# assume development server mode
RUN_MODE = 'dev_server'
if sys_argv_0.find('gunicorn') != -1:
    RUN_MODE = 'gunicorn'
elif sys_argv_0.find('celery') != -1:
    if sys_argv_1.find('beat') != -1:
        RUN_MODE = 'celerybeat'
    else:
        RUN_MODE = 'celery'
elif sys_argv_1.lower() == 'test':
    RUN_MODE = 'test'

# the setting APPNAME is used for the application name in logging
APPNAME = {
    'dev_server': '{}_web'.format(SERVICE_NAME),
    'gunicorn': '{}_web'.format(SERVICE_NAME),
    'celery': '{}_cel'.format(SERVICE_NAME),
    'celerybeat': '{}_celb'.format(SERVICE_NAME),
    'test': 'test'
}[RUN_MODE]

####################################################################
## read and configure environment variables

TESTING = RUN_MODE == 'test'
SERVICE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
SERVICE_PARENT_DIR = os.path.dirname(SERVICE_ROOT)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'baseapp.settings')
DEBUG = os.environ.get('DEBUG', True)

####################################################################
## pull version information from webstack root

try:
    SERVICE_VERSION = open(os.path.join(SERVICE_ROOT, "VERSION.txt")).read().strip()
except IOError:
    SERVICE_VERSION = '0.0'

####################################################################
## load config

DATA_ROOT = os.path.join(SERVICE_ROOT, 'data')
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
REPORT_BASEURL = os.environ.get('ENTITY_BASEURL', 'http://localhost:8192/report')
REPORT_ROOT = os.environ.get('REPORT_ROOT', '/disk/d0/data/report')
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgres://postgres:password@localhost/tlsmd')
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'amqp://{service_name}_user:password@localhost:5672/{service_name}_vhost')

####################################################################
## database configuration

import dj_database_url
DATABASE_SETTIGS = dj_database_url.parse(DATABASE_URL)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DATABASE_SETTIGS.get('NAME'),
        'USER': DATABASE_SETTIGS.get('USER'),
        'PASSWORD': DATABASE_SETTIGS.get('PASSWORD'),
        'HOST': DATABASE_SETTIGS.get('HOST'),
        'PORT': DATABASE_SETTIGS.get('PORT'),
        'HAS_HSTORE': False,
        'OPTIONS': {
            'sslmode': 'disable'
        }
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
### if debug is false then this needs to be set to a host.
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = False

# Set the local path for the the application.
LOCALE_PATHS = ()

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(SERVICE_ROOT, 'static')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# UrL that handles the admin media
#ADMIN_MEDIA_DOCUMENT_ROOT = os.path.join(
#    os.path.dirname(django.__file__),
#    'contrib/admin/static/admin/')

# Additional locations of static files
STATICFILES_DIRS = [
]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
]

# Make this unique, and don't share it with anybody.
SECRET_KEY = '4u461le*-u*8_$vkkg_i_#53a0qu+&h5$kox7vju=25iq-1%8*'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'baseapp.urls'

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
                'baseapp.context_processors.service_settings'
            ],
        },
    },
]

WSGI_APPLICATION = 'baseapp.wsgi.application'

APPEND_SLASH = False

INSTALLED_APPS = (
    'baseapp',
    'tlsmdlib',
    'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    'django.contrib.postgres'
)

###### logging configuration

LOGGING_CONFIG_FILE = os.path.join(SERVICE_ROOT, 'etc', 'logging_prod.ini')
if DEBUG:
    LOGGING_CONFIG_FILE = os.path.join(SERVICE_ROOT, 'etc', 'logging_dev.ini')


###### Celery async task queue settings
## exapand service name service name
BROKER_URL = CELERY_BROKER_URL.format(service_name=SERVICE_NAME)
CELERY_RESULT_BACKEND = None

# serialization settings
import anyjson
anyjson.force_implementation('json')
CELERY_TASK_SERIALIZER = 'json'
CELERY_EVENT_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# task settings
CELERYD_PREFETCH_MULTIPLIER = 1
CELERY_TRACK_STARTED = True
CELERY_ENABLE_UTC = True

# define work queues
from kombu import Queue

CELERY_QUEUES = (
    Queue('baseapp', routing_key='baseapp.#'),
)

CELERY_DEFAULT_QUEUE = 'baseapp'
CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'
CELERY_DEFAULT_ROUTING_KEY = 'baseapp.default'

CELERY_ROUTES = {
#    'tlsmd.add_video_url': dict(routing_key='baseapp.default'),
}


###### Celery-Beat periodic task submission settings

from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    'heartbeat-1minute': {
        'task': 'baseapp.healthcheck_task',
        'schedule': crontab(),  # run health check every 60 seconds
        'options': {'expires': 70}  # expire the health check job after 70 seconds
    }
}


###### Django REST Framework Settings

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('baseapp.permissions.InternalOrIsAuthenticated', ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 30
}

###### Session configuration

_one_year_seconds_seconds = 60 * 60 * 24 * 365
SESSION_COOKIE_AGE = _one_year_seconds_seconds
SESSION_COOKIE_HTTPONLY = False
SESSION_COOKIE_NAME = 'tlsmd_sessionid'
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
