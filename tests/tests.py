# -- coding: utf-8 --
import unittest
import flask
import httmock
import cfapi
from brigade import create_app
from bs4 import BeautifulSoup


class BrigadeTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def response_content(self, url, request):
        if "list-manage.com/subscribe/post" in url.geturl():
            return httmock.response(200, '{ "status_code" : 200, "msg" : "Almost finished... We need to confirm your email address. To complete the subscription process, please click the link in the email we just sent you."}') # noqa
        if url.geturl() == 'http://www.codeforamerica.org/fragments/email-signup.html' or url.geturl() == 'http://www.codeforamerica.org/fragments/global-footer.html': # noqa
            return httmock.response(200, '''<html>bunch of HTML</html>''')
        if url.geturl() == cfapi.BASE_URL + '/organizations/404':
            return httmock.response(404, '{"status": "Resource Not Found"}')
        if url.geturl() == cfapi.BASE_URL + '/organizations/TEST-ORG':
            return httmock.response(200, '{"city": "San Francisco, CA", "type": "Brigade", "name": "Code for San Francisco"}') # noqa
        if url.geturl() == cfapi.BASE_URL + "/organizations.geojson":
            return httmock.response(200, '{"features" : [{ "id": "TEST-ORG", "properties" : { "id" : "TEST-ORG", "type" : "Brigade", "last_updated": 1510874211 } } ] }') # noqa
        if url.geturl() == cfapi.BASE_URL + "/projects/1":
            return httmock.response(200, '''
                {
                    "code_url": "https://github.com/jmcelroy5/sf-in-progress",
                    "description": "Engaging San Francisco Citizens in the housing development
                        process through data and technology.",
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

        if "q=TEST" in url.geturl() or "organization_type=Brigade" in url.geturl() or "status=Alpha" in url.geturl(): # noqa
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

        if url.path == '/api/projects':
            return httmock.response(200, '''{
                  "objects": [
                    {
                      "code_url": "https://github.com/jmcelroy5/sf-in-progress",
                      "description": "Engaging San Francisco Citizens in the housing development
                          process through data and technology.",
                      "commit_status": "success",
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
        with httmock.HTTMock(self.response_content):
            response = self.client.get("/brigade/TEST-ORG/")
            self.assertEqual(200, response.status_code)

    def test_404(self):
        ''' Test for 404 links '''
        with httmock.HTTMock(self.response_content):
            response = self.client.get("/brigade/404/")
            self.assertEqual(404, response.status_code)

    def test_projects_searches(self):
        ''' Test the different project searches '''
        with httmock.HTTMock(self.response_content):
            response = self.client.get("/brigade/projects?q=TEST")
            soup = BeautifulSoup(response.data, "html.parser")
            project_name = soup.find_all('h3')
            self.assertEqual(u"TEST PROJECT", project_name[0].text.strip())

            response = self.client.get("/brigade/projects?organization_type=Brigade")
            soup = BeautifulSoup(response.data, "html.parser")
            project_name = soup.find_all('h3')
            self.assertEqual(u"TEST PROJECT", project_name[0].text.strip())

            response = self.client.get("/brigade/projects?status=Alpha")
            soup = BeautifulSoup(response.data, "html.parser")
            project_name = soup.find_all('h3')
            self.assertEqual(u"TEST PROJECT", project_name[0].text.strip())

    def test_homepage_redirect(self):
        response = self.client.get("/")
        self.assertEqual(302, response.status_code)
        self.assertEqual(flask.url_for('.index', _external=True), response.location)

    def test_tools(self):
        # legacy test, can remove at some point
        response = self.client.get("/brigade/tools/")
        self.assertEqual(302, response.status_code)

    def test_free_software(self):
        response = self.client.get("/brigade/free-software/")
        self.assertEqual(200, response.status_code)

    def test_sitemap(self):
        with httmock.HTTMock(self.response_content):
            response = self.client.get('/sitemap.xml')
            self.assertEqual(200, response.status_code)
            self.assertIn('<loc>http://localhost/brigade/TEST-ORG/</loc>', response.data)


if __name__ == '__main__':
    unittest.main()
