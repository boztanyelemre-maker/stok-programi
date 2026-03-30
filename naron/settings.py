import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# .env dosyasindan ortam degiskenlerini oku
_env_file = BASE_DIR / '.env'
if _env_file.exists():
    with open(_env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ.setdefault(key.strip(), value.strip())

SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-naron-stok-yonetim-sistemi-2024-secret-key-change-in-production',
)


def _env_bool(key: str, default: bool = False) -> bool:
    v = os.environ.get(key)
    if v is None:
        return default
    return v.lower() in ('true', '1', 'yes')


def _is_render() -> bool:
    """Render.com: RENDER veya RENDER_EXTERNAL_URL (biri yeter)."""
    return _env_bool('RENDER') or bool(os.environ.get('RENDER_EXTERNAL_URL'))


# Render'da varsayılan False; yerelde True
DEBUG = _env_bool('DEBUG', default=not _is_render())

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # Third party
    'crispy_forms',
    'crispy_bootstrap5',
    'django_filters',
    # Local apps
    'core',
    'accounts',
    'products',
    'stock',
    'orders',
    'assets',
    'assignments',
    'reports',
    'parameters',
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

# Render / üretim: statik dosyalar (collectstatic çıktısı)
if _is_render() or _env_bool('USE_WHITENOISE'):
    MIDDLEWARE = list(MIDDLEWARE)
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

ROOT_URLCONF = 'naron.urls'

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
                'core.context_processors.sidebar_menu',
            ],
        },
    },
]

WSGI_APPLICATION = 'naron.wsgi.application'

# Veritabani Ayarlari
# -------------------------------------------------------------------
# Varsayilan: SQLite (tasinabilir, sunucu gerektirmez)
# Sunucu moduna gecmek icin .env dosyasina asagidakileri ekleyin:
#   DB_ENGINE=django.db.backends.postgresql
#   DB_NAME=naron_db
#   DB_USER=postgres
#   DB_PASSWORD=sifreniz
#   DB_HOST=sunucu_ip
#   DB_PORT=5432
# PostgreSQL icin: pip install psycopg2-binary
# MySQL icin:      pip install mysqlclient
#   DB_ENGINE=django.db.backends.mysql
# -------------------------------------------------------------------
# Render / Railway vb.: DATABASE_URL otomatik gelir — öncelikli kullan.
if os.environ.get('DATABASE_URL'):
    import dj_database_url

    # Render iç PostgreSQL bazen sslmode ile gelir; sorun olursa env: DATABASE_SSL_REQUIRE=false
    _ssl = _env_bool('DATABASE_SSL_REQUIRE', default=True)
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600, ssl_require=_ssl)
    }
else:
    DB_ENGINE = os.environ.get('DB_ENGINE', 'django.db.backends.sqlite3')

    if DB_ENGINE == 'django.db.backends.sqlite3':
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': DB_ENGINE,
                'NAME': os.environ.get('DB_NAME', 'naron_db'),
                'USER': os.environ.get('DB_USER', 'postgres'),
                'PASSWORD': os.environ.get('DB_PASSWORD', ''),
                'HOST': os.environ.get('DB_HOST', 'localhost'),
                'PORT': os.environ.get('DB_PORT', '5432'),
                'OPTIONS': {},
            }
        }

AUTH_USER_MODEL = 'accounts.User'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'tr'
TIME_ZONE = 'Europe/Istanbul'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
if _is_render() or _env_bool('USE_WHITENOISE'):
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# HTTPS (Render)
if _is_render():
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

_csrf_origins = os.environ.get('CSRF_TRUSTED_ORIGINS', '').strip()
if _csrf_origins:
    CSRF_TRUSTED_ORIGINS = [x.strip() for x in _csrf_origins.split(',') if x.strip()]
elif os.environ.get('RENDER_EXTERNAL_URL'):
    CSRF_TRUSTED_ORIGINS = [os.environ['RENDER_EXTERNAL_URL'].rstrip('/')]
else:
    CSRF_TRUSTED_ORIGINS = []

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

LOGIN_URL = '/hesap/giris/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/hesap/giris/'

# Stok kritik miktar varsayilan
DEFAULT_CRITICAL_STOCK = 10
