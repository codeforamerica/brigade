from urlparse import parse_qsl
from base64 import b64decode
import unittest
import json
import os

import flask
from httmock import response, HTTMock

os.environ['BRIGADE_SIGNUP_SECRET'] = 'muy bueno'

from app import app

class BrigadeTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def response_content(self, url, request):
        if "list-manage.com/subscribe/post" in url.geturl():
            return response(200, '{ "status_code" : 200, "msg" : "Almost finished... We need to confirm your email address. To complete the subscription process, please click the link in the email we just sent you."}')
        if url.geturl() == 'http://www.codeforamerica.org/fragments/email-signup.html' \
        or url.geturl() == 'http://www.codeforamerica.org/fragments/global-footer.html':
            return response(200, '''<html>bunch of HTML</html>''')
        if url.geturl() == 'https://www.codeforamerica.org/api/organizations/404':
            return response(404, '{"status": "Resource Not Found"}')
        if url.geturl() == 'https://www.codeforamerica.org/api/organizations/Code-for-San-Francisco':
            return response(200, '{"city": "San Francisco, CA"}')
        if url.geturl() == "https://www.codeforamerica.org/api/organizations.geojson":
            return response(200, '{"features" : [{ "properties" : { "id" : "TEST-ORG", "type" : "Brigade" } } ] }')
        if url.geturl() == "https://www.codeforamerica.org/api/attendance":
            return response(200, '{"total": 100, "weekly" : {"1999" : "100"}}')
        if url.geturl() == "https://www.codeforamerica.org/api/projects":
            return response(200, '''{
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
                    return response(200, 'Added to the peopledb')
                
                if form.get('BRIGADE_SIGNUP_SECRET') == os.environ['BRIGADE_SIGNUP_SECRET']:
                    return response(200, 'Added to the peopledb')
            
                return response(401, 'Go away')

        if url.geturl() == 'https://people.codeforamerica.org/checkin':
            if request.method == 'POST':
                form = dict(parse_qsl(request.body))
                username, password = None, None

                if 'Authorization' in request.headers:
                    method, encoded = request.headers['Authorization'].split(' ', 1)
                    if method == 'Basic':
                        username, password = b64decode(encoded).split(':', 1)

                if (username, password) == (os.environ['BRIGADE_SIGNUP_SECRET'], 'x-brigade-signup'):
                    return response(200, 'Added checkin')

                return response(401, 'Go away')
            
            raise NotImplementedError()
        
        raise ValueError('Bad {} to "{}"'.format(request.method, url.geturl()))


    def test_signup(self):
        ''' Test that main page signups work '''
        signup = {
            "FNAME" : "FIRST NAME",
            "LNAME" : "LAST NAME",
            "EMAIL" : "EMAIL",
            "mailchimp_url" : None,
            "brigade_id" : "FAKE-BRIGADE-ID"
        }

        # Test that our data is going through
        with app.test_request_context("/brigade/signup/", method="POST", data=signup):
            self.assertEqual(flask.request.form.get("FNAME"), "FIRST NAME")
            self.assertEqual(flask.request.form.get("LNAME"), "LAST NAME")
            self.assertEqual(flask.request.form.get("EMAIL"), "EMAIL")

        # Test that our responses are being packaged up the way we expect
        with HTTMock(self.response_content):
            response = self.app.post('/brigade/signup/', data=signup)
            response = json.loads(response.data)
            self.assertEqual(response['msg'], "Added to the peopledb")


    def test_old_brigade_links(self):
        ''' Test that the old brigade links are being redirected '''
        with HTTMock(self.response_content):
            response = self.app.get("/brigade/index/Code-for-San-Francisco/")
        self.assertTrue(response.status_code == 301)


    def test_good_links(self):
        ''' Test that normal Brigade links are working '''
        response = self.app.get("/brigade/Code-for-San-Francisco/")
        self.assertTrue(response.status_code == 200)


    def test_404(self):
        ''' Test for 404 links '''
        with HTTMock(self.response_content):
            response = self.app.get("/brigade/404/")
        self.assertTrue(response.status_code == 404)


    def test_attendance(self):
        ''' Test attendance endpoints '''
        with HTTMock(self.response_content):
            response = self.app.get("/brigade/attendance")
            self.assertEqual(response.status_code, 200)
            self.assertTrue('<p class="h1">100</p>' in response.data)


    def test_checkin(self):
        ''' Test checkin '''
        checkin = {
            "name" : "TEST NAME",
            "email" : "test@testing.com",
            "event" : "TEST EVENT",
            "cfapi_url" : "https://www.codeforamerica.org/api/organizations/TEST-ORG",
            "question" : "TEST QUESTION",
            "answer" : "TEST ANSWER"
        }

        with HTTMock(self.response_content):
            response = self.app.post("/brigade/checkin/", data=checkin, follow_redirects=True)
            self.assertTrue(response.status_code == 200)

        checkin["question"] = None
        checkin["answer"] = None
        with HTTMock(self.response_content):
            response = self.app.post("/brigade/checkin/", data=checkin, follow_redirects=True)
            self.assertTrue(response.status_code == 200)

        # test nonexistant Brigade
        checkin["cfapi_url"] = "http://www.codeforamerica.org/api/organizations/BLAH-BLAH"
        response = self.app.post("/brigade/checkin/", data=checkin)
        self.assertTrue(response.status_code == 422)

        # test http
        checkin["cfapi_url"] = "http://www.codeforamerica.org/api/organizations/Code-for-San-Francisco"
        response = self.app.post("/brigade/checkin/", data=checkin)
        self.assertTrue(response.status_code == 422)

        # test missing cfapi_url
        checkin["cfapi_url"] = None
        response = self.app.post("/brigade/checkin/", data=checkin)
        self.assertTrue(response.status_code == 422)


    def test_test_checkin(self):
        ''' Test the test-checkin route '''
        checkin = {
            "name" : "TEST NAME",
            "email" : "test@testing.com",
            "event" : "TEST EVENT",
            "cfapi_url" : "https://www.codeforamerica.org/api/organizations/Code-for-San-Francisco",
            "question" : "TEST QUESTION",
            "answer" : "TEST ANSWER"
        }

        response = self.app.post("/brigade/test-checkin/", data=checkin)
        self.assertTrue(response.status_code == 200)

        # test nonexistant Brigade
        checkin["cfapi_url"] = "http://www.codeforamerica.org/api/organizations/BLAH-BLAH"
        response = self.app.post("/brigade/test-checkin/", data=checkin)
        self.assertTrue(response.status_code == 422)

        # test http
        checkin["cfapi_url"] = "http://www.codeforamerica.org/api/organizations/Code-for-San-Francisco"
        response = self.app.post("/brigade/test-checkin/", data=checkin)
        self.assertTrue(response.status_code == 422)

        # test bad url
        checkin["cfapi_url"] = "https://codeforamerica.org/api/organizations/Code-for-San-Francisco"
        response = self.app.post("/brigade/test-checkin/", data=checkin)
        self.assertTrue(response.status_code == 422)

        # test missing cfapi_url
        checkin["cfapi_url"] = None
        response = self.app.post("/brigade/test-checkin/", data=checkin)
        self.assertTrue(response.status_code == 422)


    def test_existing(self):
        ''' Test that these org ids exist '''
        from app import is_existing_organization
        self.assertTrue(is_existing_organization("Code-for-America"))
        self.assertFalse(is_existing_organization("TEST-TEST"))


    def test_projects_page(self):
        ''' Test that the prkject page loads and looks like what we want '''
        with HTTMock(self.response_content):
            response = self.app.get("/brigade/projects")
            self.assertTrue('<p>Status: <a href="?=Alpha" class="Alpha button-s">Alpha</a></p>' in response.data)



if __name__ == '__main__':
    unittest.main()
