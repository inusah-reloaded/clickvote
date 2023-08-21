# from flask_script import Manager
from flask_migrate import Migrate #, MigrateCommand

from runvote import create_app
from runvote.core import db
from runvote.models import User, Role, Elector, Candidate, Election, Portfolio, \
    Vote, Account


app = create_app('default')
#manager = Manager(app)
migrate = Migrate(app, db)


#@manager.command
def make_shell_context():
    return dict(
        app=app, db=db, User=User, Role=Role,
        Elector=Elector, Candidate=Candidate,
        Election=Election, Vote=Vote, Account=Account, Portfolio=Portfolio
    )

#manager.add_command('shell', Shell(make_context=make_shell_context))
#manager.add_command('db', MigrateCommand)


#@manager.command
def test():
    import unittest
    test = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(test)

if __name__ == '__main__':
    app.run()
