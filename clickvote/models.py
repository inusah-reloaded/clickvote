from flask import redirect, url_for
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .core import db, login_manager, get_timestamp


class Account(db.Model, UserMixin):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    institution = db.Column(db.String(80), index=True, nullable=False)
    department = db.Column(db.String(80), nullable=False)
    program = db.Column(db.String(50), index=True, nullable=False)
    course = db.Column(db.String(50), nullable=False, index=True)
    email = db.Column(db.String(120), index=True)
    phone = db.Column(db.String(10), index=True)
    role = db.Column(db.String(20), default='root')
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)
    roles = db.relationship('Role', backref='account', lazy='dynamic')
    users = db.relationship('User', cascade='save-update, merge, delete',
                            lazy='dynamic')
    elector = db.relationship(
        'Elector', cascade='save-update, merge, delete', lazy='dynamic')
    candidates = db.relationship('Candidate', cascade='save-update,\
                                 merge, delete', lazy='dynamic')
    elections = db.relationship('Election', cascade='save-update,\
                               merge, delete', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Account %s >' % self.name


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, index=True)
    createdby = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.String(20), primary_key=True)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True, index=True)
    phone = db.Column(db.String(10), unique=True, index=True)
    createdby = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % self.username


class Elector(db.Model, UserMixin):
    __tablename__ = 'electors'
    id = db.Column(db.String(20), primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(120), unique=True, index=True)
    phone = db.Column(db.String(10), unique=True, index=True)
    level = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(20), default='vote')
    createdby = db.Column(db.Integer, db.ForeignKey('accounts.id'),
                          nullable=False)
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)
    candidates = db.relationship(
        'Candidate', cascade='save-update, merge, delete', lazy='dynamic')
    status = db.Column(db.String(10), default='inactive')

    def __init__(self, createdby=None, created=None):

        if createdby is None:
            self.createdby = current_user.creator
        if created is None:
            self.created = get_timestamp()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<Elector %r>' % self.id


class Portfolio(db.Model):
    __tablename__ = 'portfolios'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True, nullable=False)
    election_type = db.Column(db.Integer, index=True, nullable=False)
    candidates = db.relationship(
        'Candidate', backref='portfolio', lazy='dynamic')

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Portfolio %s >' % self.name


class Candidate(db.Model):
    __tablename__ = 'candidates'
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, index=True, unique=True)
    elector_id = db.Column(db.String(20), db.ForeignKey('electors.id'))
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id'))
    photo = db.Column(db.String(150))
    createdby = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    election_id = db.Column(db.Integer, db.ForeignKey('elections.id'),
                            nullable=False)
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)

    def __repr__(self):
        return '<Candidate %s>' % self.candidate_id


class Election(db.Model):
    __tablename__ = 'elections'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(180), index=True, unique=True, nullable=False)
    scope = db.Column(db.String(50), nullable=False)
    year_group = db.Column(db.String(10), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='inactive', nullable=False)
    # start_time = db.Column(db.DateTime, nullable=False)
    # stop_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(8), default='testing')
    createdby = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)
    portfolio_0 = db.Column(db.String(50))
    portfolio_1 = db.Column(db.String(50))
    portfolio_2 = db.Column(db.String(50))
    portfolio_3 = db.Column(db.String(50))
    portfolio_4 = db.Column(db.String(50))
    portfolio_5 = db.Column(db.String(50))
    portfolio_6 = db.Column(db.String(50))
    portfolio_7 = db.Column(db.String(50))
    portfolio_8 = db.Column(db.String(50))
    portfolio_9 = db.Column(db.String(50))
    portfolio_10 = db.Column(db.String(50))
    portfolio_11 = db.Column(db.String(50))
    portfolio_12 = db.Column(db.String(50))
    portfolio_13 = db.Column(db.String(50))
    pportfolio_14 = db.Column(db.String(50))
    portfolio_15 = db.Column(db.String(50))
    portfolio_16 = db.Column(db.String(50))
    portfolio_17 = db.Column(db.String(50))
    portfolio_18 = db.Column(db.String(50))
    portfolio_19 = db.Column(db.String(50))
    portfolio_20 = db.Column(db.String(50))
    candidates = db.relationship('Candidate',
                                 backref='candidate', lazy='dynamic')

    def __repr__(self):
        return '<Election %s >' % self.name

    def __str__(self):
        return self.name


class Vote(db.Model):
    __tablename__ = 'votes'
    id = db.Column(db.Integer, primary_key=True)
    elector_id = db.Column(db.String(20), db.ForeignKey('electors.id'))
    election_id = db.Column(db.Integer, db.ForeignKey('elections.id'))
    portfolio_0 = db.Column(db.String(9), default='not voted')
    portfolio_1 = db.Column(db.String(9), default='not voted')
    portfolio_2 = db.Column(db.String(9), default='not voted')
    portfolio_3 = db.Column(db.String(9), default='not voted')
    portfolio_4 = db.Column(db.String(9), default='not voted')
    portfolio_5 = db.Column(db.String(9), default='not voted')
    portfolio_6 = db.Column(db.String(9), default='not voted')
    portfolio_7 = db.Column(db.String(9), default='not voted')
    portfolio_8 = db.Column(db.String(9), default='not voted')
    portfolio_9 = db.Column(db.String(9), default='not voted')
    portfolio_10 = db.Column(db.String(9), default='not voted')
    portfolio_11 = db.Column(db.String(9), default='not voted')
    portfolio_12 = db.Column(db.String(9), default='not voted')
    portfolio_13 = db.Column(db.String(9), default='not voted')
    portfolio_14 = db.Column(db.String(9), default='not voted')
    portfolio_15 = db.Column(db.String(9), default='not voted')
    portfolio_16 = db.Column(db.String(9), default='not voted')
    portfolio_17 = db.Column(db.String(9), default='not voted')
    portfolio_18 = db.Column(db.String(9), default='not voted')
    portfolio_19 = db.Column(db.String(9), default='not voted')
    portfolio_20 = db.Column(db.String(9), default='not voted')
    status = db.Column(db.String(6), nullable=False, default='0')


class HistoryLog(db.Model):
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    createdby = db.Column(db.String(20), nullable=False, index=True)
    timestamp = db.Column(db.DateTime, nullable=False)


class UserLogin(UserMixin):

    def __init__(self):
        self.user_id = None
        self.department = None
        self.school = None
        self.creator = None
        self.name = None
        self.active_election = None
        self.scope = None

    def get_role(self):
        return self.role

    def set_role(self, role):
        self.role = role

    def get_id(self):
        return self.user_id

    def get_department(self):
        return self.department

    def is_elector(self):
        return True if self.role == 'vote' else False

    def is_admin(self):
        return True if self.role == 'admin' else False

    def is_root(self):
        return True if self.role == 'root' else False

    def __str__(self):
        return self.user_id


@login_manager.user_loader
def load_user(user_id):
    from flask import session
    user = None
    flask_user = UserLogin()
    if 'type' in session:
        flask_user.set_role(session['type'])
        flask_user.user_id = user_id

        if 'root' in session['type']:
            user = Account.query.filter_by(id=user_id).first()
            if user is None:
                return redirect(url_for('auth.login'))
            flask_user.department = user.department
            flask_user.school = user.institution
            flask_user.creator = user.id
            flask_user.name = user.name
            flask_user.active_election = session['active_election'] if \
                'active_election' in session else None
            flask_user.scope = session['scope'] if 'scope' in session else None

            return flask_user
        else:
            if session['type'] in ['vote']:
                user = Elector.query.filter_by(id=user_id).first()
            elif session['type'] in ['admin', 'user', 'strongroom']:
                user = User.query.filter_by(id=user_id).first()
            user_origin = Account.query.filter_by(id=user.createdby).first()
            flask_user.creator = user_origin.id
            flask_user.department = user_origin.department
            flask_user.school = user_origin.institution
            flask_user.name = user.id
            flask_user.active_election = session['active_election'] if \
                'active_election' in session else None
            flask_user.scope = session['scope'] if 'scope' in session else None

            return flask_user
