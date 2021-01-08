from .settings_common import *

DEBUG = False

ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS')]

STATIC_ROOT = '/usr/share/nginx/html/static'
MEDIA_ROOT = '/usr/share/nginx/html/media'

AWS_SES_ACCESS_KEY_ID = os.environ.get('AWS_SES_ACCESS_KEY_ID')
AWS_SES_SECRET_ACCESS_KEY_ID = os.environ.get('AWS_SES_SECRET_ACCESS_KEY_ID')

EMAIL_BACKEND = 'django_ses.SESBackend'

# ロギング
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    # ロガー設定
    'loggers': {
        # django用ロガー
        'django': {
            'handlers': ['file'],
            'level': 'INFO'
        },

        # アプリケーション用ロガー
        'order': {
            'handlers': ['file'],
            'level': 'INFO'
        },

        'accounts': {
            'handlers': ['file'],
            'level': 'INFO'
        },

        'cart': {
            'handlers': ['file'],
            'level': 'INFO'
        },

        'item': {
            'handlers': ['file'],
            'level': 'INFO'
        },
    },

    # ハンドラ設定
    'handlers': {
        'level': 'INFO',
        'class': 'Logging.handlers.TimedRotatingFileHandler',
        'filename': os.path.join(BASE_DIR, 'logs/django.log'),
        'formatter': 'prod',
        'when': 'D',
        'interval': 1,
        'backupCount': 7,
    },

    # フォーマッタ設定
    'formatters': {
        'prod': {
            'format': '\t'.join([
                '%(asctime)s',
                '[%(levelname)s',
                '%(pathname)s(Line:%(lineno)d',
                '%(message)s',
            ])
        },
    }
}
