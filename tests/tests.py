# -- coding: utf-8 --
from urlparse import parse_qsl
from base64 import b64decode
import unittest
import json
import os
import flask
import httmock
from brigade import create_app
import brigade.views as view_functions
from bs4 import BeautifulSoup

class BrigadeTests(unittest.TestCase):

    def setUp(self):
        os.environ['BRIGADE_SIGNUP_SECRET'] = 'muy bueno'
        os.environ["GITHUB_CLIENT_ID"] = "WHAT"
        os.environ["GITHUB_CLIENT_SECRET"] = "EVER"

        self.app = create_app(os.environ)
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.client = self.app.test_client()
        # set up a fake github access token for civic.json tests
        with self.client as test_client:
            with test_client.session_transaction() as test_session:
                test_session['access_token'] = 'fake-github-access-token'

    def tearDown(self):
        self.app_context.pop()

    def civic_json_branch_content(self, url, request):
        ''' Mocking http responses when testing civic.json branches
        '''
        if url.geturl() == 'https://www.cfapi-staging.herokuapp.com/api/projects?name=add-civic-json-test&organization_id=Code-for-America' and request.method == 'GET':
            return self.civic_json_fork_content(url, request)

        if url.geturl() == 'https://api.github.com/user' and request.method == 'GET':
            return self.civic_json_fork_content(url, request)

        if url.geturl() == 'https://api.github.com/repos/codeforamerica/add-civic-json-test/pulls' and request.method == 'GET':
            return self.civic_json_fork_content(url, request)

        # get the target repo
        # (stripped out unused parameters)
        # https://developer.github.com/v3/repos/#get
        if url.geturl() == 'https://api.github.com/repos/codeforamerica/add-civic-json-test' and request.method == 'GET':
            return httmock.response(200, '''
                {
                  "name": "add-civic-json-test",
                  "full_name": "codeforamerica/add-civic-json-test",
                  "permissions": {
                    "push": true
                  },
                  "default_branch": "master"
                }''', {'Content-Type': 'application/json; charset=utf-8'})

        # get a branch
        # https://developer.github.com/v3/git/refs/#get-a-reference
        if url.geturl() == 'https://api.github.com/repos/codeforamerica/add-civic-json-test/git/refs/heads/add-civic-json-file' and request.method == 'GET':
            return httmock.response(200, '''
                {
                  "ref": "refs/heads/add-civic-json-file",
                  "url": "https://api.github.com/repos/codeforamerica/add-civic-json-test/git/refs/heads/add-civic-json-file",
                  "object": {
                    "sha": "d442f4ab6fd4043436c8c80a072cb798d8b467ce",
                    "type": "commit",
                    "url": "https://api.github.com/repos/codeforamerica/add-civic-json-test/git/commits/d442f4ab6fd4043436c8c80a072cb798d8b467ce"
                  }
                }''', {'Content-Type': 'application/json; charset=utf-8'})

        # get a branch
        # https://developer.github.com/v3/git/refs/#get-a-reference
        if url.geturl() == 'https://api.github.com/repos/codeforamerica/add-civic-json-test/git/refs/heads/master' and request.method == 'GET':
            return httmock.response(200, '''
                {
                  "ref": "refs/heads/master",
                  "url": "https://api.github.com/repos/codeforamerica/add-civic-json-test/git/refs/heads/master",
                  "object": {
                    "sha": "571317b2562617aaf3c7e418a8bdf3caee4b32c7",
                    "type": "commit",
                    "url": "https://api.github.com/repos/codeforamerica/add-civic-json-test/git/commits/571317b2562617aaf3c7e418a8bdf3caee4b32c7"
                  }
                }''', {'Content-Type': 'application/json; charset=utf-8'})

        # create a branch
        # https://developer.github.com/v3/git/refs/#create-a-reference
        if url.geturl() == 'https://api.github.com/repos/codeforamerica/add-civic-json-test/git/refs' and request.method == 'POST':
            return httmock.response(201, '''
                {
                  "ref": "refs/heads/add-civic-json-file",
                  "url": "https://api.github.com/repos/codeforamerica/add-civic-json-test/git/refs/heads/add-civic-json-file",
                  "object": {
                    "type": "commit",
                    "sha": "aa218f56b14c9653891f9e74264a383fa43fefbd",
                    "url": "https://api.github.com/repos/codeforamerica/add-civic-json-test/git/commits/aa218f56b14c9653891f9e74264a383fa43fefbd"
                  }
                }''', {'Content-Type': 'application/json; charset=utf-8'})

        # check for existence of civic.json file on a branch
        # https://developer.github.com/v3/repos/contents/#get-contents
        if url.geturl() == 'https://api.github.com/repos/codeforamerica/add-civic-json-test/contents/civic.json?ref=add-civic-json-file' and request.method == 'GET':
            return httmock.response(404, '''
                {
                  "message": "Not Found",
                  "documentation_url": "https://developer.github.com/v3"
                }''', {'Content-Type': 'application/json; charset=utf-8'})

        # reponse from successful creation of a civic.json file
        # (stripped out unused parameters)
        # https://developer.github.com/v3/repos/contents/#create-a-file
        if url.geturl() == 'https://api.github.com/repos/codeforamerica/add-civic-json-test/contents/civic.json' and request.method == 'PUT':
            return httmock.response(201, '''
                {
                  "commit": {
                    "message": "add civic.json file",
                    "sha": "d1fc79958a32d4cc102b0e725a5cab475ecc1dd1"
                  },
                  "content": {
                    "html_url": "https://github.com/codeforamerica/add-civic-json-test/blob/add-civic-json-file/civic.json",
                    "name": "civic.json",
                    "path": "civic.json",
                    "sha": "1224e749aeb4596b766ee4c6259f4bd1968c0488",
                    "size": 101,
                    "type": "file",
                    "url": "https://api.github.com/repos/codeforamerica/add-civic-json-test/contents/civic.json?ref=add-civic-json-file"
                  }
                }''', {'Content-Type': 'application/json; charset=utf-8'})

        # create a pull request
        # https://developer.github.com/v3/pulls/#create-a-pull-request
        if url.geturl() == 'https://api.github.com/repos/codeforamerica/add-civic-json-test/pulls' and request.method == 'POST':
            return self.civic_json_fork_content(url, request)

        raise ValueError('response_content: bad {} to "{}"'.format(request.method, url.geturl()))

    def civic_json_fork_content(self, url, request):
        ''' Mocking http responses when testing civic.json forks
        '''
        if url.geturl() == 'https://www.cfapi-staging.herokuapp.com/api/projects?name=add-civic-json-test&organization_id=Code-for-America' and request.method == 'GET':
            return httmock.response(200, '''
                {
                  "objects": [
                    {
                      "api_url": "http://www.cfapi-staging.herokuapp.com/api/projects/30943",
                      "categories": null,
                      "code_url": "https://github.com/codeforamerica/add-civic-json-test",
                      "description": "Use this project to test the automated creation of a pull request adding a civic.json file.",
                      "github_details": {},
                      "id": 30943,
                      "issues": [],
                      "languages": null,
                      "last_updated": "Wed, 25 Nov 2015 21:07:35 GMT",
                      "link_url": null,
                      "name": "add-civic-json-test",
                      "organization": {},
                      "organization_name": "Code for America",
                      "status": null,
                      "tags": {},
                      "type": null
                    }
                  ],
                  "pages": {},
                  "total": 1
                }''', {'Content-Type': 'application/json; charset=utf-8'})

        # Get a single GitHub user
        # (stripped out unused parameters)
        # https://developer.github.com/v3/users/#get-a-single-user
        if url.geturl() == 'https://api.github.com/user' and request.method == 'GET':
            return httmock.response(200, '''
                {
                  "login": "mhammy",
                  "avatar_url": "https://avatars.githubusercontent.com/u/8171936?v=3"
                }''', {'Content-Type': 'application/json; charset=utf-8'})

        # list pull requests
        # https://developer.github.com/v3/pulls/#list-pull-requests
        if url.geturl() == 'https://api.github.com/repos/codeforamerica/add-civic-json-test/pulls' and request.method == 'GET':
            return httmock.response(200, '''
                [

                ]''', {'Content-Type': 'application/json; charset=utf-8'})

        # get the target repo
        # (stripped out unused parameters)
        # https://developer.github.com/v3/repos/#get
        if url.geturl() == 'https://api.github.com/repos/codeforamerica/add-civic-json-test' and request.method == 'GET':
            return httmock.response(200, '''
                {
                  "name": "add-civic-json-test",
                  "full_name": "codeforamerica/add-civic-json-test",
                  "permissions": {
                    "push": false
                  },
                  "default_branch": "master"
                }''', {'Content-Type': 'application/json; charset=utf-8'})

        # create a fork
        # (stripped out unused parameters)
        # https://developer.github.com/v3/repos/forks/#response-1
        if url.geturl() == 'https://api.github.com/repos/codeforamerica/add-civic-json-test/forks' and request.method == 'POST':
            return httmock.response(202, '''
                {
                  "full_name" : "mhammy/add-civic-json-test",
                  "owner" : {
                      "login" : "mhammy"
                    },
                  "default_branch" : "master"
                }''', {'Content-Type': 'application/json; charset=utf-8'})

        # get the forked repo
        # (stripped out unused parameters)
        # https://developer.github.com/v3/repos/#get
        if url.geturl() == 'https://api.github.com/repos/mhammy/add-civic-json-test' and request.method == 'GET':
            return httmock.response(200, '''
                {
                  "id": 46887065,
                  "name": "add-civic-json-test",
                  "full_name": "mhammy/add-civic-json-test",
                  "owner": {},
                  "private": false,
                  "html_url": "https://github.com/mhammy/add-civic-json-test",
                  "description": "Use this project to test the automated creation of a pull request adding a civic.json file.",
                  "fork": true,
                  "url": "https://api.github.com/repos/mhammy/add-civic-json-test"
                }''', {'Content-Type': 'application/json; charset=utf-8'})

        # check for existence of civic.json file
        # https://developer.github.com/v3/repos/contents/#get-contents
        if url.geturl() == 'https://api.github.com/repos/mhammy/add-civic-json-test/contents/civic.json' and request.method == 'GET':
            return httmock.response(404, '''
                {
                  "message": "Not Found",
                  "documentation_url": "https://developer.github.com/v3"
                }''', {'Content-Type': 'application/json; charset=utf-8'})

        # reponse from successful creation of a civic.json file
        # (stripped out unused parameters)
        # https://developer.github.com/v3/repos/contents/#create-a-file
        if url.geturl() == 'https://api.github.com/repos/mhammy/add-civic-json-test/contents/civic.json' and request.method == 'PUT':
            return httmock.response(201, '''
                {
                  "commit": {
                    "message": "add civic.json file",
                    "sha": "88e7264c2f046d32fbdd15eda572c04663f7d216"
                  },
                  "content": {
                    "html_url": "https://github.com/mhammy/add-civic-json-test/blob/master/civic.json",
                    "name": "civic.json",
                    "path": "civic.json",
                    "sha": "70e1d3cb3b5cf1e510a9420eb9a56a78045def31",
                    "size": 125,
                    "type": "file",
                    "url": "https://api.github.com/repos/mhammy/add-civic-json-test/contents/civic.json?ref=master"
                  }
                }''', {'Content-Type': 'application/json; charset=utf-8'})

        # create a pull request
        # (stripped out unused parameters)
        # https://developer.github.com/v3/pulls/#create-a-pull-request
        if url.geturl() == 'https://api.github.com/repos/codeforamerica/add-civic-json-test/pulls' and request.method == 'POST':
            return httmock.response(201, '''
                {
                  "id": 1,
                  "html_url": "https://github.com/codeforamerica/add-civic-json-test/pull/1"
                }''', {'Content-Type': 'application/json; charset=utf-8'})

        else:
            return self.response_content(url, request)

    def response_content(self, url, request):
        if "list-manage.com/subscribe/post" in url.geturl():
            return httmock.response(200, '{ "status_code" : 200, "msg" : "Almost finished... We need to confirm your email address. To complete the subscription process, please click the link in the email we just sent you."}')
        if url.geturl() == 'http://www.codeforamerica.org/fragments/email-signup.html' or url.geturl() == 'http://www.codeforamerica.org/fragments/global-footer.html':
            return httmock.response(200, '''<html>bunch of HTML</html>''')
        if url.geturl() == 'https://www.cfapi-staging.herokuapp.com/api/organizations/404':
            return httmock.response(404, '{"status": "Resource Not Found"}')
        if url.geturl() == 'https://www.cfapi-staging.herokuapp.com/api/organizations/Code-for-San-Francisco':
            return httmock.response(200, '{"city": "San Francisco, CA"}')
        if url.geturl() == "https://www.cfapi-staging.herokuapp.com/api/organizations.geojson":
            return httmock.response(200, '{"features" : [{ "properties" : { "id" : "TEST-ORG", "type" : "Brigade" } } ] }')
        if url.geturl() == "https://www.cfapi-staging.herokuapp.com/api/attendance":
            return httmock.response(200, '{"total": 100, "weekly" : {"1999" : "100"}}')
        if url.geturl() == "https://www.cfapi-staging.herokuapp.com/api/projects/1":
            return httmock.response(200, '''
                    {
                      "code_url": "https://github.com/jmcelroy5/sf-in-progress",
                      "description": "Engaging San Francisco Citizens in the housing development process through data and technology.",
                      "link_url": "http://107.170.214.244/",
                      "code_url": "https://github.com/testesttest/test",
                      "last_updated": "Mon, 10 Aug 2015 23:22:40 GMT",
                      "name": "SF in Progress",
                      "github_details" : {},
                      "organization": {
                        "id": "Code-for-San-Francisco",
                        "name": "Code for San Francisco"
                      },
                      "organization_name": "Code for San Francisco",
                      "status": "Alpha",
                      "tags": "housing, ndoch, active"
                    } ''')

        if "q=TEST" in url.geturl() or "organization_type=Brigade" in url.geturl() or "status=Alpha" in url.geturl():
            return httmock.response(200, '''{
                  "objects": [
                    {
                      "code_url": "TEST URL",
                      "description": "TEST DESCRIPTION",
                      "link_url": "TEST URL",
                      "last_updated": "Mon, 10 Aug 2015 23:22:40 GMT",
                      "name": "TEST PROJECT",
                      "github_details" : {},
                      "organization": {
                        "id": "Code-for-San-Francisco",
                        "name": "Code for San Francisco"
                      },
                      "organization_name": "Code for San Francisco",
                      "status": "Alpha",
                      "tags": "housing, ndoch, active"
                    }
                  ],
                  "total" : 1,
                  "pages": {}
                } ''')

        if "https://www.cfapi-staging.herokuapp.com/api/projects" in url.geturl():
            return httmock.response(200, '''{
                  "objects": [
                    {
                      "code_url": "https://github.com/jmcelroy5/sf-in-progress",
                      "description": "Engaging San Francisco Citizens in the housing development process through data and technology.",
                      "link_url": "http://107.170.214.244/",
                      "last_updated": "Mon, 10 Aug 2015 23:22:40 GMT",
                      "name": "SF in Progress",
                      "github_details" : {},
                      "organization": {
                        "id": "Code-for-San-Francisco",
                        "name": "Code for San Francisco"
                      },
                      "organization_name": "Code for San Francisco",
                      "status": "Alpha",
                      "tags": "housing, ndoch, active"
                    }
                  ],
                  "total" : 1,
                  "pages": {}
                } ''')

        if url.geturl() == 'https://people.codeforamerica.org/brigade/signup':
            if request.method == 'POST':
                form = dict(parse_qsl(request.body))
                username, password = None, None

                if 'Authorization' in request.headers:
                    method, encoded = request.headers['Authorization'].split(' ', 1)
                    if method == 'Basic':
                        username, password = b64decode(encoded).split(':', 1)

                if (username, password) == (os.environ['BRIGADE_SIGNUP_SECRET'], 'x-brigade-signup'):
                    return httmock.response(200, 'Added to the peopledb')

                if form.get('BRIGADE_SIGNUP_SECRET') == os.environ['BRIGADE_SIGNUP_SECRET']:
                    return httmock.response(200, 'Added to the peopledb')

                return httmock.response(401, 'Go away')

        if url.geturl() == 'https://people.codeforamerica.org/checkin':
            if request.method == 'POST':
                form = dict(parse_qsl(request.body))
                username, password = None, None

                if 'Authorization' in request.headers:
                    method, encoded = request.headers['Authorization'].split(' ', 1)
                    if method == 'Basic':
                        username, password = b64decode(encoded).split(':', 1)

                if (username, password) == (os.environ['BRIGADE_SIGNUP_SECRET'], 'x-brigade-signup'):
                    return httmock.response(200, 'Added checkin')

                return httmock.response(401, 'Go away')

            raise NotImplementedError()

        if 'repos/testesttest/test/forks' in url.geturl():
            return httmock.response(200, ''' {
                    "name" : "TEST NAME",
                    "full_name" : "TEST FULL NAME",
                    "owner" : { "login" : "ondrae" },
                    "default_branch" : "master"
                    } ''')

        raise ValueError('response_content: bad {} to "{}"'.format(request.method, url.geturl()))

    def test_signup(self):
        ''' Test that main page signups work '''
        signup = {
            "FNAME": "FIRST NAME",
            "LNAME": "LAST NAME",
            "EMAIL": "EMAIL",
            "mailchimp_url": None,
            "brigade_id": "FAKE-BRIGADE-ID"
        }

        # Test that our data is going through
        with self.app.test_request_context("/brigade/signup/", method="POST", data=signup):
            self.assertEqual(flask.request.form.get("FNAME"), "FIRST NAME")
            self.assertEqual(flask.request.form.get("LNAME"), "LAST NAME")
            self.assertEqual(flask.request.form.get("EMAIL"), "EMAIL")

        # Test that our responses are being packaged up the way we expect
        with httmock.HTTMock(self.response_content):
            response = self.client.post('/brigade/signup/', data=signup)
            response = json.loads(response.data)
            self.assertEqual(response['msg'], "Added to the peopledb")

    def test_old_brigade_links(self):
        ''' Test that the old brigade links are being redirected '''
        with httmock.HTTMock(self.response_content):
            response = self.client.get("/brigade/index/Code-for-San-Francisco/")
            self.assertEqual(301, response.status_code)

    def test_good_links(self):
        ''' Test that normal Brigade links are working '''
        response = self.client.get("/brigade/Code-for-San-Francisco/")
        self.assertEqual(200, response.status_code)

    def test_404(self):
        ''' Test for 404 links '''
        with httmock.HTTMock(self.response_content):
            response = self.client.get("/brigade/404/")
            self.assertEqual(404, response.status_code)

    def test_attendance(self):
        ''' Test attendance endpoints '''
        with httmock.HTTMock(self.response_content):
            response = self.client.get("/brigade/attendance")
            self.assertEqual(response.status_code, 200)
            self.assertTrue('<p class="h1">100</p>' in response.data)

    def test_checkin(self):
        ''' Test checkin '''
        checkin = {
            "name": "TEST NAME",
            "email": "test@testing.com",
            "event": "TEST EVENT",
            "cfapi_url": "https://www.cfapi-staging.herokuapp.com/api/organizations/TEST-ORG",
            "question": "TEST QUESTION",
            "answer": "TEST ANSWER"
        }

        with httmock.HTTMock(self.response_content):
            response = self.client.post("/brigade/checkin/", data=checkin, follow_redirects=True)
            self.assertEqual(200, response.status_code)

        checkin["question"] = None
        checkin["answer"] = None
        with httmock.HTTMock(self.response_content):
            response = self.client.post("/brigade/checkin/", data=checkin, follow_redirects=True)
            self.assertEqual(200, response.status_code)

        # test nonexistant Brigade
        checkin["cfapi_url"] = "http://www.cfapi-staging.herokuapp.com/api/organizations/BLAH-BLAH"
        response = self.client.post("/brigade/checkin/", data=checkin)
        self.assertEqual(422, response.status_code)

        # test http
        checkin["cfapi_url"] = "http://www.cfapi-staging.herokuapp.com/api/organizations/Code-for-San-Francisco"
        response = self.client.post("/brigade/checkin/", data=checkin)
        self.assertEqual(422, response.status_code)

        # test missing cfapi_url
        checkin["cfapi_url"] = None
        response = self.client.post("/brigade/checkin/", data=checkin)
        self.assertEqual(422, response.status_code)

    def test_test_checkin(self):
        ''' Test the test-checkin route '''
        checkin = {
            "name": "TEST NAME",
            "email": "test@testing.com",
            "event": "TEST EVENT",
            "cfapi_url": "https://www.cfapi-staging.herokuapp.com/api/organizations/Code-for-San-Francisco",
            "question": "TEST QUESTION",
            "answer": "TEST ANSWER"
        }

        response = self.client.post("/brigade/test-checkin/", data=checkin)
        self.assertEqual(200, response.status_code)

        # test nonexistant Brigade
        checkin["cfapi_url"] = "http://www.cfapi-staging.herokuapp.com/api/organizations/BLAH-BLAH"
        response = self.client.post("/brigade/test-checkin/", data=checkin)
        self.assertEqual(422, response.status_code)

        # test http
        checkin["cfapi_url"] = "http://www.cfapi-staging.herokuapp.com/api/organizations/Code-for-San-Francisco"
        response = self.client.post("/brigade/test-checkin/", data=checkin)
        self.assertEqual(422, response.status_code)

        # test bad url
        checkin["cfapi_url"] = "https://cfapi-staging.herokuapp.com/api/organizations/Code-for-San-Francisco"
        response = self.client.post("/brigade/test-checkin/", data=checkin)
        self.assertEqual(422, response.status_code)

        # test missing cfapi_url
        checkin["cfapi_url"] = None
        response = self.client.post("/brigade/test-checkin/", data=checkin)
        self.assertEqual(422, response.status_code)

    def test_existing(self):
        ''' Test that these org ids exist '''
        self.assertTrue(view_functions.is_existing_organization("Code-for-America"))
        self.assertFalse(view_functions.is_existing_organization("TEST-TEST"))

    def test_projects_page(self):
        ''' Test that the project page loads and looks like what we want '''
        with httmock.HTTMock(self.response_content):
            response = self.client.get("/brigade/projects")
            soup = BeautifulSoup(response.data, "html.parser")
            card_head_div = soup.find('div', {'class': 'card-head Alpha'})
            self.assertIsNotNone(card_head_div)
            self.assertEqual(u'Alpha', card_head_div.text.strip())

    def test_projects_searches(self):
        ''' Test the different project searches '''
        with httmock.HTTMock(self.response_content):
            response = self.client.get("/brigade/projects?q=TEST")
            soup = BeautifulSoup(response.data, "html.parser")
            project_name = soup.find_all('h3')
            self.assertEqual(u"TEST PROJECT", project_name[1].text.strip())

            response = self.client.get("/brigade/projects?organization_type=Brigade")
            soup = BeautifulSoup(response.data, "html.parser")
            project_name = soup.find_all('h3')
            self.assertEqual(u"TEST PROJECT", project_name[1].text.strip())

            response = self.client.get("/brigade/projects?status=Alpha")
            soup = BeautifulSoup(response.data, "html.parser")
            project_name = soup.find_all('h3')
            self.assertEqual(u"TEST PROJECT", project_name[1].text.strip())

    def test_project_monitor(self):
        ''' Test the project monitor page works as expected '''
        with httmock.HTTMock(self.response_content):
            response = self.client.get("/brigade/projects/monitor")
            self.assertTrue('"travis_url": "https://api.travis-ci.org/repositories/jmcelroy5/sf-in-progress/builds"' in response.data)

    def test_civic_tags_processed(self):
        ''' Tag lists entered via the civic.json form will be processed as expected
        '''
        tags = u'blacktip,,,collared,grey nurse,   hound,lemon,lemon, nervous, silky,thresher ,nervous,'
        expected_tags = [u'blacktip', u'collared', u'grey nurse', u'hound', u'lemon', u'nervous', u'silky', u'thresher']
        processed_tags = view_functions.process_tags(tags)
        self.assertEqual(processed_tags, expected_tags)

    def test_successful_civic_json_fork_submission(self):
        ''' Using the form to create a civic.json pull request works.
        '''
        with httmock.HTTMock(self.civic_json_fork_content):
            # Test PR
            data = {
                "status": u"Beta",
                "tags": u"glass,humboldt,bigfin,colossal,bush-club,grimaldi scaled,whiplash,market,japanese flying"
            }
            response = self.client.post("/brigade/Code-for-America/projects/add-civic-json-test/add-civic-json", data=data)

        # if the process was successful the response should be a redirect to the pull request on github
        self.assertEqual(302, response.status_code)
        self.assertEqual('https://github.com/codeforamerica/add-civic-json-test/pull/1', response.location)

    def test_civic_json_submission_matches_form(self):
        ''' The civic.json that's submitted to GitHub matches what was submitted in the form
        '''
        data = {
            "status": u"Official",
            "tags": u"allium, bachelor,camellia,  dahlia,foxglove,bachelor,gas  ,hardy,hardy,impatien,jupiter,kerria"
        }

        def test_civic_json_put(url, request):
            if url.geturl() == 'https://api.github.com/repos/mhammy/add-civic-json-test/contents/civic.json' and request.method == 'PUT':
                submitted_civic_json = json.loads(b64decode(json.loads(request.body)['content']))
                self.assertEqual(submitted_civic_json['status'], u'Official')
                self.assertEqual(submitted_civic_json['tags'], [u'allium', u'bachelor', u'camellia', u'dahlia', u'foxglove', u'gas', u'hardy', u'impatien', u'jupiter', u'kerria'])

            return self.civic_json_fork_content(url, request)

        with httmock.HTTMock(test_civic_json_put):
            response = self.client.post("/brigade/Code-for-America/projects/add-civic-json-test/add-civic-json", data=data)

        # if the process was successful the response should be a redirect to the pull request on github
        self.assertEqual(302, response.status_code)
        self.assertEqual('https://github.com/codeforamerica/add-civic-json-test/pull/1', response.location)

    def test_civic_json_submission_with_non_latin_characters(self):
        ''' Submitting non-latin characters through the civic.json form doesn't error.
        '''
        with httmock.HTTMock(self.civic_json_fork_content):
            # Test PR
            data = {
                "status": u"Beta",
                "tags": u"玻璃,具体,焦油,沥青,碎石,铁"
            }
            response = self.client.post("/brigade/Code-for-America/projects/add-civic-json-test/add-civic-json", data=data)

        # if the process was successful the response should be a redirect to the pull request on github
        self.assertEqual(302, response.status_code)
        self.assertEqual('https://github.com/codeforamerica/add-civic-json-test/pull/1', response.location)

    def test_civic_json_submission_with_no_form_data(self):
        ''' Trying to submit an empty form to create a civic.json file loads an error message.
        '''
        with httmock.HTTMock(self.civic_json_fork_content):
            data = {
                "status": u"",
                "tags": u""
            }
            response = self.client.post("/brigade/Code-for-America/projects/add-civic-json-test/add-civic-json", data=data)

        self.assertEqual(200, response.status_code)
        soup = BeautifulSoup(response.data, "html.parser")
        self.assertEqual(u'Please enter status and/or tags for the project!', soup.find('p', {'data-test-id': 'error-message'}).text)

    def test_successful_civic_json_branch_submission(self):
        ''' Using the form to create a civic.json pull request with a branch works.
        '''

        reject_limit = [1]

        # return a 404 the first time we check for a branch
        def test_civic_json_no_branch_once(url, request):
            if url.geturl() == 'https://api.github.com/repos/codeforamerica/add-civic-json-test/git/refs/heads/add-civic-json-file' and request.method == 'GET' and reject_limit[0] > 0:
                reject_limit[0] = reject_limit[0] - 1
                return httmock.response(404, '''
                    {
                      "message": "Not Found",
                      "documentation_url": "https://developer.github.com/v3"
                    }''', {'Content-Type': 'application/json; charset=utf-8'})

            # return the standard response to all requests that make it here
            return self.civic_json_fork_content(url, request)

        with httmock.HTTMock(test_civic_json_no_branch_once):
            # Test PR
            data = {
                "status": u"Beta",
                "tags": u"glass,humboldt,bigfin,colossal,bush-club,grimaldi scaled,whiplash,market,japanese flying"
            }
            response = self.client.post("/brigade/Code-for-America/projects/add-civic-json-test/add-civic-json", data=data)

        # if the process was successful the response should be a redirect to the pull request on github
        self.assertEqual(302, response.status_code)
        self.assertEqual('https://github.com/codeforamerica/add-civic-json-test/pull/1', response.location)

    def test_civic_json_fork_exists_after_delay(self):
        ''' If we get a 404 from GitHub, the script keeps trying until it gets a 200.
        '''
        data = {
            "status": u"Alpha",
            "tags": u"aynte of tegea, cleobulina, consort ban, corinna, cornificia, elephantis, enheduanna, erinna"
        }

        # return a 404 for the fork URL this many times before saying that it's there
        reject_limit = [2]

        def test_civic_json_fork_delayed(url, request):
            if url.geturl() == 'https://api.github.com/repos/mhammy/add-civic-json-test' and request.method == 'GET' and reject_limit[0] > 0:
                reject_limit[0] = reject_limit[0] - 1
                return httmock.response(404, '''
                    {
                      "message": "Not Found",
                      "documentation_url": "https://developer.github.com/v3"
                    }''', {'Content-Type': 'application/json; charset=utf-8'})

            # return the standard response to all requests that make it here
            return self.civic_json_fork_content(url, request)

        with httmock.HTTMock(test_civic_json_fork_delayed):
            response = self.client.post("/brigade/Code-for-America/projects/add-civic-json-test/add-civic-json", data=data)

        # verify that the reject limit was exhausted
        self.assertTrue(reject_limit[0] <= 0)

        # if the process was successful the response should be a redirect to the pull request on github
        self.assertEqual(302, response.status_code)
        self.assertEqual('https://github.com/codeforamerica/add-civic-json-test/pull/1', response.location)

if __name__ == '__main__':
    unittest.main()
