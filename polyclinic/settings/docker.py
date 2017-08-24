# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import environ
from django.conf import global_settings
from .base import *

env = environ.Env(
    DEBUG=(bool, False),
    EMAIL_FROM=(str, global_settings.DEFAULT_FROM_EMAIL),
    ADMINS=(list, []),
    MANAGERS=(list, []),
)

DEBUG = env('DEBUG')

ADMINS = [(i.split('@')[0], i) for i in env('ADMINS')]

MANAGERS = [(i.split('@')[0], i) for i in env('MANAGERS')]

ALLOWED_HOSTS = '*'

DATABASES['default'].update(env.db(default='sqlite:///%s' % DATABASES['default']['NAME']))

SECRET_KEY = env('SECRET_KEY')

EMAIL_CONFIG = env.email_url(default='consolemail://')
DEFAULT_FROM_EMAIL = SERVER_EMAIL = env('EMAIL_FROM')
vars().update(EMAIL_CONFIG)