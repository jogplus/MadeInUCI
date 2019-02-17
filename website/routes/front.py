from flask import Blueprint
from flask import render_template
from ..auth import current_user
from ..forms.auth import AuthenticateGoogle
from ..models.user import User
from ..models.project import Project
from ..models.star import Star


bp = Blueprint('front', __name__)


@bp.route('/', methods=['GET', 'POST'])
def home():
    google_form = AuthenticateGoogle(prefix="google")
    google_form.validate_on_submit()
    projects = Project.query.all()
    projects = sorted(projects, key=lambda p: p.star_count)
    starIDs = []
    if current_user:
        starsIDs = [s.projectid for s in Star.query.filter_by(userid=current_user.id).all()]
    return render_template('index.html', google_form=google_form, projects=projects, starIDs=starIDs)
