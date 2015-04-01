import json
import os
from requests import get, post

from flask import Flask, render_template, request
import filters

app = Flask(__name__)
app.register_blueprint(filters.blueprint)

# ROUTES
@app.route('/')
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

    # Get footer html
    r = get("http://www.codeforamerica.org/fragments/global-footer.html")
    footer = r.content

    return render_template("index.html", brigades=brigades, footer=footer )


@app.route("/signup/", methods=["POST"])
def signup():
    ''' Takes in signup requests from /brigade/signup/form
        Sends the data to a requested mailchimp list, our mailchimp list, and the peopledb
    '''
    # Prep mailchimp data
    mailchimp_data = {
        'FNAME' : request.form.get("first_name"),
        'LNAME' : request.form.get("last_name"),
        'EMAIL' : request.form.get("email")
        }

    # POST to Brigade's mailchimp
    mailchimp_url = request.form.get("mailchimp_url", None)
    brigade_mailchimp_response = None
    if mailchimp_url:
        brigade_mailchimp_response = post(mailchimp_url, data=mailchimp_data)

    # POST to Code for America's mailchimp
    mailchimp_data['group[10273][8192]'] = '8192' # I attend Brigade events

    if request.form.get("brigade_id", None):
        mailchimp_data['REFERRAL'] = '/brigade/' + request.form.get("brigade_id", None)
    else:
        mailchimp_data['REFERRAL'] = '/brigade'

    cfa_mailchimp_url = "https://codeforamerica.us2.list-manage.com/subscribe/post-json?u=d9acf2a4c694efbd76a48936f&amp;id=3ac3aef1a5"
    cfa_mailchimp_response = post(cfa_mailchimp_url, data=mailchimp_data)

    # POST to PeopleDB
    peopledb_data = {
        'first_name' : request.form.get("first_name"),
        'last_name' : request.form.get("last_name"),
        'email' : request.form.get("email"),
        'brigade_id' : request.form.get("brigade_id", None),
        'SECRET_KEY' : os.environ.get("SECRET_KEY", "boop")
        }

    peopledb_response = post("https://people.codeforamerica.org/brigade/signup", data=peopledb_data)

    # Choose a response to show
    if brigade_mailchimp_response:
        return brigade_mailchimp_response

    elif cfa_mailchimp_response:
        return cfa_mailchimp_response.content

    elif peopledb_response:
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


@app.route("/signup/", methods=["GET"])
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


@app.route("/about/")
def about():
    return render_template("about.html")


@app.route("/organize/")
def organize():
    return render_template("organize.html")


@app.route("/tools/")
def tools():
    return render_template("tools.html")


@app.route("/tools/template/")
def template():
    return render_template("template.html")


@app.route("/projects")
@app.route("/<brigadeid>/projects")
def projects(brigadeid=None):
    ''' Display a list of projects '''
    projects = []
    brigade = None
    next = None

    # def get_projects(projects, url):
    #     got = get(url)
    #     new_projects = got.json()["objects"]
    #     projects = projects + new_projects
    #     if "next" in got.json()["pages"]:
    #         projects = get_projects(projects, got.json()["pages"]["next"])
    #     return projects

    if brigadeid:
        url = "http://codeforamerica.org/api/organizations/"+ brigadeid +"/projects"
        got = get(url)
        # projects = get_projects(projects, url)
        projects = got.json()["objects"]
        if "next" in got.json()["pages"]:
            next = got.json()["pages"]["next"]
        brigade = projects[0]["organization"]

    else:
        url = "http://codeforamerica.org/api/projects?organization_type=Brigade"
        got = get(url)
        projects = got.json()["objects"]
        if "next" in got.json()["pages"]:
            next = got.json()["pages"]["next"]

    return render_template("projects.html", projects=projects, brigade=brigade, next=next)


@app.route('/<brigadeid>/')
def brigade(brigadeid):
    # Get this Brigade's info
    got = get("https://www.codeforamerica.org/api/organizations/" + brigadeid)
    brigade = got.json()

    return render_template("brigade.html", brigade=brigade, brigadeid=brigadeid)



if __name__ == '__main__':
    app.run(debug=True)
