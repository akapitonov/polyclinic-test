from .base import *


SECRET_KEY = 'pv+n#hlapql2t(hdm2==#k^f*fre*2xxeva6nl!jf901$822e4'


DEBUG = True

TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

ALLOWED_HOSTS = '*'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

try:
    from .local import *
except ImportError:
    pass
