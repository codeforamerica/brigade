import json
from requests import get
from flask import Flask, render_template
app = Flask(__name__)

from datetime import datetime

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
    dt = dt[:19]
    dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
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
    return render_template("index.html", brigades=brigades)


@app.route('/<brigadeid>/')
def brigade(brigadeid):
    # Get this Brigade's info
    got = get("https://www.codeforamerica.org/api/organizations/" + brigadeid)
    brigade = got.json()

    return render_template("brigade.html", brigade=brigade)


if __name__ == '__main__':
    app.run(debug=True)