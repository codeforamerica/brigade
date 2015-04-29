import json
import os
from requests import get, post
import datetime

from flask import Flask, render_template, request, redirect
import filters

app = Flask(__name__, static_url_path="/brigade/static")
app.register_blueprint(filters.blueprint)


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


# ROUTES
@app.route('/brigade/')
def index():
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
        'brigade_id' : request.form.get("brigade_id", None),
        'SECRET_KEY' : os.environ.get("SECRET_KEY", "boop")
        }

    peopledb_response = post("https://people.codeforamerica.org/brigade/signup", data=peopledb_data)

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

    # Get the projects updated within the last month
    # got = get("https://www.codeforamerica.org/api/projects?only_ids=True&per_page=100")
    # got = got.json()
    # projects = got['objects']
    # projects_total = got['total']
    # active_projects = []
    # for project in projects:
    #     # Sat, 14 Mar 2015 00:01:04 GMT
    #     tformat = "%a, %d %b %Y %H:%M:%S %Z"
    #     last_updated = datetime.datetime.strptime(project['last_updated'], tformat)
    #     delta = datetime.datetime.now() - last_updated
    #     if delta.days < 7:
    #         print delta.days
    #         active_projects.append(project)
    #     else:
    #         break
    # Do some paging here to get more projects

    # active_projects_total = len(active_projects)

    return render_template("numbers.html", brigades_total=brigades_total, official_brigades_total=official_brigades_total, projects_total=projects_total)


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
        url = "https://www.codeforamerica.org/api/projects?organization_type=Brigade"
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


if __name__ == '__main__':
    app.run(debug=True)
