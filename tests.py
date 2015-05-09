from urlparse import parse_qsl
from base64 import b64decode
import unittest
import json
import os

import flask
from httmock import response, HTTMock

from app import app

class BrigadeTests(unittest.TestCase):

    def setUp(self):
        os.environ['SECRET_KEY'] = 'muy bueno'
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
        if url.geturl() == 'https://people.codeforamerica.org/brigade/signup':
            if request.method == 'POST':
                form = dict(parse_qsl(request.body))
                
                if form.get('SECRET_KEY') == os.environ['SECRET_KEY']:
                    return response(200, 'Added to the peopledb')
            
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
        with HTTMock(self.response_content):
            response = self.app.get("/brigade/Code-for-San-Francisco/")
        self.assertTrue(response.status_code == 200)


    def test_404(self):
        ''' Test for 404 links '''
        with HTTMock(self.response_content):
            response = self.app.get("/brigade/404/")
        self.assertTrue(response.status_code == 404)


if __name__ == '__main__':
    unittest.main()
