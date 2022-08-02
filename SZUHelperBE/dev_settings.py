from pathlib import Path

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ie_3l1+mqo^cmcvnk3f+0w_j1ct&fsof0ll3cq6!7l2h6y2q)q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
    },
}

INTERNAL_IPS = [
    '127.0.0.1',
]
