# -- coding: utf-8 --
from flask import current_app, render_template, request, redirect, make_response, flash, session
from . import brigade as app
from datetime import datetime
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

CFAPI = "https://codeforamerica-api.herokuapp.com/api"

def get_brigades():
    # Get location of all civic tech orgs
    got = get(CFAPI + "/organizations.geojson")
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
            print org
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


@app.route("/brigade/numbers/")
def numbers():
    # Get the total number of Brigades
    got = get(CFAPI + "/organizations?type=Brigade&per_page=1")
    got = got.json()
    brigades_total = got['total']

    # Get the official Brigades
    got = get(CFAPI + "/organizations?type=Official&per_page=1")
    got = got.json()
    official_brigades_total = got['total']

    # Get the total number of Code for All Groups
    got = get(CFAPI + "/organizations?type=Code for All&per_page=1")
    got = got.json()
    cfall_total = got['total']

    # Get number of meetup-members
    got = get("http://codeforamerica.org/api/organizations/member_count")
    got = got.json()
    member_count = got['total']

    # Get number of RSVPs
    got = get(CFAPI + "/events/rsvps")
    got = got.json()
    rsvps = got['total']

    # Get total number of projects
    got = get(CFAPI + "/projects?only_ids&per_page=1")
    got = got.json()
    projects_total = got['total']

    # Get total number of Brigade projects
    got = get(CFAPI + "/projects?only_ids&organization_type=Brigade&per_page=1")
    got = got.json()
    brigade_projects_total = got['total']

    # Get total number of Code for All projects
    got = get(CFAPI + "/projects?only_ids&organization_type=Code for All&per_page=1")
    got = got.json()
    cfall_projects_total = got['total']

    # Get total number of Government projects
    got = get(CFAPI + "/projects?only_ids&organization_type=Government&per_page=1")
    got = got.json()
    gov_projects_total = got['total']

    # Get number of Issues
    got = get(CFAPI + "/issues?per_page=1")
    got = got.json()
    issues_total = got['total']

    # Get number of Help Wanted Issues
    got = get(CFAPI + "/issues/labels/help%20wanted?per_page=1")
    got = got.json()
    help_wanted_total = got['total']

    # Get number of civic issue finder clicks
    got = get("https://www.codeforamerica.org/geeks/civicissues/analytics/total_clicks")
    got = got.json()
    total_issue_clicks = got['total_clicks']

    kwargs = dict(brigades_total=brigades_total, official_brigades_total=official_brigades_total,
                  cfall_total=cfall_total, member_count=member_count, rsvps=rsvps,
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
    page = request.args.get("page", None)
    status = request.args.get("status", None)
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
        url = CFAPI + "/organizations/" + brigadeid + "/projects"
        # set the brigade name
        if projects:
            brigade = projects[0]["organization"]
        else:
            brigade = {"name": brigadeid.replace("-", " ")}
    else:
        # build cfapi url
        url = CFAPI + "/projects"
        url += "?sort_by=last_updated"
    if search:
        url += "&q=" + search
    if page:
        url += "&page=" + page
    if status:
        url += "&status=" + status
    if organization_type:
        url += "&organization_type=" + organization_type

    projects = get_projects(projects, url)

    return render_template("projects.html", projects=projects, brigade=brigade, next=next)


@app.route("/brigade/rsvps")
@app.route("/brigade/<brigadeid>/rsvps")
def rsvps(brigadeid=None):
    ''' Show the Brigade rsvps '''

    if brigadeid:
        if not is_existing_organization(brigadeid):
            return render_template('404.html'), 404

    if not brigadeid:
        got = get(CFAPI + "/events/rsvps")
    else:
        got = get(CFAPI + "/organizations/%s/events/rsvps" % brigadeid)

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

    got = get(CFAPI + "/organizations/" + brigadeid)
    brigade = got.json()

    return render_template("brigade.html", brigade=brigade, brigadeid=brigadeid)


@app.route('/brigade/projects/monitor')
@app.route('/brigade/<brigadeid>/projects/monitor')
def project_monitor(brigadeid=None):
    ''' Are the Brigade projects test passing or not '''
    projects = []
    projects_with_tests = []
    limit = int(request.args.get('limit', 50))
    if not brigadeid:
        projects = get_projects(projects, CFAPI + "/projects", limit)
    else:
        projects = get_projects(projects, CFAPI + "/organizations/" + brigadeid + "/projects", limit)

    for project in projects:
        if project["commit_status"] in ["success", "failure"]:
            projects_with_tests.append(project)

    return render_template('monitor.html', projects=projects_with_tests, org_name=brigadeid)
