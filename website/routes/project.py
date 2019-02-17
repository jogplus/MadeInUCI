from flask import Blueprint
from flask import url_for, redirect, render_template, request
from ..auth import current_user, logout as _logout
from ..auth import oauth, require_login
from ..forms.user import AuthenticateForm, UserCreationForm, AuthenticateGoogle
from ..forms.profile import ProfileForm
from ..forms.project import ProjectForm
from google.oauth2 import id_token
from ..models.project import Project
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
def star():
    project =Project.query.filter_by(id=id).first()
    if project:
        return "temp"
    return "temp"
