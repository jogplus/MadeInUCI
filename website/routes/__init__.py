from . import front
from . import account
from . import project

def init_app(app):
    app.register_blueprint(account.bp, url_prefix='/account')
    app.register_blueprint(project.bp, url_prefix='/project')
    app.register_blueprint(front.bp, url_prefix='')
