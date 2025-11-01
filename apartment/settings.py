import os
from pathlib import Path
import dj_database_url
import socket

# -------------------------------
# Base Directory
# -------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------
# Auto-create .env file if it doesn't exist
# -------------------------------
ENV_FILE = BASE_DIR / '.env'
if not ENV_FILE.exists():
    # Create .env file with default Gmail configuration
    env_content = """# Gmail SMTP Configuration
EMAIL_HOST_USER=kinggucci195@gmail.com
EMAIL_HOST_PASSWORD=zrleapbqomopgbbi
DEFAULT_FROM_EMAIL=kinggucci195@gmail.com
"""
    try:
        ENV_FILE.write_text(env_content, encoding='utf-8')
        print(f"[OK] Created .env file at {ENV_FILE}")
    except Exception as e:
        print(f"[WARNING] Could not create .env file: {e}")

# Load environment variables from .env file (if python-dotenv is installed)
try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=ENV_FILE)
    # .env file loaded successfully
except ImportError:
    # python-dotenv not installed, using manual .env loading
    # Manually load .env file if python-dotenv is not available
    if ENV_FILE.exists():
        try:
            with open(ENV_FILE, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ.setdefault(key.strip(), value.strip())
            # Manually loaded .env file successfully
        except Exception as e:
            print(f"[WARNING] Could not manually load .env: {e}")
except Exception as e:
    print(f"[WARNING] Error loading .env file: {e}")

# Fallback: Try loading from system environment if .env doesn't have values
if not os.environ.get("EMAIL_HOST_USER"):
    os.environ.setdefault("EMAIL_HOST_USER", "kinggucci195@gmail.com")
if not os.environ.get("EMAIL_HOST_PASSWORD"):
    os.environ.setdefault("EMAIL_HOST_PASSWORD", "zrleapbqomopgbbi")
if not os.environ.get("DEFAULT_FROM_EMAIL"):
    os.environ.setdefault("DEFAULT_FROM_EMAIL", "kinggucci195@gmail.com")

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
    DEBUG = not bool(os.environ.get('RENDER'))

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
    'corsheaders',  # CORS support for Next.js frontend
    'accounts',
    'rest_framework',
]

# -------------------------------
# Middleware
# -------------------------------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # CORS middleware (must be at the top)
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ✅ Static PWA support
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
# Database (Supabase online / SQLite offline)
# -------------------------------
try:
    socket.gethostbyname('aws-1-ap-southeast-1.pooler.supabase.com')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'HOST': 'aws-1-ap-southeast-1.pooler.supabase.com',
            'NAME': 'postgres',
            'USER': 'postgres.tvttwbifawwudymwnjpg',
            'PASSWORD': 'Cookie12345',
            'PORT': '5432',
        }
    }
    print("[OK] Using Supabase PostgreSQL (online mode)")
except socket.gaierror:
    print("[INFO] Offline mode: using SQLite fallback")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'offline.sqlite3',
        }
    }

# -------------------------------
# Password Validators
# -------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
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

STATICFILES_DIRS = [
    BASE_DIR / 'static',
    BASE_DIR / 'accounts/static',  # ✅ Added so PWA files are collected
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ✅ Offline support for PWA
OFFLINE_URL = '/offline.html'

# -------------------------------
# Authentication Redirects
# -------------------------------
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# -------------------------------
# Security Settings
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
    CSRF_TRUSTED_ORIGINS = [
        'https://apartment-p51r.onrender.com',
        'https://*.onrender.com'
    ]

# -------------------------------
# Default Primary Key Field Type
# -------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -------------------------------
# Django REST Framework settings
# -------------------------------
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

# -------------------------------
# CORS Settings for Next.js Frontend
# -------------------------------
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://apartment-p51r.onrender.com",
]

# Allow credentials (cookies, authorization headers) if needed
CORS_ALLOW_CREDENTIALS = True

# -------------------------------
# Email Configuration (Gmail SMTP)
# -------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True").lower() == "true"
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "kinggucci195@gmail.com")
# Process app password - remove spaces and trim
raw_password = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_HOST_PASSWORD = raw_password.replace(" ", "").strip() if raw_password else ""
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)

# Validate email configuration
if not EMAIL_HOST_USER or not EMAIL_HOST_PASSWORD:
    print("[WARNING] EMAIL_HOST_USER or EMAIL_HOST_PASSWORD not set. Email sending will fail.")
else:
    # Only log that email is configured, don't log the password
    print(f"[OK] Email configured: {EMAIL_HOST_USER}")

# Rate limiting for password reset requests (per IP)
PASSWORD_RESET_RATE_LIMIT = 3  # Max requests per hour
PASSWORD_RESET_RATE_WINDOW = 3600  # 1 hour in seconds
