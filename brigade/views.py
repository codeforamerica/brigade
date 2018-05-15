# -- coding: utf-8 --
import cfapi
import dateutil.parser
import json
import logging
import urllib
from . import brigade as app
from datetime import datetime
from flask import render_template, request, redirect, url_for
from flask.helpers import safe_join
from operator import itemgetter
from requests import get

# Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
requests_logger = logging.getLogger("requests")
requests_logger.setLevel(logging.WARNING)


def redirect_from(*urls):
    def decorator(f):
        def view_func(**kwargs):
            route_name = ".".join([app.name, f.func_name])
            return redirect(url_for(route_name, **kwargs), code=301)

        for url in urls:
            app.add_url_rule(url, 'redirect_' + f.func_name, view_func)

        return f
    return decorator


#
# ROUTES
#
@redirect_from('/brigade/map/')
@app.route('/map')
def map():
    brigades = cfapi.get_brigades(official_brigades_only=True)
    brigades = json.dumps(brigades)
    return render_template("map.html", brigades=brigades)


@redirect_from("/brigade/about/")
@app.route("/about")
def about():
    return render_template("about.html")


@redirect_from("/brigade/organize/", "/brigade/organize/<page>")
@app.route("/resources")
def resources():
    return render_template("resources.html")


@redirect_from("/brigade/tools/", "/software/")
@app.route("/resources/software")
def free_software_index():
    return render_template("free_software.html")


@redirect_from("/software/<software>/")
@app.route("/resources/software/<software>")
def free_software_show(software):
    template_path = safe_join("free_software/", software + ".html")
    return render_template(template_path)


VIDEO_RESOURCES = [
        { "id": "jvVZHmMmq9I", "title": "Food Security Workshop", "date": "April 10, 2018", "description": "Civic Data Alliance, Code for Philly, Hack for LA, and Code for America discuss food security projects from the network. The Food Security workshop was an opportunity to ask questions, share work and stories, and collaborate on ways to address food security challenges in Brigades and their communities.", "start": "134", "topics": ["workshops", "project ideas"] },
        { "id": "3wNntmydohc", "title": "How to Host a Demo Day Workshop", "date": "March 8, 2018", "description": "Watch Code for Boston, Open Oakland, and Code for San Francisco talk about successful practices to host a Demo Day! Learn some tips, strategic approaches, and successful tactics from Brigades, and how you may be able to implement new ideas for your Brigades' demo days!", "topics": ["workshops", "organizer tips"] },
        { "id": "8wzqe0OUwLc", "title": "Brigade Fundraising Workshop", "date": "February 22, 2018", "description": "Watch Code for Atlanta, Code for Raleigh, Code for San Francisco, Code for San Jose, and Code for America talk about successful practices in fundraising for your brigade! Learn some tips, strategic approaches, and successful tactics from Brigades, and how you may be able to implement various fundraising approaches!", "topics": ["workshops", "fundraising"] }
    ]
@app.route("/resources/videos")
@app.route("/resources/videos/<topic>")
def resources_videos(topic=None):
    return render_template("resources_videos.html", videos=VIDEO_RESOURCES)


@app.route("/events")
def events():
    return render_template("events.html")


@app.route("/styleguide/")
def styleguide():
    return render_template("styleguide.html")


def brigade_projects(brigadeid=None):
    return redirect(url_for('.projects', brigadeid=brigadeid), code=301)


@redirect_from("/brigade/projects/", "/brigade/<brigadeid>/projects")
@app.route("/projects")
@app.route("/brigades/<brigadeid>/projects")
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
    page = request.args.get("page", 1, int)
    status = request.args.get("status", None)
    organization_type = request.args.get("organization_type", None)

    # Set next
    next = url_for('.projects', brigadeid=brigadeid, page=page + 1)

    # build the url
    if brigadeid:
        url = cfapi.BASE_URL + "/organizations/" + brigadeid + "/projects"
    else:
        url = cfapi.BASE_URL + "/projects"

    query = {"sort_by": "last_updated"}
    if search:
        query.update({"q": search})
    if page:
        query.update({"page": page})
    if status:
        query.update({"status": status})
    if organization_type:
        query.update({"organization_type": organization_type})
    url += '?' + urllib.urlencode(query)

    projects = cfapi.get_projects(projects, url)

    # set the brigade name
    if brigadeid:
        if len(projects):
            brigade = projects[0]["organization"]
        else:
            brigade = {"name": brigadeid.replace("-", " ")}

    return render_template("projects.html", projects=projects, brigade=brigade, next=next)


@app.route("/brigade/rsvps/")
@app.route("/brigade/<brigadeid>/rsvps")
def brigade_rsvps(brigadeid=None):
    return redirect(url_for('.rsvps', brigadeid=brigadeid), code=301)


@app.route("/rsvps")
@app.route("/brigades/<brigadeid>/rsvps")
def rsvps(brigadeid=None):
    ''' Show the Brigade rsvps '''

    if brigadeid:
        if not cfapi.is_existing_organization(brigadeid):
            return render_template('404.html'), 404

    if not brigadeid:
        got = get(cfapi.BASE_URL + "/events/rsvps")
    else:
        got = get(cfapi.BASE_URL + "/organizations/%s/events/rsvps" %
                  brigadeid)

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
@app.route('/brigade/<brigadeid>/')
def redirect_brigade(brigadeid):
    ''' Redirect old Brigade links to new Brigade links'''
    return redirect(url_for('.brigade', brigadeid=brigadeid), code=301)


@app.route('/brigades/<brigadeid>/')
def brigade(brigadeid):
    ''' Get this Brigade's info '''

    if brigadeid:
        if not cfapi.is_existing_organization(brigadeid):
            return render_template('404.html'), 404

    got = get(cfapi.BASE_URL + "/organizations/" + brigadeid)
    brigade = got.json()

    ''' If Brigade has upcoming events, check if the next event is happening today '''
    if 'current_events' in brigade and len(brigade['current_events']) > 0:
        event_date = dateutil.parser.parse(
            brigade['current_events'][0]['start_time']).strftime('%Y-%m-%d')
        todays_date = datetime.now().strftime('%Y-%m-%d')
        if event_date == todays_date:
            brigade['current_events'][0]['is_today'] = True

    return render_template("brigade.html", brigade=brigade, brigadeid=brigadeid)


@app.route('/brigade/projects/monitor')
@app.route('/brigade/<brigadeid>/projects/monitor')
def project_monitor_redirect(brigadeid=None):
    return redirect(url_for('.project_monitor', brigadeid=brigadeid), code=301)


@app.route('/projects/monitor')
@app.route('/brigades/<brigadeid>/projects/monitor')
def project_monitor(brigadeid=None):
    ''' Are the Brigade projects test passing or not '''
    projects = []
    projects_with_tests = []
    limit = int(request.args.get('limit', 50))
    if not brigadeid:
        projects = cfapi.get_projects(
            projects, cfapi.BASE_URL + "/projects", limit)
    else:
        projects = cfapi.get_projects(
            projects,
            cfapi.BASE_URL + "/organizations/" + brigadeid + "/projects", limit
        )

    for project in projects:
        if project["commit_status"] in ["success", "failure"]:
            projects_with_tests.append(project)

    return render_template('monitor.html', projects=projects_with_tests, org_name=brigadeid)


@redirect_from('/brigade/list', '/brigades')
@app.route('/brigades')
def brigade_list():
    brigades_by_state = cfapi.get_official_brigades_by_state()
    brigades = cfapi.get_brigades(official_brigades_only=True)
    brigades_total = len(brigades)
    return render_template(
        "brigade_list.html",
        brigades_total=brigades_total,
        brigades_by_state=brigades_by_state)


@redirect_from('/brigade/', '/brigade/numbers/')
@app.route('/', methods=['GET'])
def index():
    brigades = cfapi.get_brigades(official_brigades_only=True)
    brigades = json.dumps(brigades)
    return render_template("index.html", brigades=brigades)
