from authlib.flask.client import OAuth
from flask import Flask, redirect

app = Flask(__name__)
app.config.from_pyfile("app.cfg")
oauth = OAuth(app)
tok = ''


def save_request_token(token):
    global tok
    tok = token
    print(token)


def fetch_request_token():
    return tok


oauth.register(
    name='flickr',
    client_id=app.config['FLICKR_CLIENT_ID'],
    client_secret=app.config['FLICKR_CLIENT_SECRET'],
    request_token_url=app.config['FLICKR_REQUEST_TOKEN_URL'],
    request_token_params=app.config['FLICKR_REQUEST_TOKEN_PARAMS'],
    access_token_url=app.config['FLICKR_ACCESS_TOKEN_URL'],
    access_token_params=app.config['FLICKR_ACCESS_TOKEN_PARAMS'],
    authorize_url=app.config['FLICKR_AUTHORIZE_URL'],
    api_base_url=app.config['FLICKR_API_BASE_URL'],
    client_kwargs=app.config['FLICKR_CLIENT_KWARGS'],
    save_request_token=save_request_token,
    fetch_request_token=fetch_request_token,
)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/login")
def login():
    redirect_uri = "http://localhost:5000/authorize"
    return oauth.flickr.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    token = oauth.flickr.authorize_access_token()
    # this is a pseudo method, you need to implement it yourself
    tok = token
    print(token)
    return redirect("http://localhost:4200/")


@app.route('/profile')
def twitter_profile():
    resp = oauth.flickr.get('flickr.test.login')
    profile = resp.json()
    print(profile)


if __name__ == "__main__":
    app.run(debug=True)
