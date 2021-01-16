from .settings_common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS')]
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

STATIC_ROOT = '/usr/share/nginx/html/static'
MEDIA_ROOT = '/usr/share/nginx/html/media'

# AWS_SES_ACCESS_KEY_ID = os.environ.get('AWS_SES_ACCESS_KEY_ID')
# AWS_SES_SECRET_ACCESS_KEY = os.environ.get('AWS_SES_SECRET_ACCESS_KEY')

# メールバックエンド設定
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django_ses.SESBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# ロギング
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    # ロガー設定
    'loggers': {
        # django用ロガー
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
        },

        # アプリケーション用ロガー
        'order': {
            'handlers': ['file'],
            'level': 'INFO',
        },

        'accounts': {
            'handlers': ['file'],
            'level': 'INFO',
        },

        'cart': {
            'handlers': ['file'],
            'level': 'INFO',
        },

        'item': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    },

    # ハンドラ設定
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django.log'),
            'formatter': 'prod',
            'when': 'D',
            'interval': 1,
            'backupCount': 7,
        },
    },

    # フォーマッタ設定
    'formatters': {
        'prod': {
            'format': '\t'.join([
                '%(asctime)s',
                '[%(levelname)s]',
                '%(pathname)s(Line:%(lineno)d)',
                '%(message)s'
            ])
        },
    }
}

# セキュリティ関連設定
# security.W004
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# security.W006
SECURE_CONTENT_TYPE_NOSNIFF = True
# security.W007
SECURE_BROWSER_XSS_FILTER = True
# security.W008
SECURE_SSL_REDIRECT = True
# security.W012
SESSION_COOKIE_SECURE = True
# security.W016
CSRF_COOKIE_SECURE = True
# security.W019
X_FRAME_OPTIONS = 'DENY'
# security.W021
SECURE_HSTS_PRELOAD = True
