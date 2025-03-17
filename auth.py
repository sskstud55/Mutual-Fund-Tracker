from flask import redirect, session, request, url_for
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

CLIENT_SECRETS_FILE = "client_secret.json"  # Each user must provide their own Google OAuth credentials
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/userinfo.email", "openid"]
REDIRECT_URI = "http://localhost:5000/auth/callback"

def get_google_auth_url():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    flow.redirect_uri = REDIRECT_URI
    auth_url, _ = flow.authorization_url(prompt="consent")
    return auth_url

def get_google_user():
    """Retrieve user details after Google login."""
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    flow.redirect_uri = REDIRECT_URI
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials
    user_info_service = googleapiclient.discovery.build("oauth2", "v2", credentials=credentials)
    user_info = user_info_service.userinfo().get().execute()

    session["email"] = user_info["email"]
    session["name"] = user_info["name"]
    session["credentials"] = credentials_to_dict(credentials)

def credentials_to_dict(credentials):
    return {"token": credentials.token, "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri, "client_id": credentials.client_id,
            "client_secret": credentials.client_secret, "scopes": credentials.scopes}

def login_required(f):
    """Decorator to require login."""
    def decorated_function(*args, **kwargs):
        if "email" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function
