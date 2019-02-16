from flask import Blueprint
from flask import url_for, redirect, render_template, request
from ..auth import current_user, logout as _logout
from ..auth import oauth
from ..forms.user import AuthenticateForm, UserCreationForm, AuthenticateGoogle
from google.oauth2 import id_token
from google.auth.transport import requests

bp = Blueprint('account', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user:
        return redirect(url_for('front.home'))
    form = AuthenticateForm()
    if form.validate_on_submit():
        form.login()
        return redirect(url_for('front.home'))
    return render_template('account/login.html', form=form)

@bp.route('/login/google', methods=['POST'])
def login_google():
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(request.form['idtoken'], requests.Request(), oauth._registry['google']['client_id'])

        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        # If auth request is from a G Suite domain:
        # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
        #     raise ValueError('Wrong hosted domain.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        sub = idinfo['sub'] #userid
        email = idinfo['email']
        name = idinfo['name']
        form = AuthenticateGoogle()
        form.validate_email(email, sub, name)
        form.login()
        return redirect(request.form['callback'])
    except ValueError:
        # Invalid token
        pass

@bp.route('/logout')
def logout():
    _logout()
    return redirect(url_for('front.home'))


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user:
        return redirect(url_for('front.home'))
    form = UserCreationForm()
    if form.validate_on_submit():
        form.signup()
        return redirect(url_for('front.home'))
    return render_template('account/signup.html', form=form)