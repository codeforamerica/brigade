import json
import re
from requests import get

BASE_URL = "http://api.codeforamerica.org/api"
STATE_NAMES = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AS': 'American Samoa',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'GU': 'Guam',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MP': 'Northern Mariana Islands',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NA': 'National',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'PR': 'Puerto Rico',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VI': 'Virgin Islands',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'
}


def get_brigades(official_brigades_only=False):
    # Get location of all civic tech orgs
    got = get(BASE_URL + "/organizations.geojson")
    geojson = got.json()
    brigades = []

    # Prepare the geojson for a map
    for org in geojson["features"]:
        # Add icon info for the map
        org["properties"]["marker-symbol"] = "town-hall"
        # All Brigades on the map have a red marker
        org["properties"]["marker-color"] = "#aa1c3a"
        # Grab only orgs with type Brigade
        if (org["properties"]["tags"] and "Brigade" in org["properties"]["tags"]):

            # If cfa_brigades_only=True, only return Official Brigades
            if official_brigades_only:
                if "Official" in org["properties"]["tags"]:
                    brigades.append(org)
            else:
                brigades.append(org)

    return brigades


def get_official_brigades_by_state():
    brigades = get_brigades(official_brigades_only=True)
    states = {}
    for brigade in brigades:
        # Find all two-letter state abbreviations in the brigade's city (e.g.
        # "Kansas City, MO & KS"), and add the brigade to those states
        brigade_states = re.findall(
            r'\b([A-Z]{2})\b', brigade['properties']['city'])
        for state in brigade_states:
            state_fullname = STATE_NAMES[state]
            if state_fullname not in states:
                states[state_fullname] = []
            states[state_fullname].append(brigade['properties'])

        # Handle statewide collaborations like "North Carolina" or "California"
        if brigade['properties']['city'] in STATE_NAMES.values():
            state_fullname = brigade['properties']['city']
            if state_fullname not in states:
                states[state_fullname] = []
            states[state_fullname].append(brigade['properties'])

    for brigades in states.values():
        brigades.sort(key=lambda b: b['name'])
    return states


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
