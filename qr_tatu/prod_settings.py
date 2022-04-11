import os.path
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+=af3i7_)ze1p^d)1(%3622t@2ubkewcug1grhlzxks9x_(c&1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']




# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'QrTatu_db',
        'USER': 'qr_admindb',
        'PASSWORD':'qdwg12rfsd5^12%',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}


STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_DIR = os.path.join(BASE_DIR, 'static')

STATICFIELS_DIRS = (
    [STATIC_DIR],
     )