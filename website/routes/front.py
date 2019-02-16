from flask import Blueprint
from flask import render_template
from ..auth import current_user
from ..forms.auth import AuthenticateGoogle


bp = Blueprint('front', __name__)


@bp.route('/', methods=['GET', 'POST'])
def home():
    google_form = AuthenticateGoogle(prefix="google")
    google_form.validate_on_submit()
    return render_template('index.html', google_form=google_form)
