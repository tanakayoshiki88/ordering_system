from .settings_common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


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
        # 自作アプリケーション全般のログを披露ロガー
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


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
