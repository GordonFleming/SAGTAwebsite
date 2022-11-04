from .base import *

import ast
import os

SECRET_KEY = os.environ.get("SECRET_KEY")

# Recaptcha settings
RECAPTCHA_PUBLIC_KEY = "6LfOaOsUAAAAAOo7jXLW5wTwN2LO3iM8Tz49wVGZ"
RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_PRIVATE_KEY")
NOCAPTCHA = True

DEBUG = os.getenv("DJANGO_DEBUG", "off") == "on"
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
