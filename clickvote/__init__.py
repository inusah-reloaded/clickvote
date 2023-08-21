import os
from flask import Flask, send_from_directory
# from flask_admin import Admin
# from flask_admin.contrib.sqla import ModelView
#import flask_excel as excel

from config import config
from .core import db, csrf, login_manager
from runvote.models import Account, Role

appdir = os.path.abspath(os.path.dirname(__file__))

login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.voter_login'


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
#    excel.init_excel(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    from .views import runvote
    from .auth import auth
    app.register_blueprint(runvote, url_prefix='/console')
    app.register_blueprint(auth)

#    admin = Admin(app, name='runvote admin', template_mode='bootstrap3')
#    admin.add_view(ModelView(Role, db.session))
#    admin.add_view(ModelView(Account, db.session))

    app.config['UPLOAD_FOLDER'] = os.path.join(appdir, 'uploads')
    app.config['IMAGES_FOLDER'] = os.path.join(app.config[
        'UPLOAD_FOLDER'], 'images')
    app.upload_folder = app.config['UPLOAD_FOLDER']

    @app.route('/uploads/<filename>', defaults={'setname': None})
    @app.route('/uploads/<setname>/<filename>')
    def uploaded_file(setname, filename):
        return send_from_directory(os.path.join(app.config[
            'UPLOAD_FOLDER'], setname), filename)

    return app
