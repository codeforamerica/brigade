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

# Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
requests_logger = logging.getLogger("requests")
requests_logger.setLevel(logging.WARNING)

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


# Load load projects from the cfapi
def get_projects(projects, url, limit=10):
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
            project["repo"] = url.path

    return project

def get_github_user():
    ''' Get GitHub user information from the GitHub API
    '''
    user = None
    if session.get("access_token"):
        user = github.get("user")

    return user


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
    # got = get("https://www.codeforamerica.org/api/projects?status=experiment")
    # experiment_count = got.json()["total"]
    # got = get("https://www.codeforamerica.org/api/projects?status=alpha")
    # alpha_count = got.json()["total"]
    # got = get("https://www.codeforamerica.org/api/projects?status=beta")
    # beta_count = got.json()["total"]
    # got = get("https://www.codeforamerica.org/api/projects?status=official")
    # official_count = got.json()["total"]
    return render_template("stages.html")
    # , experiment_count=experiment_count, alpha_count=alpha_count, beta_count=beta_count, official_count=official_count)


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

    return render_template("civic_json.html", project=project, user=user)

@app.route("/brigade/<brigadeid>/projects/<project_name>/add-civic-json", methods=["POST"])
def civic_json(brigadeid, project_name):
    ''' Send a pull request to a project to add a civic.json file '''

    # Get information about the relevant project from the cfapi
    project = get_project_for_civic_json(brigadeid, project_name)
    user = get_github_user()

    # Create a new civic.json
    status = request.form.get("status", None)
    tags = request.form.get("tags", None)
    if tags:
        tags = [tag.strip() for tag in tags.split(',')]

    civic_json = {}
    if status:
        civic_json["status"] = status
    if tags:
        civic_json["tags"] = tags

    civic_json = json.dumps(civic_json, indent=4)


    # Fork the repo. Succeeds even if fork already exists.
    print "Making a fork at: repos{}/forks".format(project["repo"])
    try:
        response = github.post("repos{}/forks".format(project["repo"]), data=None)
    except GitHubError as e:
        error = e.response.json()['message']
        return render_template("civic_json.html", error=error, project=None, user=None)

    project_name = response["name"]
    forked_repo = response["full_name"]
    owner_login = response["owner"]["login"]
    default_branch = response["default_branch"]

    # Check if a civic.json already exists
    try:
        response = github.get("repos/{}/contents/civic.json".format(forked_repo))
        sha = response["sha"]
    except GitHubError as e:
        sha = None

    # Commit the civic.json file to our new fork
    data = {
        "message": "add civic.json file",
        "content": base64.b64encode(civic_json)
    }
    if sha:
        data["sha"] = sha

    print "Adding a civic.json file at: repos/{}/contents/civic.json".format(forked_repo)
    try:
        response = github.request("PUT", "repos/{}/contents/civic.json".format(forked_repo), data=json.dumps(data))
    except GitHubError as e:
        error = e.response.json()['message']
        return render_template("civic_json.html", error=error, project=None, user=None)

    # Check if Pull Request already exists
    try:
        response = github.get("repos{}/pulls".format(project["repo"]))
    except GitHubError as e:
        error = e.response.json()['message']
        return render_template("civic_json.html", error=error, project=None, user=None)

    for pr in response:
        if pr["title"] == "Adds a civic.json file":
            return redirect("{}/pulls".format(project["code_url"]))

    # Send a pull request
    data = {
        "title": "Adds a civic.json file",
        "body": '''Merge this to add a civic.json file to your project. This little bit of metadata will make your project easier to search for at [https://www.codeforamerica.org/brigade/projects](https://www.codeforamerica.org/brigade/projects) and elsewhere. :mag: You can read more about the status attribute at [https://www.codeforamerica.org/brigade/projects/stages](https://www.codeforamerica.org/brigade/projects/stages). It takes about an hour to update. :watch: If you have questions about any of this just ping @ondrae. :raised_hands:''',
        "head": "{}:{}".format(owner_login, default_branch),
        "base": default_branch
    }
    print "Creating a pull request for the new civic.json file"
    try:
        response = github.post("repos{}/pulls".format(project["repo"]), data=data)
    except GitHubError as e:
        error = e.response.json()['message']
        return render_template("civic_json.html", error=error, project=None, user=None)

    return redirect("{}/pulls".format(response["html_url"]))


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