from flask import Blueprint
from flask import url_for, redirect, render_template, request
from ..auth import current_user, logout as _logout
from ..auth import oauth, require_login
from ..forms.user import AuthenticateForm, UserCreationForm, AuthenticateGoogle
from ..forms.profile import ProfileForm
from ..forms.project import ProjectForm
from google.oauth2 import id_token
from ..models.project import Project
from ..models import db, Star, User
from google.auth.transport import requests

bp = Blueprint('project', __name__)

@bp.route('/edit/<id>', methods=['GET', 'POST'])
@require_login
def edit(id):
    project = Project.query.filter_by(id=id).first()
    if project:
        return render_template('edit-project.html', project=project)
    return url_for('front.home')

@bp.route('/create', methods=['GET', 'POST'])
@require_login
def create():
    form = ProjectForm()
    if form.validate_on_submit():
        form.save(current_user.email)
        return redirect(url_for('account.profile'), )
    return render_template('create-project.html', form=form)

@bp.route('/star/<id>', methods=['POST'])
@require_login
def star(id):
    id = int(id)
    project =Project.query.filter_by(id=id).first()
    user = User.query.filter_by(email=current_user.email).first()
    previousStar = Star.query.filter_by(userid=user.id, projectid=id).first()

    if previousStar:
        # Star did exist
        with db.auto_commit():
            db.session.delete(previousStar)
        project.star_count -= 1
    else:
        # Star didn't exist
        star = Star()
        star.userid = user.id
        star.projectid = id
        with db.auto_commit():
            db.session.add(star)

        project.star_count += 1

    with db.auto_commit():
        db.session.add(project)
    # db.session.add(project)
    # db.session.commit

    return redirect(url_for('front.home'))

@bp.route('/delete/<id>', methods=['POST'])
@require_login
def delete(id):
    id = int(id)
    user = User.query.filter_by(email=current_user.email).first()
    project = Project.query.filter_by(id=id, userid=user.id).first()
    stars = Star.query.filter_by(projectid=id).all()
    with db.auto_commit():
        db.session.delete(project)
    for star in stars:
        with db.auto_commit():
            db.session.delete(star)
    return redirect(url_for('front.home'))
