# -- coding: utf-8 --
from flask import current_app, render_template, request, redirect, make_response, flash, session
from . import brigade as app
from . import github
from datetime import datetime
from flask.ext.github import GitHubError
from operator import itemgetter
from requests import get, post
from urlparse import urlparse
import base64
import json
import re
import logging
import time

# Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
requests_logger = logging.getLogger("requests")
requests_logger.setLevel(logging.WARNING)

CIVIC_JSON_PR_TITLE = u'Adds a civic.json file'
CIVIC_JSON_BRANCH_NAME = u'add-civic-json-file'
CIVIC_JSON_PR_MESSAGE_TEMPLATE = u'''Hi! Merge this PR to add a civic.json file to your project. This little bit of metadata will make your project easier to find with [Code for America's project search](https://www.codeforamerica.org/brigade/projects) by adding **tags** and **status**. You can [read more about what the status means here](https://www.codeforamerica.org/brigade/projects/stages). If you have questions about any of this just ping me, @{user_login}. :raised_hands:'''

@app.context_processor
def get_fragments():
    ''' The base template includes the signup form and the footer
        pulled from our main site.
    '''
    # Get universal sign up form
    r = get("http://www.codeforamerica.org/fragments/email-signup.html")
    signup = r.content

    # Get footer html
    r = get("http://www.codeforamerica.org/fragments/global-footer.html")
    footer = r.content
    return dict(signup=signup, footer=footer)


def get_brigades():
    # Get location of all civic tech orgs
    got = get("https://www.codeforamerica.org/api/organizations.geojson")
    geojson = got.json()
    brigades = []

    # Prepare the geojson for a map
    for org in geojson["features"]:
        # Add icon info for the map
        org["properties"]["marker-symbol"] = "town-hall"
        # Official Brigades get to be red
        if "Official" in org["properties"]["type"]:
            org["properties"]["marker-color"] = "#aa1c3a"
        else:
            # Other Brigades are grey
            org["properties"]["marker-color"] = "#6D6E71"
        # Grab only orgs with type Brigade
        if "Brigade" in org["properties"]["type"]:
            brigades.append(org)

    brigades = json.dumps(brigades)
    return brigades


def is_existing_organization(orgid):
    ''' tests that an organization exists on the cfapi'''
    got = get("https://www.codeforamerica.org/api/organizations.geojson").json()
    orgids = [org["properties"]["id"] for org in got["features"]]
    return orgid in orgids


def get_projects(projects, url, limit=10):
    ''' Load projects from the cfapi
    '''
    got = get(url)
    new_projects = got.json()["objects"]
    projects = projects + new_projects
    if limit:
        if len(projects) >= limit:
            return projects
    if "next" in got.json()["pages"]:
        projects = get_projects(projects, got.json()["pages"]["next"], limit)
    return projects


def get_project_for_civic_json(brigadeid, project_name):
    ''' Get and format a project object for use in the 'add-civic-json' routes.
    '''
    got = get("https://www.codeforamerica.org/api/projects?name={}&organization_id={}".format(project_name, brigadeid))
    # In rare cases there may be more than one. Use the first matching project.
    project = got.json()["objects"][0]
    project["repo"] = None
    if project["code_url"]:
        url = urlparse(project["code_url"])
        if url.netloc == 'github.com':
            project["repo"] = url.path.lstrip("/")

    return project


def get_github_user():
    ''' Get GitHub user information from the GitHub API
    '''
    user = None
    if session.get("access_token"):
        user = github.get("user")

    return user


def process_tags(tags):
    ''' Take a string that's a comma-separated list of tags,
        strip spaces, drop empties, dedupe, return as list.
    '''
    if not tags:
        return None

    # split and drop empties
    tags = [tag.strip() for tag in tags.split(',') if len(tag.strip()) != 0]
    if not len(tags):
        return None

    # dedupe and return
    # source: http://stackoverflow.com/a/480227/958481
    seen = set()
    seen_add = seen.add
    return [tag for tag in tags if not (tag in seen or seen_add(tag))]

def make_civic_json():
    ''' Take form data from the request context and return a json object.
    '''
    # Get status from the form
    status = request.form.get("status", None)
    if status:
        if len(status.strip()) == 0 or status == u'Choose a status':
            status = None

    # Get tags from the form
    tags = process_tags(request.form.get("tags", None))

    # Return None if there's no info to capture
    if not status and not tags:
        return None

    civic_json = {}
    if status:
        civic_json["status"] = status
    if tags:
        civic_json["tags"] = tags

    return u'{}\n'.format(json.dumps(civic_json, indent=4, ensure_ascii=False)).encode('utf8')

def civic_json_pull_request_exists(project, user):
    ''' Check for an existing civic.json pull request.
    '''
    try:
        response = github.get("repos/{}/pulls".format(project["repo"]))
    except GitHubError:
        raise

    for pr in response:
        if pr["title"] == CIVIC_JSON_PR_TITLE and pr["user"]["login"] == user["login"]:
            return True

    return False

def user_has_push_access(project, response=None):
    ''' Check whether the user has push access to this project.
    '''
    if not response:
        try:
            response = github.get("repos/{}".format(project["repo"]))
        except GitHubError:
            return False

    return 'permissions' in response and 'push' in response['permissions'] and response['permissions']['push']

def get_repo_default_branch(project, response=None, default="master"):
    ''' Get the name of the project's default branch.
    '''
    if not response:
        try:
            response = github.get("repos/{}".format(project["repo"]))
        except GitHubError:
            return default

    if 'default_branch' in response:
        return response['default_branch']
    else:
        return default

def civic_json_branch_exists(project):
    ''' The branch for adding a civic.json file exists on this project's repo.
    '''
    try:
        github.get("repos/{}/git/refs/heads/{}".format(project["repo"], CIVIC_JSON_BRANCH_NAME))
    except GitHubError:
        return False

    return True

def create_civic_json_branch(project):
    ''' Create a branch for adding a civic.json file to a project.
    '''
    # get the sha of the master branch
    try:
        response = github.get("repos/{}/git/refs/heads/master".format(project["repo"]))
    except GitHubError:
        raise
    master_sha = response['object']['sha']

    # create a new branch
    try:
        github.post("repos/{}/git/refs".format(project["repo"]), data=dict(ref="refs/heads/{}".format(CIVIC_JSON_BRANCH_NAME), sha=master_sha))
    except GitHubError:
        raise

def create_civic_json_fork(project):
    ''' Create a fork for adding a civic.json file to a project.
    '''
    # Fork the repo. Succeeds even if fork already exists.
    try:
        response = github.post("repos/{}/forks".format(project["repo"]), data=None)
    except GitHubError:
        raise

    return response

def verify_civic_json_fork(forked_repo_name, call_limit=10):
    ''' Verify that the passed repo exists.
    '''
    repo_exists = False
    times_called = 0
    error_message = u"Couldn't verify the forked repo on GitHub."
    while not repo_exists:
        times_called = times_called + 1
        # timeout if it's been too long
        if times_called > call_limit:
            logging.error(u"Fork at repos/{} doesn't exist after {} seconds.".format(forked_repo_name, call_limit))
            return False, error_message

        try:
            github.get("repos/{}".format(forked_repo_name))

        except GitHubError as e:
            # error if we got a status_code other than 404
            if e.response.status_code != 404:
                logging.error(u"GitHub error {} ({}) when checking for existence of repos/{}.".format(e.response.status_code, e.response.json()['message'], forked_repo_name))
                return False, error_message

            # wait a second before trying again
            time.sleep(1)

        else:
            repo_exists = True

    return True, u""

def get_civic_json_sha(repo_name, payload=None):
    ''' Get the sha for a civic.json file in the passed repo.
    '''
    try:
        response = github.get("repos/{}/contents/civic.json".format(repo_name), params=payload)
        return response["sha"]
    except GitHubError:
        return None

def commit_civic_json(civic_json, repo_name, ref_payload):
    ''' Commit the civic.json file to the passed repo.
    '''
    # if there's already a civic.json, get its sha
    civic_sha = get_civic_json_sha(repo_name, ref_payload)

    # Build the commit data object
    data = {
        "message": "add civic.json file",
        "content": base64.b64encode(civic_json)
    }
    if civic_sha:
        data["sha"] = civic_sha
    if ref_payload:
        data["branch"] = ref_payload["ref"]

    try:
        github.request("PUT", "repos/{}/contents/civic.json".format(repo_name), data=json.dumps(data))
    except GitHubError:
        raise

#
# ROUTES
#

@app.route('/brigade/list', methods=["GET"])
def brigade_list():
    brigades = get_brigades()
    brigades = json.loads(brigades)
    brigades.sort(key=lambda x: x['properties']['city'])
    return render_template("brigade_list.html", brigades=brigades)


@app.route('/brigade/')
def index():
    brigades = get_brigades()
    return render_template("index.html", brigades=brigades)


@app.route("/brigade/signup/", methods=["POST"])
def signup():
    ''' Takes in signup requests from /brigade/signup/form
        Sends the data to a requested mailchimp list, our mailchimp list, and the peopledb
    '''

    # Prep mailchimp data
    # mailchimp_data = {
    #     'FNAME' : request.form.get("FNAME"),
    #     'LNAME' : request.form.get("LNAME"),
    #     'EMAIL' : request.form.get("EMAIL")
    #     }

    # Optionally POST to Brigade's mailchimp
    # mailchimp_url = request.form.get("mailchimp_url", None)
    # brigade_mailchimp_response = None
    # if mailchimp_url:
    #     brigade_mailchimp_response = post(mailchimp_url, data=mailchimp_data)

    # Always POST to Code for America's mailchimp
    # mailchimp_data['group[10273][8192]'] = '8192' # I attend Brigade events

    # cfa_mailchimp_url = "http://codeforamerica.us2.list-manage.com/subscribe/post-json?u=d9acf2a4c694efbd76a48936f&amp;id=3ac3aef1a5"
    # cfa_mailchimp_response = post(cfa_mailchimp_url, data=mailchimp_data)

    # Always POST to PeopleDB
    peopledb_data = {
        'first_name': request.form.get("FNAME"),
        'last_name': request.form.get("LNAME"),
        'email': request.form.get("EMAIL"),
        'brigade_id': request.form.get("brigade_id", None)
    }

    auth = current_app.config['BRIGADE_SIGNUP_SECRET'], 'x-brigade-signup'
    url = 'https://people.codeforamerica.org/brigade/signup'

    peopledb_response = post(url, data=peopledb_data, auth=auth)

    # Choose a response to show
    # if brigade_mailchimp_response:
    #     return brigade_mailchimp_response

    # elif cfa_mailchimp_response:
    #     return cfa_mailchimp_response.content

    if peopledb_response:
        response = {
            "status_code": peopledb_response.status_code,
            "msg": peopledb_response.content
        }
        return json.dumps(response)

    else:
        response = {
            "status_code": 500,
            "msg": "Something went wrong. You were not added to any lists."
        }
        return response


@app.route("/brigade/signup/", methods=["GET"])
def signup_form():
    # Get all of the organizations from the api
    organizations = get('https://www.codeforamerica.org/api/organizations.geojson')
    organizations = organizations.json()

    # Filter out just the organization names
    brigades = []
    for org in organizations['features']:
        brigades.append(org['properties']['name'])

    # Alphabetize names
    brigades.sort()

    return render_template("signup.html", brigades=brigades)


@app.route("/brigade/numbers/")
def numbers():
    # Get the total number of Brigades
    got = get("https://www.codeforamerica.org/api/organizations?type=Brigade&per_page=1")
    got = got.json()
    brigades_total = got['total']

    # Get the official Brigades
    got = get("https://www.codeforamerica.org/api/organizations?type=Official&per_page=1")
    got = got.json()
    official_brigades_total = got['total']

    # Get the total number of Code for All Groups
    got = get("https://www.codeforamerica.org/api/organizations?type=Code for All&per_page=1")
    got = got.json()
    cfall_total = got['total']

    # Get the total number of Government Groups
    got = get("https://www.codeforamerica.org/api/organizations?type=Government&per_page=1")
    got = got.json()
    government_total = got['total']

    # Get number of meetup-members
    got = get("http://codeforamerica.org/api/organizations/member_count")
    got = got.json()
    member_count = got['total']

    # Get number of RSVPs
    got = get("https://www.codeforamerica.org/api/events/rsvps")
    got = got.json()
    rsvps = got['total']

    # Get number of Attendance
    got = get("https://www.codeforamerica.org/api/attendance")
    got = got.json()
    attendance = got['total']

    # Get total number of projects
    got = get("https://www.codeforamerica.org/api/projects?only_ids&per_page=1")
    got = got.json()
    projects_total = got['total']

    # Get total number of Brigade projects
    got = get("https://www.codeforamerica.org/api/projects?only_ids&organization_type=Brigade&per_page=1")
    got = got.json()
    brigade_projects_total = got['total']

    # Get total number of Code for All projects
    got = get("https://www.codeforamerica.org/api/projects?only_ids&organization_type=Code for All&per_page=1")
    got = got.json()
    cfall_projects_total = got['total']

    # Get total number of Government projects
    got = get("https://www.codeforamerica.org/api/projects?only_ids&organization_type=Government&per_page=1")
    got = got.json()
    gov_projects_total = got['total']

    # Get number of Issues
    got = get("https://www.codeforamerica.org/api/issues?per_page=1")
    got = got.json()
    issues_total = got['total']

    # Get number of Help Wanted Issues
    got = get("https://www.codeforamerica.org/api/issues/labels/help%20wanted?per_page=1")
    got = got.json()
    help_wanted_total = got['total']

    # Get number of civic issue finder clicks
    got = get("https://www.codeforamerica.org/geeks/civicissues/analytics/total_clicks")
    got = got.json()
    total_issue_clicks = got['total_clicks']

    kwargs = dict(brigades_total=brigades_total, official_brigades_total=official_brigades_total,
                  cfall_total=cfall_total, government_total=government_total,
                  member_count=member_count, rsvps=rsvps, attendance=attendance,
                  projects_total=projects_total, brigade_projects_total=brigade_projects_total,
                  cfall_projects_total=cfall_projects_total, gov_projects_total=gov_projects_total,
                  issues_total=issues_total, help_wanted_total=help_wanted_total, total_issue_clicks=total_issue_clicks)

    return render_template("numbers.html", **kwargs)


@app.route("/brigade/about/")
def about():
    return render_template("about.html")


@app.route("/brigade/organize/")
@app.route("/brigade/organize/<page>/")
def organize(page=None):
    if page:
        return render_template("organize/" + page + ".html")
    else:
        return render_template("organize/index.html")

@app.route("/brigade/tools/")
@app.route("/brigade/tools/<page>/")
def tools(page=None):
    if page:
        return render_template("tools/" + page + ".html")
    else:
        return render_template("tools/index.html")


@app.route("/brigade/infrastructure")
def infrastructure():
    return redirect("brigade/tools/infrastructure")


@app.route("/brigade/projects/stages")
def stages():
    ''' Describe the project stages '''
    got = get("https://www.codeforamerica.org/api/projects?status=experiment")
    experiment_count = got.json()["total"]
    got = get("https://www.codeforamerica.org/api/projects?status=alpha")
    alpha_count = got.json()["total"]
    got = get("https://www.codeforamerica.org/api/projects?status=beta")
    beta_count = got.json()["total"]
    got = get("https://www.codeforamerica.org/api/projects?status=official")
    official_count = got.json()["total"]
    return render_template("stages.html", experiment_count=experiment_count, alpha_count=alpha_count, beta_count=beta_count, official_count=official_count)


@app.route("/brigade/projects")
@app.route("/brigade/<brigadeid>/projects")
def projects(brigadeid=None):
    ''' Display a list of projects '''

    # is this an exisiting group
    if brigadeid:
        if not is_existing_organization(brigadeid):
            return render_template('404.html'), 404

    # Get the params
    projects = []
    brigade = None
    search = request.args.get("q", None)
    sort_by = request.args.get("sort_by", None)
    page = request.args.get("page", None)
    organization_type = request.args.get("organization_type", None)

    # Set next
    if page:
        if brigadeid:
            next = "/brigade/" + brigadeid + "/projects?page=" + str(int(page) + 1)
        else:
            next = "/brigade/projects?page=" + str(int(page) + 1)
    else:
        if brigadeid:
            next = "/brigade/" + brigadeid + "/projects?page=2"
        else:
            next = "/brigade/projects?page=2"

    # build the url
    if brigadeid:
        url = "https://www.codeforamerica.org/api/organizations/" + brigadeid + "/projects"
        # set the brigade name
        if projects:
            brigade = projects[0]["organization"]
        else:
            brigade = {"name": brigadeid.replace("-", " ")}
    else:
        url = "https://www.codeforamerica.org/api/projects"
    if search or sort_by or page or organization_type:
        url += "?"
    if search:
        url += "&q=" + search
    if sort_by:
        url += "&sort_by" + sort_by
    if page:
        url += "&page=" + page
    if organization_type:
        url += "&organization_type=" + organization_type

    projects = get_projects(projects, url)

    return render_template("projects.html", projects=projects, brigade=brigade, next=next)

@app.route('/brigade/github-callback')
@github.authorized_handler
def authorized(access_token):
    if 'error' in request.args:
        error_message = request.args['error_description']
        return render_template("civic_json.html", error=error_message, project=None, user=None)

    session['access_token'] = access_token
    return redirect(request.args.get("redirect_uri"))

@github.access_token_getter
def token_getter():
    return session['access_token']

@app.route("/brigade/gh-login")
def github_login():
    netloc = urlparse(request.base_url).netloc
    redirect_uri = "http://{}/brigade/github-callback?redirect_uri={}".format(netloc, request.referrer)
    return github.authorize(scope="public_repo", redirect_uri=redirect_uri)

@app.route("/brigade/gh-logout")
def github_logout():
    ''' Destroy the local GitHub access token and redirect
    '''
    if session.get("access_token"):
        session.pop("access_token", None)
    return redirect(urlparse(request.referrer).path)

@app.route("/brigade/<brigadeid>/projects/<project_name>/add-civic-json", methods=["GET"])
def show_civic_json_page(brigadeid, project_name):
    ''' Show the 'add civic json' page
    '''
    # Get information about the relevant project from the cfapi
    project = get_project_for_civic_json(brigadeid, project_name)
    user = get_github_user()
    pr_message = CIVIC_JSON_PR_MESSAGE_TEMPLATE.format(user_login=user['login']) if user and 'login' in user else u''
    return render_template("civic_json.html", project=project, user=user, pr_message=pr_message)

@app.route("/brigade/<brigadeid>/projects/<project_name>/add-civic-json", methods=["POST"])
def create_civic_json(brigadeid, project_name):
    ''' Send a pull request to a project to add a civic.json file.
    '''

    # Get information about the relevant project from the cfapi
    project = get_project_for_civic_json(brigadeid, project_name)
    user = get_github_user()

    # create a civic.json object
    civic_json = make_civic_json()
    if not civic_json:
        error_message = u'Please enter status and/or tags for the project!'
        return render_template("civic_json.html", error=error_message, project=project, user=user)

    # Check whether a pull request with this title and from this user already exists
    try:
        pr_exists = civic_json_pull_request_exists(project, user)
    except GitHubError as e:
        error_message = e.response.json()['message']
        return render_template("civic_json.html", error=error_message, project=project, user=user)
    # Redirect to the pull requests for the project if the pr exists
    if pr_exists:
        return redirect("{}/pulls".format(project["code_url"]))

    # Branch if the user has push access to the repo
    has_push_access = True
    pull_base = None
    try:
        get_repo_response = github.get("repos/{}".format(project["repo"]))
    except GitHubError:
        has_push_access = False
    else:
        has_push_access = user_has_push_access(project, get_repo_response)

    if has_push_access and not civic_json_branch_exists(project):
        try:
            create_civic_json_branch(project)
        except GitHubError as e:
            error_message = e.response.json()['message']
            logging.error(u"GitHub error {} ({}) when trying to create a branch at repos/{}/git/refs/heads/{}.".format(e.response.status_code, error_message, project["repo"], CIVIC_JSON_BRANCH_NAME))

        ref_payload = {u'ref': CIVIC_JSON_BRANCH_NAME}
        repo_name = project["repo"]
        pull_head = CIVIC_JSON_BRANCH_NAME
        pull_base = get_repo_default_branch(project, get_repo_response)

    # Otherwise, fork the repo.
    else:
        try:
            response = create_civic_json_fork(project)
        except GitHubError as e:
            error_message = e.response.json()['message']
            logging.error(u"GitHub error {} ({}) when making a fork at repos/{}/forks.".format(e.response.status_code, error_message, project["repo"]))
            return render_template("civic_json.html", error=error_message, project=None, user=None)

        fork_exists, error_message = verify_civic_json_fork(response["full_name"])
        if not fork_exists:
            return render_template("civic_json.html", error=error_message, project=None, user=None)

        ref_payload = None
        repo_name = response["full_name"]
        pull_head = u"{}:{}".format(response["owner"]["login"], response["default_branch"])
        pull_base = response["default_branch"]

    # commit the civic.json to the branch or fork
    try:
        commit_civic_json(civic_json, repo_name, ref_payload)
    except GitHubError as e:
        error_message = e.response.json()['message']
        logging.error(u"GitHub error {} ({}) when adding civic.json file at repos/{}/contents/civic.json.".format(e.response.status_code, error_message, repo_name))
        return render_template("civic_json.html", error=error_message, project=None, user=None)

    # Send a pull request
    pr_message = request.form.get("pr-message", None)
    if not pr_message:
        pr_message = CIVIC_JSON_PR_MESSAGE_TEMPLATE.format(user_login=user['login'])
    data = {
        "title": CIVIC_JSON_PR_TITLE,
        "body": pr_message,
        "head": pull_head,
        "base": pull_base
    }

    try:
        response = github.post("repos/{}/pulls".format(project["repo"]), data=data)
    except GitHubError as e:
        error_message = e.response.json()['message']
        logging.error(u"GitHub error {} ({}) when sending a pull request to repos/{}/pulls.".format(e.response.status_code, error_message, project["repo"]))
        return render_template("civic_json.html", error=error_message, project=None, user=None)

    return redirect(response["html_url"])


@app.route("/brigade/attendance")
@app.route("/brigade/<brigadeid>/attendance")
def attendance(brigadeid=None):
    ''' Show the Brigade attendance '''

    if brigadeid:
        if not is_existing_organization(brigadeid):
            return render_template('404.html'), 404

    if not brigadeid:
        got = get("https://www.codeforamerica.org/api/attendance")
    else:
        got = get("https://www.codeforamerica.org/api/organizations/%s/attendance" % brigadeid)

    attendance = got.json()

    if attendance["weekly"]:

        # GCharts wants a list of lists
        attendance["weeks"] = []
        for key, value in attendance["weekly"].iteritems():
            week = [str(key), value]
            attendance["weeks"].append(week)
        attendance["weeks"] = sorted(attendance["weeks"], key=itemgetter(0))

        attendance["this_week"] = 0
        attendance["last_week"] = 0
        if len(attendance["weeks"]) >= 1:
            attendance["this_week"] = attendance["weeks"][-1][1]
            if len(attendance["weeks"]) >= 2:
                attendance["last_week"] = attendance["weeks"][-2][1]

    return render_template("attendance.html", brigadeid=brigadeid, attendance=attendance)


@app.route("/brigade/rsvps")
@app.route("/brigade/<brigadeid>/rsvps")
def rsvps(brigadeid=None):
    ''' Show the Brigade rsvps '''

    if brigadeid:
        if not is_existing_organization(brigadeid):
            return render_template('404.html'), 404

    if not brigadeid:
        got = get("https://www.codeforamerica.org/api/events/rsvps")
    else:
        got = get("https://www.codeforamerica.org/api/organizations/%s/events/rsvps" % brigadeid)

    rsvps = got.json()

    if rsvps["weekly"]:

        # GCharts wants a list of lists
        rsvps["weeks"] = []
        for key, value in rsvps["weekly"].iteritems():
            week = [str(key), value]
            rsvps["weeks"].append(week)
        rsvps["weeks"] = sorted(rsvps["weeks"], key=itemgetter(0))

        rsvps["this_week"] = 0
        rsvps["last_week"] = 0
        if len(rsvps["weeks"]) >= 1:
            rsvps["this_week"] = rsvps["weeks"][-1][1]
            if len(rsvps["weeks"]) >= 2:
                rsvps["last_week"] = rsvps["weeks"][-2][1]

    return render_template("rsvps.html", brigadeid=brigadeid, rsvps=rsvps)


@app.route('/brigade/index/<brigadeid>/')
def redirect_brigade(brigadeid):
    ''' Redirect old Brigade links to new Brigade links'''
    return redirect("/brigade/" + brigadeid, code=301)

@app.route('/brigade/<brigadeid>/')
def brigade(brigadeid):
    ''' Get this Brigade's info '''

    if brigadeid:
        if not is_existing_organization(brigadeid):
            return render_template('404.html'), 404

    got = get("https://www.codeforamerica.org/api/organizations/" + brigadeid)
    brigade = got.json()

    return render_template("brigade.html", brigade=brigade, brigadeid=brigadeid)


@app.route("/brigade/checkin/", methods=["GET"])
@app.route("/brigade/<brigadeid>/checkin/", methods=["GET"])
def get_checkin(brigadeid=None):
    ''' Checkin to a Brigade event '''

    if brigadeid:
        if not is_existing_organization(brigadeid):
            return render_template('404.html'), 404

    brigades = None
    if not brigadeid:
        # Get all of the organizations from the api
        organizations = get('https://www.codeforamerica.org/api/organizations.geojson')
        organizations = organizations.json()
        brigades = []
        # Org's names and ids
        for org in organizations['features']:
            if "Brigade" in org['properties']['type']:
                brigades.append({
                    "name": org['properties']['name'],
                    "id": org['id']
                })

        # Alphabetize names
        brigades.sort(key=lambda x: x.values()[0])

    # If we want to remember the event, question
    event = request.args.get("event", None)
    question = request.args.get("question", None)

    return render_template("checkin.html", brigadeid=brigadeid, event=event, brigades=brigades, question=question)


@app.route("/brigade/checkin/", methods=["POST"])
@app.route("/brigade/<brigadeid>/checkin/", methods=["POST"])
def post_checkin(brigadeid=None):
    ''' Prep the checkin for posting to the peopledb '''
    # VALIDATE
    cfapi_url = request.form.get('cfapi_url')
    if not cfapi_url:
        return make_response("Missing required cfapi_url", 422)

    elif not re.match("https:\/\/www\.codeforamerica\.org\/api\/organizations\/[A-Za-z-]*", cfapi_url):
        return make_response("cfapi_url needs to like https://www.codeforamerica.org/api/organizations/Brigade-ID", 422)

    brigadeid = request.form.get('cfapi_url').split("/")[-1]
    if not is_existing_organization(brigadeid):
        return make_response(brigadeid + "is not an existing brigade.", 422)

    # MAILCHIMP SIGNUP
    if request.form.get("mailinglist", None):
        if request.form.get("email", None):

            # Split first and last name
            name = request.form.get('name', None)
            if name:
                if ' ' in request.form['name']:
                    first_name, last_name = name.split(' ', 1)
                else:
                    first_name, last_name = name, ''
            else:
                first_name, last_name = None, None

            mailchimp_data = {
                'FNAME': first_name,
                'LNAME': last_name,
                'EMAIL': request.form.get("email"),
                'REFERRAL': request.url,
                'group[10273][8192]': '8192', # I attend Brigade events
                'group[10245][32]': '32' # Brigade newsletter
            }

            cfa_mailchimp_url = "http://codeforamerica.us2.list-manage.com/subscribe/post-json?u=d9acf2a4c694efbd76a48936f&amp;id=3ac3aef1a5"
            cfa_mailchimp_response = post(cfa_mailchimp_url, data=mailchimp_data)

            if cfa_mailchimp_response.status_code != 200:
                return cfa_mailchimp_response.content

    # Prep PeopleDB post
    # Q&A is stored as a json string
    extras = {}
    extras["question"] = request.form.get("question", None)
    extras["answer"] = request.form.get("answer", None)
    extras = json.dumps(extras)

    peopledb_post = {
        "name": request.form.get('name', None),
        "email": request.form.get("email", None),
        "event": request.form.get("event", None),
        "date": request.form.get("date", datetime.now()),
        "org_cfapi_url": request.form.get('cfapi_url'),
        "extras": extras
    }

    auth = current_app.config["BRIGADE_SIGNUP_SECRET"] + ':x-brigade-signup'
    headers = {'Authorization': 'Basic ' + base64.b64encode(auth)}
    peopleapp = "https://people.codeforamerica.org/checkin"

    r = post(peopleapp, data=peopledb_post, headers=headers)

    if r.status_code == 200:
        # Remembering event name and brigadeid for later
        event = request.form.get("event", None)
        question = request.form.get("question", None)
        brigadeid = request.form.get("cfapi_url").replace("https://www.codeforamerica.org/api/organizations/", "")
        flash("Thanks for volunteering")

        if brigadeid:
            url = "brigade/" + brigadeid + "/checkin/"
        else:
            url = "brigade/checkin/"

        if event or question:
            url += "?"
            if event:
                event = event.replace(" ", "+")
                url += "event=" + event
            if event and question:
                url += "&"
            if question:
                question = question.replace(" ", "+")
                url += "question=" + question

        return redirect(url)

    # Pass any errors through
    else:
        return make_response(r.content, r.status_code)


@app.route("/brigade/test-checkin/", methods=["POST"])
@app.route("/brigade/<brigadeid>/test-checkin/", methods=["POST"])
def post_test_checkin(brigadeid=None):
    ''' Prep the checkin for posting to the peopledb '''

    test_checkin_data = {
        "name": request.form.get('name', None),
        "email": request.form.get("email", None),
        "event": request.form.get("event", None),
        "date": request.form.get("date", str(datetime.now())),
        "cfapi_url": request.form.get('cfapi_url'),
        "question": request.form.get("question", None),
        "answer": request.form.get("answer", None)
    }

    if not test_checkin_data["cfapi_url"]:
        return make_response("Missing required cfapi_url", 422)

    elif not re.match("https:\/\/www\.codeforamerica\.org\/api\/organizations\/[A-Za-z-]*", test_checkin_data["cfapi_url"]):
        return make_response("cfapi_url needs to like https://www.codeforamerica.org/api/organizations/Brigade-ID", 422)

    brigadeid = test_checkin_data["cfapi_url"].split("/")[-1]
    if not is_existing_organization(brigadeid):
        return make_response(brigadeid + "is not an existing brigade.", 422)

    else:
        return make_response(json.dumps(test_checkin_data), 200)


@app.route('/brigade/projects/monitor')
@app.route('/brigade/<brigadeid>/projects/monitor')
def project_monitor(brigadeid=None):
    ''' Check for Brigade projects on Travis'''
    limit = int(request.args.get('limit', 50))
    travis_projects = []
    projects = []
    if not brigadeid:
        projects = get_projects(projects, "https://www.codeforamerica.org/api/projects", limit)
    else:
        projects = get_projects(projects, "https://www.codeforamerica.org/api/organizations/" + brigadeid + "/projects", limit)

    # Loop through projects and get
    for project in projects:
        if project["code_url"]:
            url = urlparse(project["code_url"])
            if url.netloc == "github.com":
                travis_url = "https://api.travis-ci.org/repositories" + url.path + "/builds"
                project["travis_url"] = travis_url
                travis_projects.append(project)

    return render_template('projectmonitor.html', projects=travis_projects, org_name=brigadeid)
