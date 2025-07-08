from pathlib import Path
import os # Ensure os is imported at the top
from django.core.exceptions import ImproperlyConfigured # Required for SECRET_KEY check
import dj_database_url # You'll need to install this: pip install dj-database-url


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Get SECRET_KEY from environment variable, provide a fallback for dev
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-jn@$9f=5w3!^)r#@-4pc#^8s0k5c#_^+-$)mtv(buy62mc=!$p') # Your current default key
if not SECRET_KEY:
    raise ImproperlyConfigured("The SECRET_KEY environment variable is not set.")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True' # Get DEBUG from env var

# ALLOWED_HOSTS for Docker compatibility
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0'] # Allow connections from within Docker


# Application definition

INSTALLED_APPS = [
    'teacher',
    'main',
    'student',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'sms.wsgi.application'


# Database configuration (adjust for PostgreSQL in Docker)
# We'll get database credentials from environment variables for flexibility
# and to avoid hardcoding sensitive info.

DATABASES = {
    'default': dj_database_url.config(
        # Use a default value if DATABASE_URL env var is not set
        # This is useful for local development outside Docker or for initial setup
        default='sqlite:///db.sqlite3', # Fallback to SQLite if DATABASE_URL is not found
        conn_max_age=600 # Optional: connection pool timeout
    )
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Collect static files here

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') # Where user-uploaded files will be stored

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'