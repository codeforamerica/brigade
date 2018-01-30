# -- coding: utf-8 --
from flask import render_template, request, redirect, url_for, send_from_directory
from flask.helpers import safe_join
from . import brigade as app
import cfapi
from operator import itemgetter
from requests import get

import logging


# Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
requests_logger = logging.getLogger("requests")
requests_logger.setLevel(logging.WARNING)


#
# ROUTES
#
@app.route('/brigade/list', methods=["GET"])
def brigade_list():
    return redirect(url_for('.index'), code=301)


@app.route('/brigade/')
def index():
    brigades = cfapi.get_brigades(official_brigades_only=True)
    return render_template("index.html", brigades=brigades)


@app.route('/brigade/map')
def brigade_map():
    return redirect(url_for('.map'), code=301)


@app.route('/map')
def map():
    brigades = cfapi.get_brigades(official_brigades_only=True)
    return render_template("map.html", brigades=brigades)


@app.route("/brigade/numbers")
def brigade_numbers():
    return redirect(url_for('.numbers'), code=301)


@app.route("/numbers")
def numbers():
    # Get the total number of Brigades
    got = get(cfapi.BASE_URL + "/organizations?type=Brigade&per_page=1")
    got = got.json()
    brigades_total = got['total']

    # Get the official Brigades
    got = get(cfapi.BASE_URL + "/organizations?type=Official&per_page=1")
    got = got.json()
    official_brigades_total = got['total']

    # Get the total number of Code for All Groups
    got = get(cfapi.BASE_URL + "/organizations?type=Code for All&per_page=1")
    got = got.json()
    cfall_total = got['total']

    # Get number of meetup-members
    got = get(cfapi.BASE_URL + "/organizations/member_count")
    got = got.json()
    member_count = got['total']

    # Get number of RSVPs
    got = get(cfapi.BASE_URL + "/events/rsvps")
    got = got.json()
    rsvps = got['total']

    # Get total number of projects
    got = get(cfapi.BASE_URL + "/projects?only_ids&per_page=1")
    got = got.json()
    projects_total = got['total']

    # Get total number of Brigade projects
    got = get(cfapi.BASE_URL + "/projects?only_ids&organization_type=Brigade&per_page=1")
    got = got.json()
    brigade_projects_total = got['total']

    # Get total number of Code for All projects
    got = get(cfapi.BASE_URL + "/projects?only_ids&organization_type=Code for All&per_page=1")
    got = got.json()
    cfall_projects_total = got['total']

    # Get total number of Government projects
    got = get(cfapi.BASE_URL + "/projects?only_ids&organization_type=Government&per_page=1")
    got = got.json()
    gov_projects_total = got['total']

    # Get number of Issues
    got = get(cfapi.BASE_URL + "/issues?per_page=1")
    got = got.json()
    issues_total = got['total']

    # Get number of Help Wanted Issues
    got = get(cfapi.BASE_URL + "/issues/labels/help%20wanted?per_page=1")
    got = got.json()
    help_wanted_total = got['total']

    kwargs = dict(brigades_total=brigades_total, official_brigades_total=official_brigades_total,
                  cfall_total=cfall_total, member_count=member_count, rsvps=rsvps,
                  projects_total=projects_total, brigade_projects_total=brigade_projects_total,
                  cfall_projects_total=cfall_projects_total, gov_projects_total=gov_projects_total,
                  issues_total=issues_total, help_wanted_total=help_wanted_total,)

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
def tools():
    return redirect(url_for('.free_software_index'), code=302)


@app.route("/software/")
def free_software_index():
    return render_template("free_software.html")


@app.route("/software/<software>")
def free_software_show(software):
    template_path = safe_join("free_software/", software + ".html")
    return render_template(template_path)


@app.route("/styleguide/")
def styleguide():
    return render_template("styleguide.html")


@app.route("/brigade/projects")
@app.route("/brigade/<brigadeid>/projects")
def projects(brigadeid=None):
    ''' Display a list of projects '''

    # is this an exisiting group
    if brigadeid:
        if not cfapi.is_existing_organization(brigadeid):
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
        url = cfapi.BASE_URL + "/organizations/" + brigadeid + "/projects"
        # set the brigade name
        if projects:
            brigade = projects[0]["organization"]
        else:
            brigade = {"name": brigadeid.replace("-", " ")}
    else:
        # build cfapi url
        url = cfapi.BASE_URL + "/projects"
        url += "?sort_by=last_updated"
    if search:
        url += "&q=" + search
    if page:
        url += "&page=" + page
    if status:
        url += "&status=" + status
    if organization_type:
        url += "&organization_type=" + organization_type

    projects = cfapi.get_projects(projects, url)

    return render_template("projects.html", projects=projects, brigade=brigade, next=next)


@app.route("/brigade/rsvps")
@app.route("/brigade/<brigadeid>/rsvps")
def rsvps(brigadeid=None):
    ''' Show the Brigade rsvps '''

    if brigadeid:
        if not cfapi.is_existing_organization(brigadeid):
            return render_template('404.html'), 404

    if not brigadeid:
        got = get(cfapi.BASE_URL + "/events/rsvps")
    else:
        got = get(cfapi.BASE_URL + "/organizations/%s/events/rsvps" % brigadeid)

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
        if not cfapi.is_existing_organization(brigadeid):
            return render_template('404.html'), 404

    got = get(cfapi.BASE_URL + "/organizations/" + brigadeid)
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
        projects = cfapi.get_projects(projects, cfapi.BASE_URL + "/projects", limit)
    else:
        projects = cfapi.get_projects(
            projects,
            cfapi.BASE_URL + "/organizations/" + brigadeid + "/projects", limit
        )

    for project in projects:
        if project["commit_status"] in ["success", "failure"]:
            projects_with_tests.append(project)

    return render_template('monitor.html', projects=projects_with_tests, org_name=brigadeid)


@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


@app.route('/', methods=['GET'])
def redirect_to_index():
    return redirect(url_for('.index'))
