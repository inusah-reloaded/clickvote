from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
import datetime
import time


db = SQLAlchemy()
dbsession = db.session
csrf = CSRFProtect()
login_manager = LoginManager()


def get_timestamp():
    return datetime.datetime.fromtimestamp(
        time.time()).strftime('%Y-%m-%d %H:%M:%S')
