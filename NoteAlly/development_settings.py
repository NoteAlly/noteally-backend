from .settings import * #NOSONAR


DEBUG = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3'
    }
}

# MEDIA_URL = 'media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# STORAGES = {
#     "default": {
#         "BACKEND": "django.core.files.storage.FileSystemStorage",
#         "OPTIONS": {
#             "location": MEDIA_URL
#         },
#     },
#     "staticfiles": {
#         "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
#         "OPTIONS": {
#             "location": STATIC_URL
#         },
#     },
# }


STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": AWS_ACCESS_KEY_ID,
            "secret_key": AWS_SECRET_ACCESS_KEY,
            "bucket_name": AWS_S3_BUCKET_NAME,
            "region_name": AWS_REGION_NAME,
            "custom_domain": AWS_S3_CUSTOM_DOMAIN,
            "object_parameters": AWS_S3_OBJECT_PARAMETERS,
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        "OPTIONS": {
            "location": 'static/',
            "base_url": "/static/"
        },
    },
}
