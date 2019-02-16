from wtforms.fields import StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from wtforms.validators import StopValidation
from .base import BaseForm
from ..models import db, User
from ..auth import login


class ProfileForm(BaseForm):
    major = StringField()
    year = StringField()
    description = StringField()

    def save(self, email):
        user = User.query.filter_by(email=email).first()
        user.major = self.major.data
        user.year = self.year.data
        user.description = self.description.data
        with db.auto_commit():
            db.session.add(user)
        login(user, True)
        return user