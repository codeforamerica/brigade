import json
import os
from requests import get, post

from datetime import datetime
from base64 import b64encode

from flask import Flask, render_template, request, redirect, url_for, make_response
import filters

app = Flask(__name__, static_url_path="/brigade/static")
app.register_blueprint(filters.blueprint)

app.config['BRIGADE_SIGNUP_SECRET'] = os.environ['BRIGADE_SIGNUP_SECRET']

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

# ROUTES
@app.route('/brigade/list', methods=["GET"])
def brigade_list():
    brigades = get_brigades()
    brigades = json.loads(brigades)
    brigades.sort(key=lambda x: x['properties']['city'])
    return render_template("brigade_list.html", brigades=brigades )


@app.route('/brigade/')
def index():
    brigades = get_brigades()
    return render_template("index.html", brigades=brigades )


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
        'first_name' : request.form.get("FNAME"),
        'last_name' : request.form.get("LNAME"),
        'email' : request.form.get("EMAIL"),
        'brigade_id' : request.form.get("brigade_id", None)
        }
    
    auth = app.config['BRIGADE_SIGNUP_SECRET'], 'x-brigade-signup'
    url = 'https://people.codeforamerica.org/brigade/signup'

    peopledb_response = post(url, data=peopledb_data, auth=auth)
    
    # Choose a response to show
    # if brigade_mailchimp_response:
    #     return brigade_mailchimp_response

    # elif cfa_mailchimp_response:
    #     return cfa_mailchimp_response.content

    if peopledb_response:
        response = {
            "status_code" : peopledb_response.status_code,
            "msg" : peopledb_response.content
        }
        return json.dumps(response)

    else:
        response = {
            "status_code" : 500,
            "msg" : "Something went wrong. You were not added to any lists."
        }
        return json.dumps(response)


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

    # Get total number of projects
    got = get("https://www.codeforamerica.org/api/projects?per_page=1")
    got = got.json()
    projects = got['objects']
    projects_total = got['total']

    # Get total number of Brigade projects
    got = get("https://www.codeforamerica.org/api/projects?organization_type=Brigade&per_page=1")
    got = got.json()
    projects = got['objects']
    brigade_projects_total = got['total']

    # Get total number of Code for All projects
    got = get("https://www.codeforamerica.org/api/projects?organization_type=Code for All&per_page=1")
    got = got.json()
    projects = got['objects']
    cfall_projects_total = got['total']

    # Get total number of Government projects
    got = get("https://www.codeforamerica.org/api/projects?organization_type=Government&per_page=1")
    got = got.json()
    projects = got['objects']
    gov_projects_total = got['total']

    # Get number of Health projects
    got = get("https://www.codeforamerica.org/api/projects?q=health&per_page=1")
    got = got.json()
    projects = got['objects']
    health_total = got['total']

    # Get number of Money projects
    got = get("https://www.codeforamerica.org/api/projects?q=money&per_page=1")
    got = got.json()
    projects = got['objects']
    money_total = got['total']

    # Get number of Justice projects
    got = get("https://www.codeforamerica.org/api/projects?q=justice&per_page=1")
    got = got.json()
    projects = got['objects']
    justice_total = got['total']

    # Get number of Issues
    got = get("https://www.codeforamerica.org/api/issues?per_page=1")
    got = got.json()
    issues = got['objects']
    issues_total = got['total']

    # Get number of Help Wanted Issues
    got = get("https://www.codeforamerica.org/api/issues/labels/help%20wanted?per_page=1")
    got = got.json()
    issues = got['objects']
    help_wanted_total = got['total']

    # Get number of Bug Issues
    got = get("https://www.codeforamerica.org/api/issues/labels/bug?per_page=1")
    got = got.json()
    issues = got['objects']
    bug_total = got['total']

    # Get number of Enhancement Issues
    got = get("https://www.codeforamerica.org/api/issues/labels/enhancement?per_page=1")
    got = got.json()
    issues = got['objects']
    enhancement_total = got['total']

    kwargs = dict(brigades_total=brigades_total, official_brigades_total=official_brigades_total, cfall_total=cfall_total, government_total=government_total, projects_total=projects_total, brigade_projects_total=brigade_projects_total, cfall_projects_total=cfall_projects_total, gov_projects_total=gov_projects_total, health_total=health_total, money_total=money_total, justice_total=justice_total, issues_total=issues_total, help_wanted_total=help_wanted_total, bug_total=bug_total, enhancement_total=enhancement_total)

    return render_template("numbers.html", **kwargs )


@app.route("/brigade/about/")
def about():
    return render_template("about.html")


@app.route("/brigade/organize/")
def organize():

    got = get("http://www.codeforamerica.org/api/organizations.geojson")
    geojson = got.json()
    brigades = []

    # Prepare the geojson for a map
    for org in geojson["features"]:
        # Grab only orgs with type Brigade
        if "Brigade" in org["properties"]["type"]:
            brigades.append(org)
        elif "Code for All" in org["properties"]["type"]:
            brigades.append(org)

    brigades = json.dumps(brigades)

    # Get universal sign up form
    r = get("http://www.codeforamerica.org/fragments/email-signup.html")
    signup = r.content

    return render_template("organize.html", brigades=brigades, signup=signup)



@app.route("/brigade/tools/")
@app.route("/brigade/tools/<page>/")
def tools(page=None):
    if page:
        return render_template("tools/"+page+".html")
    else:
        return render_template("tools/index.html")


@app.route("/brigade/infrastructure")
def infrastructure():
    return render_template("infrastructure.html")


@app.route("/brigade/projects/")
@app.route("/brigade/<brigadeid>/projects/")
def projects(brigadeid=None):
    ''' Display a list of projects '''
    projects = []
    brigade = None
    search = request.args.get("q", None)
    sort_by = request.args.get("sort_by", None)
    page = request.args.get("page", None)

    if page:
        if brigadeid:
            next = "/brigade/"+brigadeid+"/projects/?page=" + str(int(page) + 1)
        else:
            next = "/brigade/projects/?page=" + str(int(page) + 1)
    else:
        if brigadeid:
            next = "/brigade/"+brigadeid+"/projects/?page=2"
        else:
            next = "/brigade/projects/?page=2"

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

    if brigadeid:
        url = "https://www.codeforamerica.org/api/organizations/"+ brigadeid +"/projects"
        if search or sort_by or page:
            url += "?"
        if search:
            url += "&q=" + search
        if sort_by:
            url += "&sort_by" + sort_by
        if page:
            url += "&page=" + page
        got = get(url)
        projects = get_projects(projects, url)
        brigade = projects[0]["organization"]

    else:
        url = "https://www.codeforamerica.org/api/projects"
        if search or sort_by or page:
            url += "?"
        if search:
            url += "&q=" + search
        if sort_by:
            url += "&sort_by" + sort_by
        if page:
            url += "&page=" + page
        got = get(url)
        projects = get_projects(projects, url)

    return render_template("projects.html", projects=projects, brigade=brigade, next=next)


@app.route('/brigade/index/<brigadeid>/')
def redirect_brigade(brigadeid):
    ''' Redirect old Brigade links to new Brigade links'''
    return redirect("/brigade/"+brigadeid, code=301)

@app.route('/brigade/<brigadeid>/')
def brigade(brigadeid):
    # Get this Brigade's info
    got = get("https://www.codeforamerica.org/api/organizations/" + brigadeid)
    brigade = got.json()

    if 'status' in brigade:
        if brigade['status'] == 'Resource Not Found':
            return render_template('404.html'), 404

    return render_template("brigade.html", brigade=brigade, brigadeid=brigadeid)


@app.route("/brigade/checkin/", methods=["GET", "POST"])
@app.route("/brigade/<brigadeid>/checkin/", methods=["GET", "POST"])
def checkin(brigadeid=None, event=None, brigades=None):
    ''' A tool to track attendance at Brigade events '''

    if request.method == "GET":
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

        # If we want to remember the event
        url = request.url
        if "?" in url:
            string = url.split("?")[1].split("=")
            event = string[1].replace("+"," ")

        return render_template("checkin.html", brigadeid=brigadeid,
            brigades=brigades, event=event)


    if request.method == "POST":
        ''' Prep the checkin for posting to the peopledb '''
        ''' Sample response:
            ImmutableMultiDict([('email', u'test@test.com'),
                                ('cfapi_url', u'https://www.codeforamerica.org/api/organizations/Code-for-San-Francisco'),
                                ('event', u'Hack Night'), ('name', u'FIRST LAST')])'''

        peopledb_post = {
            "name": request.form.get('name', None),
            "email": request.form.get("email", None),
            "event": request.form.get("event", None),
            "date": datetime.now(),
            "org_cfapi_url": request.form.get('cfapi_url'),
            "extras" : None
        }

        auth = app.config["BRIGADE_SIGNUP_SECRET"] + ':x-brigade-signup'
        headers = {'Authorization': 'Basic ' + b64encode(auth)}
        peopleapp = "https://people.codeforamerica.org/checkin"

        r = post(peopleapp, data=peopledb_post, headers=headers)

        if r.status_code == 200:
            # Remembering event name and brigadeid for later
            event = request.form.get("event", None)
            brigadeid = request.form["cfapi_url"].replace("https://www.codeforamerica.org/api/organizations/","")
            return redirect(url_for('checkin', event=event, brigadeid=brigadeid))

        elif r.status_code == 422:
            return make_response(r.content, 422)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
