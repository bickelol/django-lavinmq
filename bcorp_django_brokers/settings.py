from pathlib import Path
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
import os, environ
import sentry_sdk, logging


# Initialiser le chemin de base du projet
BASE_DIR = Path(__file__).resolve().parent.parent

# Configurer les hôtes autorisés
ALLOWED_HOSTS = ['*']

# Initialiser les variables d'environnement
env = environ.Env(
    DEBUG=(bool, False)
)

# Vérifier si le fichier .env existe
if Path(".env").exists():
    env_file = str(BASE_DIR / ".env")
else:
    env_file = str(BASE_DIR / "bcorp_django_brokers/config/env_production")

# Charger les variables d'environnement
environ.Env.read_env(env_file)

# Configuration de DEBUG
DEBUG = env('DEBUG')

# Clé secrète pour la sécurité
SECRET_KEY = env('SECRET_KEY')

# Nom de l'environnement
ENV_NAME = env('ENV_NAME')


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'notify.apps.NotifyConfig',
    'django_tasks'
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

ROOT_URLCONF = 'bcorp_django_brokers.urls'

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

WSGI_APPLICATION = 'bcorp_django_brokers.wsgi.application'

#TASKS = {
#    'default': {
#        'BACKEND': 'django_tasks.backends.database.DatabaseBackend',
#    },
#}

#TASKS = {
#    "default": {"BACKEND": "django.tasks.backends.immediate.ImmediateBackend"}
#}

LAVINMQ_URL = 'amqp://guest:guest@localhost:5672//'

REDPANDA_CONFIG = {
    'bootstrap.servers': 'localhost:9092',  # Change to your Redpanda address
    # Add SASL configurations here if using Redpanda Cloud
    # 'security.protocol': 'SASL_SSL',
    # 'sasl.mechanism': 'SCRAM-SHA-256',
    # 'sasl.username': 'my_user',
    # 'sasl.password': 'my_password',
}

REDPANDA_TOPICS = {
    'redpanda_notifications': 'redpanda-notifications-topic',
}


if ENV_NAME in ["production"]:
    DATABASES = {"default": env.db("MAIN_DATABASE_URL")}
else:
    DATABASES = {
        'default': env.db("MAIN_DATABASE_URL"),
    }

""" DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
} """

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


# Configuration de la langue et du fuseau horaire
LANGUAGE_CODE = 'en'
TIME_ZONE = 'Africa/Porto-Novo'

# USE_I18N = True
USE_L10N = False  # Ajout pour localiser les formats de date, de nombre, etc.
USE_TZ = True
DATE_FORMAT = 'Y-m-d'

# Configuration de l'auto-incrémentation
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuration des fichiers statiques
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static_src"),)

if ENV_NAME == "production":
    STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

# Configuration des fichiers médias
MEDIA_URL = "/media/"
if (ENV_NAME == "production"):
    MEDIA_ROOT = "/home/media_files/apps_media/MITC/mitc-features-media"
else:
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Configuration de la gestion des sessions
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Pour supprimer la session à la fermeture du navigateur
SESSION_COOKIE_AGE = 60 * 30  # Durée de la session (en secondes)
SESSION_LENGTH_REMEMBER_ME = 24 * 60 * 60  # Durée de la session pour "Se souvenir de moi"

DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 5
FILE_UPLOAD_MAX_MEMORY_SIZE = DATA_UPLOAD_MAX_MEMORY_SIZE

# Configuration de l'envoi d'e-mails
'''
if ENV_NAME != "development":
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "live.smtp.mailtrap.io"
    EMAIL_PORT = 587
    EMAIL_HOST_USER = "api"
    EMAIL_HOST_PASSWORD = env("MAILTRAP_PASSWORD")
    EMAIL_USE_TLS = True
'''

# Configuration de AWS S3 (pour le stockage de fichiers)
AWS_ACCESS_KEY_ID = env('BNB_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('BNB_AWS_SECRET_ACCESS_KEY')
AWS_S3_REGION_NAME = env('BNB_AWS_S3_REGION_NAME')
AWS_STORAGE_BUCKET_NAME = env('BNB_AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_DEFAULT_ACL = 'public-read'

GLITCHTIP_DSN = env('GLITCHTIP_DSN')

def before_send_debug(event, hint):
    """Callback pour logger chaque événement avant envoi"""
    import logging
    logger = logging.getLogger('sentry_debug')
    logger.info(f"📤 SENTRY EVENT: {event.get('event_id', 'N/A')[:8]}")
    logger.info(f"   Level: {event.get('level')}")
    logger.info(f"   Message: {event.get('message', 'N/A')[:200]}")
    logger.info(f"   Environment: {event.get('tags', {}).get('environment')}")

    # Optionnel: logger le début de la stack trace
    if 'exception' in event:
        exc = event['exception']['values'][0]
        logger.info(f"   Exception: {exc.get('type')}: {exc.get('value')[:100]}")

    return event  # ← Important: retourner l'événement pour qu'il soit envoyé



if ENV_NAME != "development":
    #if GLITCHTIP_DSN:
    sentry_sdk.init(
        dsn=GLITCHTIP_DSN,
        integrations=[
            DjangoIntegration(),
            LoggingIntegration(
                level=logging.INFO,        # Capture info et +
                event_level=logging.ERROR  # Envoyer errors comme événements
            ),
        ],
        traces_sample_rate=0.1 if ENV_NAME == "production" else 1.0,  # 10% en production
        send_default_pii=ENV_NAME != "production",
        environment=ENV_NAME,
        release=os.environ.get("VERSION", "1.0"),

         #before_send=before_send_debug,  # ← Ajoutez cette ligne
         debug=True,

        # Tags globaux
        _experiments={
            "profiles_sample_rate": 0.1,
        },
    )
