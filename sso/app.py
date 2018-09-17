import json
import hmac
import base64
import hashlib

from six.moves import urllib

import jwt
from flask import Flask, request, abort, redirect, render_template

from . import settings

app = Flask(__name__.split('.')[0])


@app.route('/discourse/sso')
def sso_login():
    encoded_payload = request.args.get('sso', '').encode('ascii')
    signature = request.args.get('sig', '').encode('ascii')
    if signature != _sign_payload(encoded_payload):
        abort(400)

    # Validate payload is base64 encoded
    try:
        payload = urllib.parse.parse_qs(
            base64.urlsafe_b64decode(encoded_payload)
        )
    except ValueError:
        abort(400)

    state = jwt.encode(payload, settings.DISCOURSE_SECRET, 'HS256')

    query = urllib.parse.urlencode({
        'client_id': settings.GOOGLE_CLIENT_ID,
        'redirect_uri': settings.GOOGLE_REDIRECT_URI,
        'response_type': 'token',
        'scope': 'profile email',
        'state': state,
    })
    url = '{}?{}'.format(settings.GOOGLE_AUTH_URL, query)
    return url + "\n"


@app.route('/discourse/sso/google-oauth2/callback')
def google_oauth2_callback():
    return render_template('google-oauth2-callback.html')


@app.route('/discourse/sso/google-oauth2/next', methods=['POST'])
def google_oauth2_next():
    state = request.form.get('state')
    userinfo = request.form.get('userInfo')
    if not (state and userinfo):
        abort(400)

    payload = jwt.decode(state, settings.DISCOURSE_SECRET, algorithms=['HS256'])
    userinfo = json.loads(userinfo)

    payload['external_id'] = userinfo['sub']
    payload['name'] = userinfo['name'].encode('utf-8')
    payload['email'] = userinfo['email']
    payload['username'] = userinfo['email'].partition('@')[0]
    payload['avatar_url'] = userinfo['picture']

    encoded_payload = base64.urlsafe_b64encode(urllib.parse.urlencode(payload))
    signature = _sign_payload(encoded_payload)
    qs = urllib.parse.urlencode({'sso': encoded_payload, 'sig': signature})
    return redirect(settings.DISCOURSE_SSO_LOGIN + "?" + qs)


@app.after_request
def apply_caching(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response


def _sign_payload(payload, secret=settings.DISCOURSE_SECRET):
    return hmac.new(
        secret, 
        msg=payload, 
        digestmod=hashlib.sha256
    ).hexdigest()


