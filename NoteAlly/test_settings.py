from .settings import * #NOSONAR


DEBUG = True

CORS_ORIGIN_ALLOW_ALL = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test_db.sqlite3'
    }
}


STATIC_URL = 'test_static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'test_static')

MEDIA_URL = 'test_media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'test_media')

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {
            "location": MEDIA_URL
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        "OPTIONS": {
            "location": STATIC_URL
        },
    },
}
