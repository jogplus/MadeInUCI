from wtforms.fields import StringField, PasswordField, DateTimeField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from wtforms.validators import StopValidation
from .base import BaseForm
from ..models import db, User, Project
from ..auth import login


class ProjectForm(BaseForm):
    title = StringField()
    picture = StringField()
    url = StringField()
    description = StringField()
    start_date = DateTimeField()
    duration = StringField()

    def save(self, email):
        user = User.query.filter_by(email=email).first()
        project = Project(title=self.title.data)
        project.userid = user.id
        project.picture = self.picture.data
        project.description = self.description.data
        project.start_date = self.start_date.data
        project.duration = self.duration.data
        with db.auto_commit():
            db.session.add(project)
        return project