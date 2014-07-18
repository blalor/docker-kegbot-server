# Kegbot local settings.
# Safe to edit by hand. See http://kegbot.org/docs/server/ for more info.

import os

# NEVER set DEBUG to `True` in production.
## set KEGBOT_DEBUG to a non-empty string
DEBUG = bool(os.environ.get("KEGBOT_DEBUG", ""))
TEMPLATE_DEBUG = DEBUG

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "/var/log/kegbot/kegbot.log",
        },
    },
    "loggers": {
        "root": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "OPTIONS": {
            "init_command": "SET storage_engine=INNODB"
        },
        
        "NAME":     os.environ["KEGBOT_DB_NAME"],
        "HOST":     os.environ["KEGBOT_DB_HOST"],
        "USER":     os.environ["KEGBOT_DB_USER"],
        "PASSWORD": os.environ["KEGBOT_DB_PASSWORD"],
    }
}

KEGBOT_ROOT = "/var/lib/kegbot"
MEDIA_ROOT  = KEGBOT_ROOT + "/media"
STATIC_ROOT = KEGBOT_ROOT + "/static"

MEDIA_URL  = "/media/"
STATIC_URL = "/static/"

SECRET_KEY = "d7wz4m5qeomw8oh6-!y-1vf+6)0*!zcc53$f2c8tlmulgg!t^$"

if "KEGBOT_EMAIL_HOST" in os.environ:
    # Tell Kegbot use the SMTP e-mail backend.
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

    # "From" address for e-mails.
    EMAIL_FROM_ADDRESS = os.environ["KEGBOT_EMAIL_FROM"]

    EMAIL_HOST = os.environ["KEGBOT_EMAIL_HOST"]
    EMAIL_PORT = int(os.environ.get("KEGBOT_EMAIL_PORT", 25))

    # Credentials for SMTP server.
    if "KEGBOT_EMAIL_USER" in os.environ:
        EMAIL_HOST_USER     = os.environ["KEGBOT_EMAIL_USER"]
        EMAIL_HOST_PASSWORD = os.environ["KEGBOT_EMAIL_PASSWORD"]
    
    EMAIL_USE_SSL       = bool(os.environ.get("KEGBOT_EMAIL_USE_SSL", ""))
    EMAIL_USE_TLS       = bool(os.environ.get("KEGBOT_EMAIL_USE_TLS", ""))
