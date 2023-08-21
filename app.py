
from flask_migrate import Migrate 

from clickvote import create_app
from clickvote.core import db
from clickvote.models import User, Role, Elector, Candidate, Election, Portfolio, \
    Vote, Account


app = create_app('default')
migrate = Migrate(app, db)

def make_shell_context():
    return dict(
        app=app, db=db, User=User, Role=Role,
        Elector=Elector, Candidate=Candidate,
        Election=Election, Vote=Vote, Account=Account, Portfolio=Portfolio
    )

def test():
    import unittest
    test = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(test)

if __name__ == '__main__':
    app.run()
