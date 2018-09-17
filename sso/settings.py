import os

DISCOURSE_SECRET = os.getenv(
    'DISCOURSE_SECRET',
# Secret is for demo purpose and same published at
# https://meta.discourse.org/t/official-single-sign-on-for-discourse-sso/13045
    'd836444a9e4084d5b224a60c208dce14'
)
DISCOURSE_SSO_LOGIN = os.getenv(
    'DISCOURSE_SSO_LOGIN',
    'http://my-discourse-site/session/sso_login'
)

GOOGLE_AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_SECRET = os.getenv('GOOGLE_SECRET')
GOOGLE_REDIRECT_URI = os.getenv(
    'GOOGLE_REDIRECT_URI',
    'http://localhost:5000/discourse/sso/google-oauth2/callback'
)

try:
    from local_settings import *
except ImportError:
    pass
