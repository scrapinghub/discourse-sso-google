# Discourse SSO implementation with Google apps as auth provider

A webapp that sits in the middle of Discourse and Google Apps.

It implements Discourse SSO protocol and authenticates users via OAuth2 against
your Google Apps domain.

This is not another plugin implementing plugin to add social login for Discourse.

The advantages of SSO integration approach are described at
https://meta.discourse.org/t/official-single-sign-on-for-discourse-sso/13045

This is not better or worse than default social Google auth integration, it is
just different and for different purposes.


## Setup

1. Decide under what hostname are you going to run this application, be sure it
   is accessible under https.  For the sake of this example we will use
   `https://my.sso.app` for this app and `https://my.forum` for the Discourse
   forum location.

2. Register a new project and create credentials as describe at
   https://meta.discourse.org/t/configuring-google-login-for-discourse/15858,
   but do not update Discourse settings. We are going to use the OAuth2
   credentials in a different way.
   Set _Authorized Javascript Origins` to `https://my.sso.app` and
   _Authorized redirect URIs_ to ``https://my.sso.app/discourse/sso/google-oauth2/callback`

3. Set the following Discourse settings
   
   ```
   enable_sso = true
   sso_url = https://my.sso.app/discourse/sso
   sso_secret = YOUR_SSO_SECRET_KEY
   ```

4. Launch this webapp with the following settings

   ```python
   DISCOURSE_SECRET = 'YOUR_SSO_SECRET_KEY'
   DISCOURSE_SSO_LOGIN = 'https://my.forum/session/sso_login'
   GOOGLE_CLIENT_ID = 'The Client ID provided by Google in step 2'
   GOOGLE_SECRET = 'The secret provided by Google in step 2'
   GOOGLE_REDIRECT_URI = 'https://my.auth.app/discourse/sso/google-oauth2/callback'
   GOOGLE_DOMAIN = 'your-google-apps-domain.com'
   ```

5. That's all.
