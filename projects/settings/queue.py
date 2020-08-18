import os

# Redis Queues
# =============================================================================

RQ_QUEUES = {
    'default': {
        'DEFAULT_TIMEOUT': 180,
        'URL': os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/1'),
    },
    'high': {
        'DEFAULT_TIMEOUT': 360,
        # 'PASSWORD': 'some-password',
        'HOST': '127.0.0.1',
        'PORT': 6379,
        'DB': 1,
    },
    'low': {
        'DEFAULT_TIMEOUT': 500,
        'HOST': '127.0.0.1',
        'PORT': 6379,
        'DB': 1,
    }
}

# If you need custom exception handlers
# RQ_EXCEPTION_HANDLERS = ['path.to.my.handler']
