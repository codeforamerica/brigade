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
        if url.geturl() == 'https://people.codeforamerica.org/brigade/signup':
            return response(200, "Added to the peopledb")

    def test_signup(self):
        ''' Test that main page signups work '''
        signup = {
            "FNAME" : "FIRST NAME",
            "LNAME" : "LAST NAME",
            "EMAIL" : "EMAIL",
            "mailchimp_url" : "FAKE MAILCHIMP URL",
            "brigade_id" : "FAKE-BRIGADE-ID"
        }

        # Test that our data is going through
        with app.test_request_context("/signup/", method="POST", data=signup):
            self.assertEqual(flask.request.form.get("FNAME"), "FIRST NAME")
            self.assertEqual(flask.request.form.get("LNAME"), "LAST NAME")
            self.assertEqual(flask.request.form.get("EMAIL"), "EMAIL")

        # Test that our responses are being packaged up the way we expect
        with HTTMock(self.response_content):
            response = self.app.post('/signup/', data=signup)
            response = json.loads(response.data)
            self.assertEqual(response['msg'], 'Added to the peopledb')

        # Test that our responses are being packaged up the way we expect
        with HTTMock(self.response_content):
            response = self.app.post('/signup/', data=signup)
            response = json.loads(response.data)
            self.assertEqual(response['msg'], 'Added to the peopledb')

if __name__ == '__main__':
    unittest.main()
