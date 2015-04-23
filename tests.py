import unittest
import json

import flask
from httmock import response, HTTMock

from app import app

class BrigadeTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def response_content(self, url, request):
        print url.geturl()
        if "list-manage.com/subscribe/post" in url.geturl():
            return response(200, '{ "status_code" : 200, "msg" : "Almost finished... We need to confirm your email address. To complete the subscription process, please click the link in the email we just sent you."}')
        if url.geturl() == 'https://people.codeforamerica.org/brigade/signup':
            return response(200, "Added to the peopledb")

        if 'http://www.codeforamerica.org/api/projects?organization_type=Brigade' in url.geturl():
            return response(200, '''
            {
              "objects": [
                {
                  "api_url": "http://www.codeforamerica.org/api/projects/6573",
                  "categories": null,
                  "code_url": "https://github.com/codeforamerica/brigade",
                  "description": "The Code for America Brigade Website",
                  "github_details": None,
                  "id": 6573,
                  "issues": None,
                  "last_updated": "Thu, 23 Apr 2015 00:03:15 GMT",
                  "link_url": "https://www.codeforamerica.org/brigade/",
                  "name": "TESTING",
                  "organization": None,
                  "organization_name": "Code for America",
                  "status": null,
                  "tags": null,
                  "type": null
                }
              ],
              "pages": {
                "next": "https://www.codeforamerica.org/api/projects?organization_type=Brigade&page=2"
              },
              "total": 1
            }
            ''')

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


    def test_project_paging(self):
        with HTTMock(self.response_content):
            response = self.app.get("/brigade/projects/")
            self.assertTrue("?page=2" in response.data)


if __name__ == '__main__':
    unittest.main()
