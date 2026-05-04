from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-va^74$f6qqlo@@us((o*i($g2el5bog1=-s75fo-$a5(^i)ls='

# Detect if we're in development or production
# Set DJANGO_ENV=production on your production server
DJANGO_ENV = os.environ.get('DJANGO_ENV', 'development')

DEBUG = (DJANGO_ENV != 'production')

if DEBUG:
    # Development settings
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'ghandy.cloud', 'www.ghandy.cloud']
else:
    # Production settings
    ALLOWED_HOSTS = ['ghandy.cloud', 'www.ghandy.cloud']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'base',
    'item',
]


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


ROOT_URLCONF = 'ghandyStore.urls'


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
                'base.context_processors.cart',
            ],
        },
    },
]


WSGI_APPLICATION = 'ghandyStore.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ghandystore',
        'USER': 'JanaHero',
        'PASSWORD': 'StrongPassword123',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
        # 'ENGINE': 'django.db.backends.mysql',
        # 'NAME': 'ghandystore',
        # 'USER': 'root',
        # 'PASSWORD': '',
        # 'HOST': os.environ.get('MYSQL_HOST', '127.0.0.1'),
        # 'PORT': os.environ.get('MYSQL_PORT', '3306'),

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

if DEBUG:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
else:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
WHATSAPP_ORDER_NUMBER = os.environ.get('WHATSAPP_ORDER_NUMBER', '963937341881')
INSTAGRAM_URL = os.environ.get(
    'INSTAGRAM_URL',
    'https://www.instagram.com/_.ghandy._?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw==',
)

# SSL/Security settings - only enabled in production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
else:
    # Development: disable SSL redirects
    SECURE_SSL_REDIRECT = False
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False
