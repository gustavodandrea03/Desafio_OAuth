from flask import Flask, redirect, url_for, session, request
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os

load_dotenv()  

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'SECRET_KEY')

oauth = OAuth(app)
github = oauth.register(
    name='github',
    client_id=os.getenv('CLIENT ID'),
    client_secret=os.getenv('CLIENT SECRET'),
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri=None,
    client_kwargs={'scope': 'user:email'},
)


@app.route('/')
def index():
    return 'Bem-vindo! <a href="/login">Entrar no GitHub</a>'

@app.route('/login')
def login():
    redirect_uri = url_for('authorized', _external=True)
    return github.authorize_redirect(redirect_uri)

@app.route('/logout')
def logout():
    session.pop('token', None)
    return redirect('/')

@app.route('/login/authorized')
def authorized():
    token = github.authorize_access_token()
    resp = github.get('user', token=token)
    user_info = resp.json()
    session['user'] = user_info
    return f"Logged in as: {user_info['login']}"


if __name__ == '__main__':
    app.run(debug=True)
