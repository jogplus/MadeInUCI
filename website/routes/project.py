from flask import Blueprint
from flask import url_for, redirect, render_template, request
from ..auth import current_user, logout as _logout
from ..auth import oauth, require_login
from ..forms.user import AuthenticateForm, UserCreationForm, AuthenticateGoogle
from google.oauth2 import id_token
from google.auth.transport import requests

bp = Blueprint('project', __name__)

@bp.route('/create', methods=['GET', 'POST'])
@require_login
def profile():
    return render_template('edit-project.html')