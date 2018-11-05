import os
from .base import *
DEBUG = True
ENVIRONMENT_NAME, _ = os.path.splitext(os.path.basename(os.path.abspath(__file__)))

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# RAVEN_CONFIG = {
#     'dsn': 'https://4496c0aab78046699ed016c80bcf1ab9:9064062e615443d1bf24ce1748cd87b7@sentry.io/1236089',
#     # If you are using git, you can also automatically configure the release based on the git info.
#     'release': raven.fetch_git_sha(BASE_DIR),
# }

MIDDLEWARE += [
    # 'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'vianifashion',
        'NAME': 'vianifashion$viani',
        'PASSWORD': config('PROD_DB_PASSWORD'),
        'HOST': 'vianifashion.mysql.pythonanywhere-services.com',
        'OPTIONS' : {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"}
        },
    }

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'