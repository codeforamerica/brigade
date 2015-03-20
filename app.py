import json
from requests import get, post
from flask import Flask, render_template, request
app = Flask(__name__)

from datetime import datetime

# http://flask.pocoo.org/snippets/33/
@app.template_filter("timesince")
def friendly_time(dt, past_="ago", 
    future_="from now", 
    default="just now"):
    """
    Returns string representing "time since"
    or "time until" e.g.
    3 days ago, 5 hours from now etc.
    """

    now = datetime.utcnow()
    try:
        trimmed_time = dt[:19]
        dt = datetime.strptime(trimmed_time, "%Y-%m-%d %H:%M:%S")
    except:
        pass
    try:
        # Thu, 26 Feb 2015 03:45:21 GMT
        dt = datetime.strptime(dt, "%a, %d %b %Y %H:%M:%S %Z")
    except:
        pass
    if now > dt:
        diff = now - dt
        dt_is_past = True
    else:
        diff = dt - now
        dt_is_past = False

    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:

        if period:
            return "%d %s %s" % (period, \
                singular if period == 1 else plural, \
                past_ if dt_is_past else future_)

    return default

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

    # POST to mailchimp
    if "mailchimp_url" in request.form:
        mailchimp_url = request.form.get("mailchimp_url")
        mailchimp_data = {
            'FNAME' : request.form.get("fname"),
            'LNAME' : request.form.get("lname"),
            'EMAIL' : request.form.get("email"),
            'group[10273][8192]' : '8192', # I attend Brigade events
            'REFERRAL' : '/brigade'
            }

        mailchimp_response = post(mailchimp_url, data=mailchimp_data)

    # POST to PeopleDB
    peopledb_data = {
        'FNAME' : request.form.get("fname"),
        'LNAME' : request.form.get("lname"),
        'EMAIL' : request.form.get("email"),
        'brigade_id' : request.form.get("brigade_id"),
        'SECRETKEY' : "woot"
        }

    peopledb_response = post("https://people.codeforamerica.org/brigade/sign-up", data=peopledb_data)

    return json.dumps(mailchimp_response.json())


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
    # Get email sign up form
    r = get("http://www.codeforamerica.org/fragments/email-signup.html")
    email_signup = r.content

    # Get this Brigade's info
    got = get("https://www.codeforamerica.org/api/organizations/" + brigadeid)
    brigade = got.json()



    return render_template("brigade.html", brigade=brigade, email_signup=email_signup, brigadeid=brigadeid)


if __name__ == '__main__':
    app.run(debug=True)