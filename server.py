import json 
import os 
import sqlite3
from flask import Flask, redirect, request, url_for
from flask_login import(
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests
from db import init_db_command
from user import User 

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = ("https://accounts.google.com/.well-known/openid-configuration")
SECRET_KEY = os.environ.get("SECRET_KEY", None)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# User session management setup
login_manager = LoginManager()
login_manager.init_app(app)

try:
    init_db_command()
except sqlite3.OperationalError:
    pass

#OAuth 2 CLient Setup 
client = WebApplicationClient(GOOGLE_CLIENT_ID)

#flask login helper to retrieve a user from the db 
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route("/")
def index():
    if current_user.is_authenticated:
        return(
             "<p>Hello, {}! You're logged in! Email: {}</p>"
            "<div><p>Google Profile Picture:</p>"
            '<img src="{}" alt="Google profile pic"></img></div>'
            '<a class="button" href="/logout">Logout</a>'.format(
                current_user.name, current_user.email, current_user.profile_pic
            )
        )
    else: 
        return '<a class="button" href="/login">Google Login</a>'
    
def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()
#add error handling ^ 

@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri) 

@app.route("/login/callback")
def callback():
    # Get authorization code from Google
    code = request.args.get("code")

    google_provider_cfg = get_google_provider_cfg()  # Corrected function call
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Retrieve user information
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.status_code != 200:
        return "Failed to fetch user info from Google", 500

    userinfo = userinfo_response.json()

    if userinfo.get("email_verified"):
        unique_id = userinfo["sub"]
        users_email = userinfo["email"]
        picture = userinfo["picture"]
        users_name = userinfo["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create user in DB if they don't exist
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture)

    user = User(unique_id, users_name, users_email, picture)
    login_user(user)

    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(ssl_context="adhoc")