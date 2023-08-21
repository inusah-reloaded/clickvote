from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, FileField, SelectField,\
    PasswordField, IntegerField
from wtforms.fields import DateField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import validators
from flask_wtf.file import FileRequired, FileAllowed

from .helpers import get_roles, get_portfolios


class AddVoterForm(FlaskForm):
    id = StringField('ID:', [validators.InputRequired()])
    first_name = StringField('First Name:', [validators.InputRequired()])
    last_name = StringField('Last Name:', [validators.InputRequired()])
    # password = PasswordField('Password', [validators.InputRequired()])
    # mobile = IntegerField('Mobile:')
    email = StringField('Email:')
    level = SelectField('Level:', [
        validators.InputRequired()], choices=[
            ('', ''), ('100', '100'),
            ('200', '200'), ('300', '300'),
            ('400', '400')])
    submit = SubmitField('Add')


class EditVoterForm(FlaskForm):
    id = StringField('ID:', [validators.InputRequired()])
    first_name = StringField('FirstName:', [validators.InputRequired()])
    last_name = StringField('Last Name:', [validators.InputRequired()])
    email = StringField('Email:')
    mobile = IntegerField('Mobile:')
    department = StringField('Department:', [validators.InputRequired()])
    program = StringField('Program:')
    level = StringField('Level:')
    submit = SubmitField('Update')


class ImportFromCSVForm(FlaskForm):
    csv_file = FileField('Excel File',
                         validators=[
                             FileRequired(), FileAllowed([
                                 'xls', 'xlsx'], 'xls | xlsx  Files only!')])

    submit = SubmitField('Upload')


class SearchForm(FlaskForm):
    identifier = StringField('Search Field', [validators.InputRequired()])
    submit = SubmitField('Search')


class AddUserForm(FlaskForm):
    username = StringField('User Name', [validators.InputRequired()])
    first_name = StringField('First Name', [validators.InputRequired()])
    last_name = StringField('Last Name', [validators.InputRequired()])
    email = StringField('Email')
    phone = IntegerField('Mobile', [validators.InputRequired()])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password')
    role = QuerySelectField(u'Role', [
       validators.InputRequired()], query_factory=get_roles)

    submit = SubmitField('Add')


class EditUserForm(FlaskForm):

    first_name = StringField('First Name', [validators.InputRequired()])
    last_name = StringField('Last Name', [validators.InputRequired()])
    email = StringField('Email')
    phone = IntegerField('Mobile', [validators.InputRequired()])
    old_password = PasswordField('Old Password', [validators.InputRequired()])
    new_password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password')
#    role = QuerySelectField(u'Role', [
#        validators.InputRequired()], query_factory=get_roles)

    submit = SubmitField('Add')


class AddCandidateForm(FlaskForm):
    candidate_id = IntegerField('CID', [validators.InputRequired()])
    voter_id = StringField('Student ID', [validators.InputRequired()])
    portfolio = QuerySelectField('Portfolio', [
        validators.InputRequired()], query_factory=get_portfolios)
    election_id = IntegerField('Election ID', [validators.InputRequired()])
    picture = FileField('Image File', validators=[
        FileRequired(message='Image file required | jpg | png | jpeg'),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Image Files only!')]
    )

    submit = SubmitField('Add')


class EditCandidateForm(FlaskForm):
    candidate_id = IntegerField('CID', [validators.InputRequired()])
    voter_id = StringField('Student ID', [validators.InputRequired()])
    portfolio = SelectField('Portfolio')
    # election_id = IntegerField('Election ID', [validators.InputRequired()])
    picture = FileField('Image File', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Image Files only!')]
    )

    submit = SubmitField('Update')


class CSRFonlyForm(FlaskForm):
    name = StringField('name')


class CreateElectionForm(FlaskForm):
    name = StringField('Name', [validators.InputRequired()])
    scope = SelectField('Scope', [validators.InputRequired()],
                        choices=[('dep', 'dep'), ('src', 'src')])
    date = DateField('Date',  [validators.InputRequired(),
                               validators.Optional()], format='%Y-%m-%d')
    portfolio_1 = QuerySelectField('Portfolio 1', [validators.InputRequired()],
                                   query_factory=get_portfolios)
    portfolio_2 = QuerySelectField('Portfolio 2', [validators.InputRequired()],
                                   query_factory=get_portfolios)
    portfolio_3 = QuerySelectField('Portfolio 3', [validators.InputRequired()],
                                   query_factory=get_portfolios)
    portfolio_4 = QuerySelectField('Portfolio 4', [validators.InputRequired()],
                                   query_factory=get_portfolios)
    portfolio_5 = QuerySelectField('Portfolio 5', [validators.InputRequired()],
                                   query_factory=get_portfolios)
    portfolio_6 = QuerySelectField('Portfolio 6', query_factory=get_portfolios)
    portfolio_7 = QuerySelectField('Portfolio 7', query_factory=get_portfolios)
    portfolio_8 = QuerySelectField('Portfolio 8', query_factory=get_portfolios)
    portfolio_9 = QuerySelectField('Portfolio 9', query_factory=get_portfolios)
    portfolio_10 = QuerySelectField('Portfolio 10',
                                    query_factory=get_portfolios)

    portfolio_11 = QuerySelectField('Portfolio 11',
                                    query_factory=get_portfolios)
    portfolio_12 = QuerySelectField('Portfolio 12',
                                    query_factory=get_portfolios)
    portfolio_13 = QuerySelectField('Portfolio 13',
                                    query_factory=get_portfolios)
    portfolio_14 = QuerySelectField('Portfolio 14',
                                    query_factory=get_portfolios)
    portfolio_15 = QuerySelectField('Portfolio 15',
                                    query_factory=get_portfolios)
                                   
    submit = SubmitField('Create')


class EditElectionForm(FlaskForm):
    name = StringField('Name', [validators.InputRequired()])
    scope = SelectField('Scope', [validators.InputRequired()],
                        choices=[('dep', 'dep'), ('src', 'src')])
    date = DateField('Date',  [validators.InputRequired(),
                               validators.Optional()], format='%Y-%m-%d')
    portfolio_1 = QuerySelectField('Portfolio 1',
                                   query_factory=get_portfolios)
    portfolio_2 = QuerySelectField('Portfolio 2',
                                   query_factory=get_portfolios)
    portfolio_3 = QuerySelectField('Portfolio 3',
                                   query_factory=get_portfolios)
    portfolio_4 = QuerySelectField('Portfolio 4',
                                   query_factory=get_portfolios)
    portfolio_5 = QuerySelectField('Portfolio 5',
                                   query_factory=get_portfolios)
    portfolio_6 = QuerySelectField('Portfolio 6', query_factory=get_portfolios)
    portfolio_7 = QuerySelectField('Portfolio 7', query_factory=get_portfolios)
    portfolio_8 = QuerySelectField('Portfolio 8', query_factory=get_portfolios)
    portfolio_9 = QuerySelectField('Portfolio 9', query_factory=get_portfolios)
    portfolio_10 = QuerySelectField('Portfolio 10',
                                    query_factory=get_portfolios)

    portfolio_11 = QuerySelectField('Portfolio 11',
                                    query_factory=get_portfolios)
    portfolio_12 = QuerySelectField('Portfolio 12',
                                    query_factory=get_portfolios)
    portfolio_13 = QuerySelectField('Portfolio 13',
                                    query_factory=get_portfolios)
    portfolio_14 = QuerySelectField('Portfolio 14',
                                    query_factory=get_portfolios)
    portfolio_15 = QuerySelectField('Portfolio 15',
                                    query_factory=get_portfolios)
                                   
    submit = SubmitField('Create')


class EditAccountForm(FlaskForm):
    old_password = PasswordField('Old Password', [validators.InputRequired()])
    new_password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password')
    submit = SubmitField('Update')

