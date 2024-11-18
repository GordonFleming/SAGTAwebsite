from .base import *

import ast
import os

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {},
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = os.getenv("DEBUG")
WAGTAIL_SITE_NAME = os.environ.get("SITE_NAME")
HTTP_PORT = os.environ.get("HTTP_PORT")
ALLOWED_HOSTS = ["{}".format(WAGTAIL_SITE_NAME), "www.{}".format(WAGTAIL_SITE_NAME)]
DATABASES["default"]["NAME"] = os.environ.get(
    "SQLITE_LOCATION", DATABASES["default"]["NAME"]
)

try:
    from .local import *
except ImportError:
    pass
