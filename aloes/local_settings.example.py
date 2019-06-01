"""Local settings"""

SECRET_KEY = 'Your secret key'

DEBUG = False

ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {

    }
}

TIME_ZONE = 'Europe/Paris'

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': '/var/backups/aloes/'}
