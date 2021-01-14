from .settings_common import *

import os

# local_settings.pyからSECRET_KEYを読み込み
try:
    from .local_settings import *
except ImportError:
    pass

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# メールバックエンド設定
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django_ses.SESBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# ロギング設定

LOGGING = {
    # バージョンは「1」固定
    'version': 1,

    # 既存のログ設定を無効化しない
    'disable_existing_loggers': False,

    # ログフォーマット
    'formatters': {
        # 開発用
        'develop': {
            'format': '%(asctime)s [%(levelname)s] %(pathname)s:%(lineno)d '
                      '%(message)s'
        },
    },

    # ハンドラ
    'handlers': {
        # コンソール出力用ハンドラ
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'develop',
        },
    },

    # ロガー
    'loggers': {
        # 自作アプリケーション全般のログを拾うロガー
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },

        # Django本体が出すログ全般を拾うロガー
        'django': {
            'handler': ['console'],
            'level': 'INFO',
            'propagate': False,
        },

        # 発行される SQL 文を出力するための設定
        'django.db.backends': {
            'handler': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
