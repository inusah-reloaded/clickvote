import os
# from runvote import create_app
from datetime import date
from functools import wraps
from flask import flash, request, redirect, current_app, url_for
from .models import Elector, User, Candidate, Role, Portfolio, Vote, Election, \
    Account, HistoryLog
from .core import dbsession
from sqlalchemy import exc, desc, asc
from werkzeug.utils import secure_filename
from flask_login import current_user
import datetime
import time
# from grampg import PasswordGenerator


def get_timestamp():
    return datetime.datetime.fromtimestamp(
        time.time()).strftime('%Y-%m-%d %H:%M:%S')


def get_account_id():
    return current_user.user_id if current_user.is_root() \
        else current_user.creator


def set_history(action, description, user):
    history = HistoryLog()
    history.action = action
    history.description = description
    history.createdby = user
    history.timestamp = get_timestamp()
    dbsession.add(history)
    dbsession.commit()


def add_new_voter(form):
    if form.validate_on_submit():
        elector = Elector.query.filter_by(id=form.id.data).first()
        if elector is not None:
            flash(u'record already exist', 'error')
        else:

            voter = Elector()
            voter.id = form.id.data
            voter.first_name = form.first_name.data
            voter.last_name = form.last_name.data
            # voter.password = form.password.data
            # voter.email = form.email.data
            # voter.phone = form.mobile.data
            voter.level = form.level.data
            voter.createdby = current_user.creator
            voter.created = get_timestamp()
            dbsession.add(voter)
            try:
                dbsession.commit()
                set_history('New Record',
                            'added voter with id: '+voter.id, current_user.name)
                flash(u'Successfully added electorate', 'success')
            except exc.IntegrityError:
                dbsession.rollback()
                handle_exception(voter)
                flash(u'Failed to add electorate', 'error')


def add_new_user(form):
    if form.validate_on_submit():
        user_query = dbsession.query(User).filter_by(
            id=form.username.data).count()
        if user_query == 1:
            flash(u'record already exist', 'error')
        else:
            user = User()
            user.id = form.username.data
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.email = form.email.data
            user.phone = form.phone.data
            user.password = form.password.data
            user.role = form.role.data
            user.createdby = current_user.creator
            user.created = get_timestamp()
            dbsession.add(user)

            try:
                dbsession.commit()
                set_history('New Record',
                            'added user with id: '+user.id, current_user.name)
                flash(u'User successfully added', 'success')
                redirect(request.url)
            except exc.IntegrityError:
                dbsession.rollback()
                handle_exception(user)


def edit_user_info(user_id, form):
    user = User.query.filter_by(id=user_id).first()
    if user.verify_password(form.old_password.data):
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        user.phone = form.phone.data
        user.id = form.username.data
        user.password = form.new_password.data
        user.role = form.role.data
        dbsession.add(user)
        dbsession.commit()
        set_history('Edit', 'added user with id: '+user_id, current_user.name)
        flash(u'User successfully edited', 'success')
    else:
        flash(u'Old password doesn\'t match with user password', 'error')


def delete_user(user_id):
    instance = User.query.filter_by(id=user_id).first()
    dbsession.delete(instance)
    dbsession.commit()
    set_history('Delete', 'droped  user with id: '+user_id, current_user.name)


def delete_election(eid):
    instance = Election.query.filter_by(id=eid).first()
    dbsession.delete(instance)
    dbsession.commit()
    set_history('Delete', 'droped  Election with id: '+str(eid),
                current_user.name)


def add_new_candidate(form):
    if form.validate_on_submit():
        candidate = Candidate.query.filter_by(
            candidate_id=str(form.candidate_id.data)).first()
        if candidate and candidate.election_id == form.election_id.data:
            flash(u'Candidate ID already exist', 'error')
        else:
            app = current_app
            file = form.picture.data
            filename = secure_filename(file.filename)
            path = os.path.join(app.config[
                'IMAGES_FOLDER'], filename)
            candidate = Candidate()
            candidate.candidate_id = form.candidate_id.data
            candidate.election_id = form.election_id.data
            candidate.elector_id = form.voter_id.data
            candidate.portfolio = form.portfolio.data
            candidate.photo = filename
            candidate.createdby = current_user.creator
            candidate.created = get_timestamp()
            dbsession.add(candidate)
            # try:
            dbsession.commit()
            file.save(path)
            set_history('New Record',
                        'added Candidate with id: '+ str(candidate.id),
                        current_user.name)
            flash(u'Candidate successfully added', 'success')
            # except exc.IntegrityError:
            # dbsession.rollback()
            # flash(u'Failed to add candidate', 'error')

def edit_candidate_info(cid, form):
    if form.validate_on_submit():
        candidate = dbsession.query(Candidate).filter_by(id=cid).first()
        if candidate.candidate_id == form.candidate_id.data:

            app = current_app
            file = form.picture.data
            if form.picture.data:
                filename = secure_filename(file.filename)
                path = os.path.join(app.config[
                    'IMAGES_FOLDER'], filename)
            candidate.candidate_id = form.candidate_id.data
            candidate.elector_id = form.voter_id.data
            candidate.portfolio_id = form.portfolio.data
            if form.picture.data:
                candidate.photo = filename
            candidate.createdby = current_user.creator
            candidate.updated = get_timestamp()
            dbsession.add(candidate)
            # try:
            dbsession.commit()
            if form.picture.data:
                file.save(path)
            set_history('New Record',
                        'Edited Candidate with id: '+str(candidate.id),
                        current_user.name)
            flash(u'Candidate info successfully edited', 'success')


def delete_candidate(candidate_id):
    instance = Candidate.query.filter_by(id=candidate_id).first()
    dbsession.delete(instance)
    dbsession.commit()
    set_history('Delete', 'droped Candidate with id: '+candidate_id,
                current_user.name)


def delete_elector(elector_id):
    instance = Elector.query.filter_by(id=elector_id).first()
    dbsession.delete(instance)
    dbsession.commit()
    set_history('Delete', 'Droped Voter with id: '+elector_id,
                current_user.name)


def import_from_csv(form):
    if form.validate_on_submit():
        def init_candidate(row):
            c = Elector(
                row['id'],
                row['first_name'],
                row['last_name'],
                row['level'],
            )
            return c
        # try:
    request.save_to_database(
        field_name='csv_file', session=dbsession,
        table=Elector, initializers=init_candidate)
    flash(u'Electors Uploaded', 'success')
    # except exc.IntegrityError:
    # flash(u'Failed! Possible intergrity error', 'error')


def get_voter_details(voter_id):
    return (dbsession.query(Elector, Account)
            .filter_by(id=voter_id)
            .filter_by(createdby=current_user.creator)
            .join(Account)
            .filter_by(id=Elector.createdby)
            .first()
            ) if current_user.department not in 'src' else \
        (dbsession.query(Elector, Account)
            .filter_by(id=voter_id)
            .join(Account)
            .filter_by(id=Elector.createdby)
            .filter_by(institution=current_user.school)
            .first()
         )


def get_candidates(cid=None):
    if cid is None:
        return (dbsession.query(Account, Candidate, Elector)
                .filter_by(id=Candidate.createdby)
                .join(Candidate)
                .filter_by(createdby=current_user.creator)
                .join(Elector)
                .filter_by(id=Candidate.elector_id)
                .order_by(Candidate.candidate_id).all()
                )
    return (dbsession.query(Account, Candidate, Elector)
            .filter_by(id=Candidate.createdby)
            .join(Candidate)
            .filter_by(id=int(cid))
            .filter_by(createdby=current_user.creator)
            .join(Elector)
            .filter_by(id=Candidate.elector_id)
            .first()
            )


def get_candidates_by(school, scope, election, position=None):
    if position is None:
        if 'src' in scope:
            return (dbsession.query(Election, Account,
                    Candidate, Portfolio, Elector)
                    .filter(Election.status.in_(['active', 'testing']))
                    .filter_by(scope='src')
                    .filter_by(id=election)
                    .join(Account)
                    .filter_by(id=Election.createdby)
                    .join(Candidate)
                    .filter_by(createdby=Election.createdby)
                    .join(Elector)
                    .filter_by(id=Candidate.elector_id)
                    .join(Portfolio)
                    .filter_by(id=Candidate.portfolio_id)
                    .order_by(asc(Candidate.candidate_id)).all()
                    )
        return (dbsession.query(
            Election, Account, Candidate, Portfolio, Elector)
                .filter(Election.status.in_(['active', 'testing']))
                .filter_by(scope='dep')
                .filter_by(id=election)
                .filter_by(createdby=current_user.creator)
                .join(Account)
                .filter_by(id=Election.createdby)
                .join(Candidate)
                .filter_by(createdby=Election.createdby)
                .join(Elector)
                .filter_by(id=Candidate.elector_id)
                .join(Portfolio)
                .filter_by(id=Candidate.portfolio_id)
                .order_by(asc(Candidate.candidate_id)).all()
                )

    if 'src' in scope:
        return (dbsession.query(
            Election, Account, Candidate, Portfolio, Elector)
                .filter(Election.status.in_(['active', 'testing']))
                .filter_by(scope='src')
                .filter_by(id=election)
                .join(Account)
                .filter_by(id=Election.createdby)
                .join(Candidate)
                .filter_by(createdby=Election.createdby)
                .join(Elector)
                .filter_by(id=Candidate.elector_id)
                .join(Portfolio)
                .filter_by(id=Candidate.portfolio_id)
                .filter_by(name=position)
                .order_by(asc(Candidate.candidate_id)).all()
                )
    return (dbsession.query(Election, Account, Candidate, Portfolio, Elector)
            .filter(Election.status.in_(['active', 'testing']))
            .filter_by(scope='dep')
            .filter_by(id=election)
            .filter_by(createdby=current_user.creator)
            .join(Account)
            .filter_by(id=Election.createdby)
            .join(Candidate)
            .filter_by(createdby=Election.createdby)
            .join(Elector)
            .filter_by(id=Candidate.elector_id)
            .join(Portfolio)
            .filter_by(id=Candidate.portfolio_id)
            .filter_by(name=position)
            .order_by(asc(Candidate.candidate_id)).all()
            )


def get_candidate(eid, id, position):
    if 'no' in id:
        return ('NO', dbsession.query(Candidate, Portfolio, Elector)
                .filter_by(election_id=eid)
                .join(Elector)
                .filter_by(id=Candidate.elector_id)
                .join(Portfolio)
                .filter_by(id=Candidate.portfolio_id)
                .filter_by(name=position)
                .first())
    if 'skip' in id:
        return ('SKIP', dbsession.query(Candidate, Portfolio, Elector)
                .filter_by(election_id=eid)
                .join(Elector)
                .filter_by(id=Candidate.elector_id)
                .join(Portfolio)
                .filter_by(id=Candidate.portfolio_id)
                .filter_by(name=position)
                .first())

    return (dbsession.query(Candidate, Portfolio, Elector)
            .filter_by(election_id=eid)
            .filter_by(id=id)
            .join(Elector)
            .filter_by(id=Candidate.elector_id)
            .join(Portfolio)
            .filter_by(id=Candidate.portfolio_id)
            .filter_by(name=position)
            .first()
            )


def selected_candidates(eid):
    vote = (dbsession.query(Vote).filter_by(election_id=eid)
            .filter_by(elector_id=current_user.user_id)
            .first()
            )
    port_0 = (
        get_candidate(eid, vote.portfolio_0, get_election_portfolios(eid, '0'))
              ) if 'not voted' not in vote.portfolio_0 else None

    port_1 = (
        get_candidate(eid, vote.portfolio_1, get_election_portfolios(eid, '1'))
              ) if 'not voted' not in vote.portfolio_1 else None

    port_2 = (
        get_candidate(eid, vote.portfolio_2, get_election_portfolios(eid, '2'))
              ) if 'not voted' not in vote.portfolio_2 else None

    port_3 = (
        get_candidate(eid, vote.portfolio_3, get_election_portfolios(eid, '3'))
              ) if 'not voted' not in vote.portfolio_3 else None

    port_4 = (
        get_candidate(eid, vote.portfolio_4, get_election_portfolios(eid, '4'))
              ) if 'not voted' not in vote.portfolio_4 else None

    port_5 = (
        get_candidate(eid, vote.portfolio_5, get_election_portfolios(eid, '5'))
              ) if 'not voted' not in vote.portfolio_5 else None

    port_6 = (
        get_candidate(eid, vote.portfolio_6, get_election_portfolios(eid, '6'))
              ) if 'not voted' not in vote.portfolio_6 else None

    port_7 = (
        get_candidate(eid, vote.portfolio_7, get_election_portfolios(eid, '7'))
              ) if 'not voted' not in vote.portfolio_7 else None

    port_8 = (
        get_candidate(eid, vote.portfolio_8, get_election_portfolios(eid, '8'))
              ) if 'not voted' not in vote.portfolio_8 else None

    port_9 = (
        get_candidate(eid, vote.portfolio_9, get_election_portfolios(eid, '9'))
              ) if 'not voted' not in vote.portfolio_9 else None

    port_10 = (
        get_candidate(eid, vote.portfolio_10,
                      get_election_portfolios(eid, '10'))
              ) if 'not voted' not in vote.portfolio_10 else None
    port_11 = (
        get_candidate(eid, vote.portfolio_11,
                      get_election_portfolios(eid, '11'))
              ) if 'not voted' not in vote.portfolio_11 else None

    port_12 = (
        get_candidate(eid, vote.portfolio_12,
                      get_election_portfolios(eid, '12'))
              ) if 'not voted' not in vote.portfolio_12 else None

    port_13 = (
        get_candidate(eid, vote.portfolio_13,
                      get_election_portfolios(eid, '13'))
              ) if 'not voted' not in vote.portfolio_13 else None

    port_14 = (
        get_candidate(eid, vote.portfolio_14,
                      get_election_portfolios(eid, '14'))
              ) if 'not voted' not in vote.portfolio_14 else None

    port_15 = (
        get_candidate(eid, vote.portfolio_15,
                      get_election_portfolios(eid, '15'))
              ) if 'not voted' not in vote.portfolio_15 else None

    port_16 = (
        get_candidate(eid, vote.portfolio_16,
                      get_election_portfolios(eid, '16'))
              ) if 'not voted' not in vote.portfolio_16 else None

    port_17 = (
        get_candidate(eid, vote.portfolio_17,
                      get_election_portfolios(eid, '17'))
              ) if 'not voted' not in vote.portfolio_17 else None

    port_18 = (
        get_candidate(eid, vote.portfolio_18,
                      get_election_portfolios(eid, '18'))
              ) if 'not voted' not in vote.portfolio_18 else None

    port_19 = (
        get_candidate(eid, vote.portfolio_19,
                      get_election_portfolios(eid, '19'))
              ) if 'not voted' not in vote.portfolio_19 else None

    port_20 = (
        get_candidate(eid, vote.portfolio_20,
                      get_election_portfolios(eid, '20'))
              ) if 'not voted' not in vote.portfolio_20 else None

    return [port_0, port_1, port_2, port_3, port_4, port_5, port_6, port_7,
            port_8, port_9, port_10, port_11, port_12, port_13, port_14,
            port_15, port_16, port_17, port_18, port_19, port_20]


def get_users(id=None):

    if id is None:
        if current_user.role == 'root':
            return (dbsession.query(User)
                    .filter_by(createdby=current_user.user_id))
        else:
            return (dbsession.query(User)
                    .filter_by(createdby=current_user.creator))

    else:
        return (dbsession.query(User)
                .filter_by(id=id)
                .filter_by(createdby=current_user.creator))


def get_history(createdby=None):

    if createdby is None:
        return dbsession.query(HistoryLog).order_by(desc(
            HistoryLog.id))
    return dbsession.query(HistoryLog).filter_by(
        createdby=createdby).order_by(desc(HistoryLog.id))


def get_roles(id=None):
    if id is None:
        return dbsession.query(Role).all()
    else:
        return Role.query.filter_by(id=id).first()


def get_portfolios_edit():
    choices = [("0", "Select Portfolio")]
    for i in Portfolio.query.all():
        choices.append((str(i.id), i.name))
    return choices


def get_portfolios(pid=None):
    if pid is None:
        return Portfolio.query
    return Portfolio.query.filter_by(id=pid).first().name



def get_all_portfolios(election_id):
    return [get_election_portfolios(election_id, str(i)) for i in range(12)]


def create_elections(form):
    election = Election()
    election.name = form.name.data
    election.scope = form.scope.data
    election.year_group = 'all'
    election.date = form.date.data
    # election.start_time = form.start_time.data
    # election.stop_time = form.stop_time.data
    election.createdby = current_user.creator
    election.created = get_timestamp()
    election.portfolio_0 = str(form.portfolio_1.data)
    election.portfolio_1 = str(form.portfolio_2.data)
    election.portfolio_2 = str(form.portfolio_3.data)
    election.portfolio_3 = str(form.portfolio_4.data)
    election.portfolio_4 = str(form.portfolio_5.data)
    election.portfolio_5 = str(form.portfolio_6.data)
    election.portfolio_6 = str(form.portfolio_7.data)
    election.portfolio_7 = str(form.portfolio_8.data)
    election.portfolio_8 = str(form.portfolio_9.data)
    election.portfolio_9 = str(form.portfolio_10.data)

    dbsession.add(election)
    dbsession.commit()

    set_history('New Record',
                'Created '+election.name+' with id: '+str(election.id),
                current_user.name)
    flash(u'election created successfully', 'success')


def edit_elections(eid, form):
    election = Election.query.filter_by(id=eid).first()
    election.name = form.name.data
    election.scope = form.scope.data
    election.date = form.date.data
    # election.start_time = form.start_time.data
    # election.stop_time = form.stop_time.data
    election.createdby = current_user.creator
    election.updated = get_timestamp()
    election.portfolio_0 = str(form.portfolio_1.data)
    election.portfolio_1 = str(form.portfolio_2.data)
    election.portfolio_2 = str(form.portfolio_3.data)
    election.portfolio_3 = str(form.portfolio_4.data)
    election.portfolio_4 = str(form.portfolio_5.data)
    election.portfolio_5 = str(form.portfolio_6.data)
    election.portfolio_6 = str(form.portfolio_7.data)
    election.portfolio_7 = str(form.portfolio_8.data)
    election.portfolio_8 = str(form.portfolio_9.data)
    election.portfolio_9 = str(form.portfolio_10.data)

    dbsession.add(election)
    dbsession.commit()
    set_history('Edit',
                'Edited '+election.name+' with id: '+eid,
                current_user.name)
    flash(u'election created successfully', 'success')


def edit_election_status(election_id, status):
    election = Election.query.filter_by(id=election_id).first()
    if election.status == 'testing' and status == 'active':
        Vote.query.filter(Vote.election_id == election_id).delete()
    elif election.status in ['active', 'closed', 'report'] and status == \
            'testing':
        return 'Sorry! Status change failed'
    election.status = status
    dbsession.add(election)
    dbsession.commit()
    set_history('Edit', 'set election status to: '+status, current_user.name)
    return 'Status change is successful'


def get_elections(eid=None):
    if eid is None:
        return (dbsession.query(Election)
                .filter_by(createdby=current_user.creator).all())
    return (dbsession.query(Election)
            .filter_by(createdby=current_user.creator)
            .filter_by(id=eid).first())


def handle_exception(name):
    dbsession.add(name)
    dbsession.flush()
    pass


def get_elector_status(elector_id, election_id):
    result = (dbsession.query(Vote).filter_by(elector_id=elector_id)
              .filter_by(election_id=election_id)
              .first()
              )
    return result.status if result is not None else 'inactive'


def get_election_portfolios(election_id, status):
    '''
    if status == 'voted':
        return 'voted'
    '''
    query = dbsession.execute(
        "select elections.portfolio_"+status+" from elections where id=:id",
        {'id': election_id}).first()
    return query[0]


def check_elector_votes_record(elector_id, election_id):
    count = Vote.query.filter_by(election_id=election_id) \
        .filter_by(elector_id=elector_id).count()
    if not count:
        add_new_record_to_votes(elector_id, election_id)
        set_history('activation', 'activated voter with id: '+elector_id,
                    current_user.name)
        return 'Voter Successfully Activated'

    return 'Voter already activated'


def casting_vote(elector_id, election_id, cid=None):
    elector_status = ''
    next_portfolio = ''
    check_record = (Vote.query.filter_by(election_id=election_id)
                    .filter_by(elector_id=elector_id).count())
    if check_record is 0:
        add_new_record_to_votes(elector_id, election_id)
        elector_status = get_elector_status(elector_id, election_id)
        next_portfolio = get_election_portfolios(
            election_id, elector_status)
        return next_portfolio

    else:
        elector_status = get_elector_status(elector_id, election_id)
        update_elector_status(elector_id, election_id, elector_status, cid)

        if elector_status == 'voted':
            return 'voted'
        get_next_portfolio = get_election_portfolios(
            election_id, str(int(elector_status)+1))
        return get_next_portfolio


def update_elector_status(elector_id, election_id, status, cid):
    if status == 'voted':
        return
    dbsession.query(Vote).filter_by(elector_id=elector_id).filter_by(
        election_id=election_id).update(
            {'portfolio_'+status: cid, 'status': int(status)+1})
    dbsession.commit()


def set_status_as_voted(elector_id, election_id):
    obj = Vote.query.filter_by(elector_id=elector_id).filter_by(
        election_id=election_id).first()
    obj.status = 'voted'
    dbsession.add(obj)
    dbsession.commit()


def add_new_record_to_votes(elector_id, election_id):
    add_record = Vote()
    add_record.elector_id = elector_id
    add_record.election_id = election_id
    dbsession.add(add_record)
    dbsession.commit()


def get_active_election(account, school):
    department_election = (dbsession.query(Election)
                           .filter(Election.status.in_(['active', 'testing']),
                                   Election.createdby == account,
                                   Election.scope == 'dep',
                                   Election.date == date.today())
                           .first()
                           )
    src_election = (dbsession.query(Election)
                    .filter(Election.status.in_(['active', 'testing']),
                            Election.scope == 'src',
                            Election.date == date.today())
                    .first()
                    )
    return department_election or src_election or None


def validate_vote_url(elector_id, election_id):
    status = get_elector_status(elector_id, election_id)
    if status == 'voted':
        return 'voted'
    portfolio = get_election_portfolios(election_id, status)

    return portfolio


def count_votes(candidate_id, portfolio_id, election_id):
    if 'all' in candidate_id:
        return (dbsession.execute(
            'SELECT count(portfolio_'+portfolio_id+') \
            FROM votes WHERE election_id=:election_id',
            {'election_id': election_id})).first()[0]

    return (dbsession.execute(
        'SELECT count(portfolio_'+portfolio_id+') FROM votes WHERE election_id\
        =:election_id and portfolio_' + portfolio_id+'=:candidate_id',
        {'election_id': election_id, 'candidate_id': candidate_id})).first()[0]


def report_election(school, scope, election_id, pid=None, portfolio=None):
    candidates = get_candidates_by(school, scope,
                                   election_id, portfolio)
    # return [c.Portfolio.id for c in candidates]
    if pid is not None:
        return [[c, count_votes(str(c.Candidate.id), pid, c.Election.id)]
                for c in candidates]

    return [[c, count_votes(str(c.Candidate.id), str(c.Candidate.portfolio_id),
                            c.Election.id)] for c in candidates]


def registered_electors():
    return (dbsession.query(Elector, Account)
            .filter_by(createdby=current_user.creator)
            .join(Account)
            .filter_by(id=Elector.createdby)
            .count()
            ) if current_user.department not in 'src' else \
        (dbsession.query(Elector, Account)
            .join(Account)
            .filter_by(id=Elector.createdby)
            .filter_by(institution=current_user.school)
            .count()
         )


def elector_turnout(election_id):
    return (dbsession.query(Vote).filter_by(election_id=election_id).count())


def edit_elector_info(elector_id, form):
    elector = Elector.query.filter_by(id=elector_id).first()
    elector.first_name = form.first_name.data
    elector.last_name = form.last_name.data
    # elector.phone = form.mobile.data
    elector.email = form.email.data
    elector.level = form.level.data
    dbsession.add(elector)
    dbsession.commit()
    set_history('Edit', 'Edited voter with id: '+elector_id, current_user.name)
    flash('Info successfully edited')


def edit_account_info(account_id, form):
    account = Account.query.filter_by(id=account_id).first()
    if account.verify_password(form.old_password.data):
        account.password = form.new_password.data
        dbsession.add(account)
        dbsession.commit()
        flash(u'Password change is successful', 'success')
    else:
        flash(u'Old password doesn\'t match', 'error')


def generate_password(id):
    password = (PasswordGenerator().of().between(2, 3, 'letters')
                .at_least(2, 'numbers')
                .length(5)
                .beginning_with('letters')
                .done()).generate()
    elector = Elector.query.filter_by(id=id).first()
    elector.password = password
    dbsession.add(elector)
    dbsession.commit()
    return password


def activate(id):
    elector = Elector.query.filter_by(id=id).first()
    elector.status = '0'
    dbsession.add(elector)
    dbsession.commit()
    set_history('activation', 'activated voter with id: '+id, current_user.id)


def elector_view(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'vote':
            flash('You are not logged in as a Voter')
            return redirect(url_for('auth.logout'))
        return f(*args, **kwargs)
    return decorated_function


def admin_view(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role not in ['root', 'admin', 'user', 'strongroom']:
            flash('You are not allowed to access the page you tried to view')
            return redirect(url_for('auth.logout'))
        return f(*args, **kwargs)
    return decorated_function


def user_view(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role not in ['root', 'admin', 'user']:
            flash('You are not allowed to access the page you tried to view')
            return redirect(url_for('auth.logout'))
        return f(*args, **kwargs)
    return decorated_function


def strongroom_view(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role not in ['root', 'admin', 'strongroom']:
            flash('You are not allowed to access the page you tried to view')
            return redirect(url_for('auth.logout'))
        return f(*args, **kwargs)
    return decorated_function
