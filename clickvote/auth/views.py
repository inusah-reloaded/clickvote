from flask import render_template, request, url_for, redirect, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .forms import LoginForm, VoterLoginForm
from runvote.models import Account, User, Elector
from ..helpers import get_active_election, validate_vote_url, \
     get_elector_status, set_history


@auth.route('/', methods=['GET', 'POST'])
def voter_login():
    form = VoterLoginForm()

    if form.validate_on_submit():
        elector = Elector.query.filter_by(id=form.id.data).first()
        if elector is not None:
            a = Account.query.filter_by(id=elector.createdby).first()
            school = a.institution
            department = a.department
            e = get_active_election(elector.createdby, a.institution)
            elector_status = get_elector_status(elector.id, e.id)
            if elector_status == 'inactive':
                flash('You haven\'t been verified')
            elif elector_status == 'voted':
                flash('Sorry! You\'ve voted already')
            else:
                if e is not None:
                    scope = e.scope
                    election = e.id
                    login_user(elector)
                    set_history('Login', 'logged in', elector.id)
                    session['type'] = elector.role
                    session['active_election'] = e.id
                    session['scope'] = e.scope
                    portfolio = validate_vote_url(elector.id, election)
                    if portfolio == 'voted':
                        # flash('You have finished voting')
                        return redirect(url_for('runvote.vote_summary',
                                                school=school,
                                                scope=scope,
                                                department=department,
                                                election=election))

                    if scope in 'dep':
                        return redirect(
                                        url_for('runvote.vote', school=school,
                                                scope=scope,
                                                department=department,
                                                election=election,
                                                portfolio=portfolio))
                    return redirect(request.args.get('next') or
                                    url_for('runvote.vote', school=school,
                                            scope=scope,
                                            election=election,
                                            portfolio=portfolio))
        else:
            flash('Record not found')

    return render_template('auth/voter_login.html', form=form)


@auth.route('/admin_login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        account = Account.query.filter_by(name=form.id.data).first()
        user = User.query.filter_by(id=form.id.data).first()
        # elector = Elector.query.filter_by(id=form.id.data).first()

        if user is not None and user.verify_password(form.password.data):
            a = Account.query.filter_by(id=user.createdby).first()
            e = get_active_election(user.createdby, a.institution)
            if e is not None:
                session['active_election'] = e.id
                session['scope'] = e.scope
            session['type'] = str(user.role)
            login_user(user)
            set_history('Login', 'logged in', user.id)
            return redirect(request.args.get('next') or
                            url_for('runvote.console'))

        if account is not None and account.verify_password(form.password.data):
            e = get_active_election(account.id, account.institution)
            if e is not None:
                session['active_election'] = e.id
                session['scope'] = e.scope
            session['type'] = account.role
            login_user(account)
            set_history('Login', 'logged in', account.name)
            return redirect(request.args.get('next') or
                            url_for('runvote.console'))

        '''
        if elector is not None and elector.verify_password(form.password.data):
            a = Account.query.filter_by(id=elector.createdby).first()
            school = a.institution
            department = a.department
            e = get_active_election(elector.createdby, a.institution)
            if e is not None:
                scope = e.scope
                election = e.id
                login_user(elector)
                session['type'] = elector.role
                session['active_election'] = e.id
                session['scope'] = e.scope
                check_elector_votes_record(elector.id, election)
                portfolio = validate_vote_url(elector.id, election)
                if portfolio == 'voted':
                    # flash('You have finished voting')
                    return redirect(url_for('runvote.vote_summary',
                                            school=school,
                                            scope=scope,
                                            department=department,
                                            election=election))

                if scope in 'dep':
                    return redirect(
                                    url_for('runvote.vote', school=school,
                                            scope=scope,
                                            department=department,
                                            election=election,
                                            portfolio=portfolio))
                return redirect(request.args.get('next') or
                                url_for('runvote.vote', school=school,
                                        scope=scope,
                                        election=election, portfolio=portfolio))
            '''
        flash('Invalid ID or Password')

    return render_template('auth/index.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    flash('You have been logged out')
    if session['type'] in ['root', 'admin', 'user', 'strongroom']:
        set_history('Logout', 'logged out', current_user.name)
        logout_user()
        session.clear()
        return redirect(url_for('auth.login'))
    set_history('Logout', 'logged out', current_user.name)
    session.clear()
    return redirect(url_for('auth.voter_login'))
