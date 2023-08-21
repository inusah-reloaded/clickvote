from flask import render_template, Blueprint, flash,\
         jsonify, redirect, request, url_for, json
from flask_login import current_user

from .forms import AddVoterForm, EditVoterForm, SearchForm, \
    ImportFromCSVForm, AddUserForm, EditUserForm, AddCandidateForm, \
    CreateElectionForm, EditAccountForm, EditElectionForm, EditCandidateForm



from .helpers import add_new_voter, add_new_user, add_new_candidate,\
    import_from_csv, get_voter_details, get_candidates, get_users,\
    delete_candidate, delete_elector, get_candidates_by, create_elections,\
    get_elections, casting_vote, set_status_as_voted, validate_vote_url, \
    selected_candidates, get_all_portfolios, count_votes, report_election, \
    registered_electors, elector_turnout, edit_election_status, \
    elector_view, admin_view, strongroom_view, user_view, \
    edit_elector_info, edit_user_info, delete_user, get_elector_status, \
    edit_account_info, check_elector_votes_record, get_history, \
    delete_election, edit_elections, get_portfolios, get_portfolios_edit, edit_candidate_info
from flask_wtf.csrf import CSRFError
from flask_login import login_required

clickvote = Blueprint('clickvote', __name__)


@clickvote.errorhandler(CSRFError)
def handle_csrf_error(e):
    return jsonify(e.description)


@clickvote.route('/')
@login_required
@admin_view
def console():
    return render_template('clickvote/console.html')


# views for Voters
@clickvote.route('/voters/summary/')
@login_required
@admin_view
def voters_summary():
    return render_template('clickvote/voters/voters_summary.html')


@clickvote.route('/voters/add/', methods=['GET', 'POST'])
@login_required
@admin_view
def add_voter():
    add_form = AddVoterForm()
    if add_form.validate_on_submit():
        add_new_voter(add_form)
    return render_template('clickvote/voters/add_voters.html', add_form=add_form)


@clickvote.route('/voters/importcsv/', methods=['POST', 'GET'])
@login_required
@admin_view
def import_csv():
    form = ImportFromCSVForm()

    if form.validate_on_submit():
        import_from_csv(form)
    return render_template('clickvote/voters/import_csv.html', form=form)


@clickvote.route('/voters/edit/<id>/',  methods=['GET', 'POST'])
@login_required
@admin_view
def edit_voter(id):
    voter = get_voter_details(id)
    form = EditVoterForm()
    if form.validate_on_submit():
        edit_elector_info(id, form)

    return render_template(
        'clickvote/voters/edit_voter.html', form=form, voter=voter)


@clickvote.route('/voters/search/', methods=['GET', 'POST'])
@login_required
@user_view
def search_for_voter():
    form = SearchForm()
    voter = ''
    if request.method == 'POST' and 'id' in request.form:
        elector_id = request.form['id']
        if 'delete' in request.form['action']:
            delete_elector(elector_id)
            return jsonify('successfully deleted '+elector_id)
        if 'password_gen' in request.form['action']:
            # generate password
            # password = generate_password(elector_id)
            status = check_elector_votes_record(elector_id,
                                                request.form['election_id'])
            # return generated password
            return status

    if form.validate_on_submit():
        voter = get_voter_details(form.identifier.data)
    return render_template(
        'clickvote/voters/search_for_voter.html', form=form, result=voter)


# views for Users
@clickvote.route('/users/list/', methods=['GET', 'POST'])
@login_required
@admin_view
def user_list():
    form = SearchForm()
    users = get_users()
    if request.method == 'POST':
        delete_user(request.form.get('id'))
    return render_template(
        'clickvote/users/user_list.html', form=form, results=users)


@clickvote.route('/history/', methods=['GET', 'POST'])
@login_required
@admin_view
def history():
    form = SearchForm()
    history = get_history()
    if form.validate_on_submit():
        history = get_history(form.identifier.data)
    return render_template(
        'clickvote/history.html', form=form, results=history)


@clickvote.route('/users/add/', methods=['GET', 'POST'])
@login_required
@admin_view
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        add_new_user(form)

    return render_template('clickvote/users/add_users.html', form=form)


@clickvote.route('/users/edit/<user_id>/', methods=['GET', 'POST'])
@login_required
@admin_view
def edit_user(user_id):
    user = ''
    form = EditUserForm()
    user = get_users(user_id)
    if form.validate_on_submit():
        edit_user_info(user_id, form)
        return redirect(url_for('clickvote.user_list'))
    return render_template('clickvote/users/edit_user.html', form=form, user=user)


@clickvote.route('/candidates/list/', methods=['GET', 'POST'])
@login_required
@admin_view
def candidate_list():
    form = SearchForm()
    candidates = get_candidates()
    if request.method == 'POST' and 'id' in request.form:
        if request.form['action'] == 'delete':
            delete_candidate(request.form['id'])
            return 'Successfully deleted'
        elif request.form['action'] == 'view':
            info = get_candidates(request.form['id'])
            json_obj = {
                'cid': info.Candidate.candidate_id,
                'first_name': info.Elector.first_name,
                'last_name': info.Elector.last_name,
                'portfolio': get_portfolios(info.Candidate.portfolio_id),
                'phone': info.Elector.phone,
                'photo': info.Candidate.photo
            }
            return json.dumps(json_obj)
    return render_template(
        'clickvote/candidates/candidate_list.html',
        form=form, results=candidates)


@clickvote.route('/candidates/add/', methods=['GET', 'POST'])
@login_required
@admin_view
def add_candidate():
    form = AddCandidateForm()
    if form.validate_on_submit():
        add_new_candidate(form)
    return render_template('clickvote/candidates/add_candidate.html', form=form)


@clickvote.route('/candidates/edit/<id>/', methods=['GET', 'POST'])
@login_required
@admin_view
def edit_candidate(id):
    candidate = get_candidates(id)
    form = EditCandidateForm(portfolio=int(candidate.Candidate.portfolio_id))
    form.portfolio.choices = get_portfolios_edit()
    # form.portfolio.default = int(candidate.Candidate.portfolio_id)
    # form.process()
    if form.validate_on_submit():
        edit_candidate_info(id, form)
    return render_template('clickvote/candidates/edit_candidate_info.html',
                           form=form, results=candidate)


@clickvote.route('/vote/<school>/<scope>/<election>/<portfolio>/',
               defaults={'department': None}, methods=['GET', 'POST'])
@clickvote.route('/vote/<school>/<scope>/<department>/<election>/<portfolio>/',
               methods=['GET', 'POST'])
@login_required
@elector_view
def vote(school, scope, department, election, portfolio):
    if portfolio == validate_vote_url(current_user.user_id, election):
        candidates = get_candidates_by(school,
                                       scope, election, portfolio)

        if request.method == 'POST' and 'crid' in request.form:
            candidate_real_id = request.form['crid']
            elector_id = request.form['sid']
            election_id = request.form['eid']

            portfolio = casting_vote(elector_id, election_id, candidate_real_id)
            if portfolio in ['Select Portfolio', 'voted']:
                set_status_as_voted(elector_id, election_id)
                # flash('You have finished voting')
                return url_for('clickvote.vote_summary', school=school,
                               scope=scope, department=department,
                               election=election)

            return url_for('clickvote.vote', school=school, scope=scope,
                           department=department, election=election,
                           portfolio=portfolio)

        return render_template('clickvote/vote.html', results=candidates,
                               election=election)
    flash('You tried jumping foward or backward. allow the system to guide you')
    return url_for('auth.logout')


@clickvote.route('/vote/summary/<school>/<scope>/<election>/',
               defaults={'department': None}, methods=['GET', 'POST'])
@clickvote.route('/vote/summary/<school>/<scope>/<department>/<election>/',
               methods=['GET', 'POST'])
@login_required
@elector_view
def vote_summary(school, scope, department, election):
    result = selected_candidates(election)

    return render_template('clickvote/vote_summary.html', result=result)


@clickvote.route('/vote/report/<school>/<scope>/<election>/<pid>/<portfolio>/',
               methods=['GET', 'POST'])
@login_required
@admin_view
def election_report(school, scope, election, pid, portfolio):
    portfolios = get_all_portfolios(election)
    if request.method == 'POST' and 'id' in request.form \
            and 'portfolio' in request.form:
        portfolio = request.form.get('portfolio')
        pid = request.form.get('id')
        return url_for('clickvote.election_report',
                       school=school, scope=scope,
                       election=election,
                       pid=pid, portfolio=portfolio)

    report = report_election(school, scope, election, str(pid), portfolio)
    if 'Summary' not in portfolio:
        skip_count = count_votes('skip', str(pid), election)
        no_count = count_votes('no', str(pid), election)
        total_votes = count_votes('all', str(pid), election)
        return render_template('clickvote/election_report.html',
                               portfolios=portfolios, report=report,
                               skip_count=skip_count, total_votes=total_votes,
                               no_count=no_count)

    total_registered = registered_electors()
    turnout = elector_turnout(election)
    return render_template('clickvote/election_report_summary.html',
                           portfolios=portfolios, registered=total_registered,
                           turnout=turnout)


@clickvote.route('/vote/strongroom/<school>/<scope>/<election>/',
               methods=['GET', 'POST'])
@login_required
@strongroom_view
def strongroom(school, scope, election):
    total_registered = registered_electors()
    turnout = elector_turnout(election)

    return render_template('clickvote/strongroom.html',
                           total_registered=total_registered, turnout=turnout)


@clickvote.route('/cast_vote/', methods=['POST'])
@elector_view
@login_required
def cast_vote():
    if request.method == 'POST':
        candidate_real_id = request.form['crid']
        elector_id = request.form['sid']
        election_id = request.form['eid']
        casting_vote(elector_id, election_id, candidate_real_id)


@clickvote.route('/settings/')
@login_required
@admin_view
def settings():
    return render_template('clickvote/settings/settings.html')


@clickvote.route('/settings/elections/', methods=['GET', 'POST'])
@login_required
@admin_view
def elections():

    form = SearchForm()
    elections = get_elections()
    if request.method == 'POST' and 'id' in request.form:

        if request.form['selection'] in 'delete':
            delete_election(request.form['id'])
            return 'record deleted!'
        else:
            state = edit_election_status(request.form['id'],
                                         request.form['selection'])
            return state
    return render_template('clickvote/settings/elections.html',
                           form=form, results=elections)


@clickvote.route('/settings/elections/edit/<id>/',  methods=['GET', 'POST'])
@login_required
@admin_view
def edit_election(id):
    election = get_elections(id)
    form = EditElectionForm()
    if form.validate_on_submit():
        edit_elections(id, form)

    return render_template(
        'clickvote/settings/edit_election.html', form=form,
        election_id=election.id)


@clickvote.route('/settings/elections/create/', methods=['GET', 'POST'])
@login_required
@admin_view
def create_election():
    form = CreateElectionForm()
    if form.validate_on_submit():
        return "Validated"
        create_elections(form)

    return render_template('clickvote/settings/create_election.html', form=form)


@clickvote.route('/settings/account/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditAccountForm()
    if form.validate_on_submit():
        edit_account_info(current_user.user_id, form)
    return render_template('clickvote/settings/edit_profile.html', form=form)


@clickvote.context_processor
def util_processor():
    return dict(get_all_portfolios=get_all_portfolios,
                report_election=report_election,
                get_elector_status=get_elector_status,
                get_elections=get_elections, get_candidates=get_candidates)
