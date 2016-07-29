# -- coding: utf-8 --
from urlparse import parse_qsl
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

    def response_content(self, url, request):
        if "list-manage.com/subscribe/post" in url.geturl():
            return httmock.response(200, '{ "status_code" : 200, "msg" : "Almost finished... We need to confirm your email address. To complete the subscription process, please click the link in the email we just sent you."}')
        if url.geturl() == 'http://www.codeforamerica.org/fragments/email-signup.html' or url.geturl() == 'http://www.codeforamerica.org/fragments/global-footer.html':
            return httmock.response(200, '''<html>bunch of HTML</html>''')
        if url.geturl() == 'https://www.codeforamerica.org/api/organizations/404':
            return httmock.response(404, '{"status": "Resource Not Found"}')
        if url.geturl() == 'https://www.codeforamerica.org/api/organizations/Code-for-San-Francisco':
            return httmock.response(200, '{"city": "San Francisco, CA"}')
        if url.geturl() == "https://www.codeforamerica.org/api/organizations.geojson":
            return httmock.response(200, '{"features" : [{ "properties" : { "id" : "TEST-ORG", "type" : "Brigade" } } ] }')
        if url.geturl() == "https://www.codeforamerica.org/api/projects/1":
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

        if "https://www.codeforamerica.org/api/projects" in url.geturl():
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

        raise ValueError('response_content: bad {} to "{}"'.format(request.method, url.geturl()))

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

if __name__ == '__main__':
    unittest.main()
