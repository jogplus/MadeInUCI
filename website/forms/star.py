from wtforms.fields import IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from wtforms.validators import StopValidation
from .base import BaseForm
from ..models import db, User, Star
from ..auth import login


class StarForm(BaseForm):
    projectid = IntegerField()

    def save(self, email):
        user = User.query.filter_by(email=email).first()
        prevousStar = Star.query.filter_by(userid=user.id, projectid=self.projectid.data).first():

        if prevousStar:
            # Star didn't exist
            db.session.delete(prevousStar)
        else:
            # Star didn't exist
            star = Star()
            star.userId = user.id
            star.projectid = self.projectid
            db.session.add(star)

        db.session.commit
        return self.projectid
