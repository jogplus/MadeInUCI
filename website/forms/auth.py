from wtforms.fields import (
    PasswordField,
    BooleanField,
    StringField,
)
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from wtforms.validators import StopValidation
from .base import BaseForm
from ..models import db, User
from ..auth import login
from ..auth import oauth

from google.oauth2 import id_token
from google.auth.transport import requests


# class ConfirmForm(BaseForm):
#     confirm = BooleanField()


class LoginConfirmForm(BaseForm):
    email = EmailField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])

    def validate_password(self, field):
        email = self.email.data.lower()
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(field.data):
            raise StopValidation('Email or password is invalid.')

        login(user, False)

class AuthenticateGoogle(BaseForm):
    email = EmailField()
    id = StringField()
    name = StringField()

    def validate_id(self, field):
        try:
            idinfo = id_token.verify_oauth2_token(self.id.data, requests.Request(), oauth._registry['google']['client_id'])
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
        except ValueError:
            # Invalid token
            pass

    def validate_email(self, field):
        if not field.data:
            raise ValueError('No email.')
        email = field.data.lower()
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(name=self.name.data, email=email)
            with db.auto_commit():
                db.session.add(user)
        login(user, False)