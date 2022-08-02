import os
from pathlib import Path

DEBUG = False
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
DATA_DIR = BASE_DIR / 'data'

with open(os.path.join(DATA_DIR, 'config', 'secret.key'), 'r') as f:
    SECRET_KEY = f.read()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.getenv('DB_HOST', default='eahelper-postgres'),
        'PORT': os.getenv('DB_PORT', default='5432'),
        'NAME': os.getenv('DB_NAME', default='eahelper'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
    }
}

REDIS_CONF = {
    'host': os.getenv('REDIS_HOST', default='eahelper-redis'),
    'port': os.getenv('REDIS_PORT', default='6379'),
}

REDIS_URL = 'redis://%s:%s' % (REDIS_CONF['host'], REDIS_CONF['port'])

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'{REDIS_URL}/0',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'IGNORE_EXCEPTIONS': True,
            # 'CONNECTION_POOL_KWARGS': {'decode_responses': True},
        }
    },
}