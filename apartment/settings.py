import os
from pathlib import Path
import dj_database_url

# -------------------------------
# Base Directory
# -------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------
# Secret Key (Safe default)
# -------------------------------
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-6_iezrvrparvw$epkyvl**trt2l0*$y!dt2&u+9$#gm0u0t5h&'
)

# -------------------------------
# DEBUG Mode (auto-detect)
# -------------------------------
_local_dev_env = os.environ.get('DJANGO_LOCAL_DEV')
if _local_dev_env is not None:
    DEBUG = _local_dev_env.lower() == 'true'
else:
    DEBUG = not bool(os.environ.get('RENDER'))  # Render sets RENDER=True automatically

# -------------------------------
# Allowed Hosts
# -------------------------------
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'apartment-p51r.onrender.com'
]

# -------------------------------
# Installed Apps
# -------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
]

# -------------------------------
# Middleware
# -------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# -------------------------------
# URL Config
# -------------------------------
ROOT_URLCONF = 'apartment.urls'

# -------------------------------
# Templates
# -------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# -------------------------------
# WSGI Application
# -------------------------------
WSGI_APPLICATION = 'apartment.wsgi.application'

# -------------------------------
# Database (Supabase PostgreSQL with Render fallback)
# -------------------------------
DATABASES = {
    'default': dj_database_url.config(
        default="postgresql://postgres.tvttwbifawwudymwnjpg:Cookie12345@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres",
        conn_max_age=600,
        ssl_require=not DEBUG  # only require SSL in production
    )
}

# -------------------------------
# Password Validators
# -------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# -------------------------------
# Internationalization
# -------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Manila'
USE_I18N = True
USE_TZ = True

# -------------------------------
# Static & Media Files
# -------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# -------------------------------
# Authentication Redirects
# -------------------------------
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# -------------------------------
# Security
# -------------------------------
if DEBUG:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    CSRF_TRUSTED_ORIGINS = []
else:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    CSRF_TRUSTED_ORIGINS = ['https://*.onrender.com']

# -------------------------------
# Default Primary Key Field Type
# -------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
