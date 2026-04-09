from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-u$#upa)*hm6um%sd$l6qu%gl5lkm9t1jwcgogo&(k_f=o07w$l'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'apps.users.apps.UsersConfig',
    'apps.brevets',
    'apps.documents',
    'apps.paiements',
    'apps.recours',
    'apps.notifications',
    'apps.dashboards',

    'rest_framework',
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Algiers'

USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.Utilisateur'

JAZZMIN_SETTINGS = {
    "site_title": "Gestion des Brevets",
    "site_header": "Administration Brevets",
    "site_brand": "Gestion des Brevets",
    "site_logo": "images/logo-sonatrach.jpg",
    "theme": "darkly",
    "default_theme_mode": "dark",
    "show_ui_builder": False,
    "navigation_expanded": True,
    "order_with_respect_to": [
        "dashboard",
        "brevets",
        "inventeurs",
        "deposants",
        "documents",
        "paiements",
        "recours",
        "notifications",
        "users",
        "auth",
    ],
    "icons": {
        "auth": "fas fa-users-cog",
        "users.Utilisateur": "fas fa-user",
        "users.Role": "fas fa-user-tag",
        "brevets": "fas fa-folder",
        "brevets.Brevet": "fas fa-lightbulb",
        "brevets.DemandeBrevet": "fas fa-file-alt",
        "inventeurs.Inventeur": "fas fa-user-astronaut",
        "deposants.Deposant": "fas fa-user-tie",
        "documents": "fas fa-folder-open",
        "documents.Document": "fas fa-file",
        "documents.TypeDocument": "fas fa-file-medical",
        "paiements": "fas fa-credit-card",
        "paiements.Paiement": "fas fa-money-bill-wave",
        "notifications": "fas fa-bell",
        "notifications.Notification": "fas fa-bell",
        "recours": "fas fa-balance-scale",
        "recours.Recours": "fas fa-gavel",
        "dashboard": "fas fa-chart-line",
    }
}

JAZZMIN_UI_TWEAKS = {
    "navbar": "navbar-dark",
    "brand_colour": "navbar-primary",
    "accent": "accent-info",
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "dark_mode_theme": "darkly",
}