from requests import get
import json

BASE_URL = "http://api.codeforamerica.org/api"


def get_brigades(cfa_brigades_only=False):
    # Get location of all civic tech orgs
    got = get(BASE_URL + "/organizations.geojson")
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
            
            # If cfa_brigades_only=True, only return CfA Brigades
            if cfa_brigades_only == True:
                if ("tags" in org["properties"] and 
                    "Brigade" in org["properties"]["tags"] and 
                    "Code for America" in org["properties"]["tags"]):
                        brigades.append(org)
            else:
                brigades.append(org)

    brigades = json.dumps(brigades)
    return brigades


# TODO: make a get_organization_projects wrapper so the URL doesn't need to be
# passed in here.
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


def is_existing_organization(orgid):
    ''' tests that an organization exists on the cfapi'''
    got = get(BASE_URL + "/organizations.geojson").json()
    orgids = [org["properties"]["id"] for org in got["features"]]
    return orgid in orgids
