# -- coding: utf-8 --
import unittest


import flask
import httmock
from bs4 import BeautifulSoup
from jinja2 import Markup
from mock import patch, Mock


from brigade import create_app
import cfapi


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
            return httmock.response(200, '''
                {
                    "features" : [{ 
                        "id": "TEST-ORG", 
                        "properties" : { 
                            "id": "TEST-ORG", 
                            "name": "Test Org",
                            "tags": ["Brigade", "Official", "Code for America"], 
                            "last_updated": 1510874211,
                            "city": "Oakland, CA"
                        } 
                    },
                    { 
                        "id": "Code-for-Atlantis",
                        "properties" : { 
                            "id": "Code-for-Atlantis", 
                            "name": "Code for Atlantis",
                            "tags": ["Brigade", "Official", "Code for America"], 
                            "last_updated": 1510874211,
                            "city": "Atlantis, GA"
                        } 
                    },
                    {
                        "id": "Code-for-Georgians",
                        "properties" : {
                            "id": "Code-for-Georgians",
                            "name": "Code for Georgians",
                            "tags": ["Brigade", "Official", "Code for America"],
                            "last_updated": 1510874211,
                            "city": "Georgia"
                        }
                    }]
                }''') # noqa
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
            response = self.client.get("/brigades/TEST-ORG/")
            self.assertEqual(200, response.status_code)

    def test_404(self):
        ''' Test for 404 links '''
        with httmock.HTTMock(self.response_content):
            response = self.client.get("/brigades/404/")
            self.assertEqual(404, response.status_code)
            response = self.client.get("/broken-link/")
            self.assertEqual(404, response.status_code)

    def test_projects_searches(self):
        ''' Test the different project searches '''
        with httmock.HTTMock(self.response_content):
            response = self.client.get("/projects?q=TEST")
            soup = BeautifulSoup(response.data, "html.parser")
            project_name = soup.find_all('h3')
            self.assertEqual(u"TEST PROJECT", project_name[0].text.strip())

            response = self.client.get("/projects?organization_type=Brigade")
            soup = BeautifulSoup(response.data, "html.parser")
            project_name = soup.find_all('h3')
            self.assertEqual(u"TEST PROJECT", project_name[0].text.strip())

            response = self.client.get("/projects?status=Alpha")
            soup = BeautifulSoup(response.data, "html.parser")
            project_name = soup.find_all('h3')
            self.assertEqual(u"TEST PROJECT", project_name[0].text.strip())

    def test_homepage_redirect(self):
        response = self.client.get("/brigade/")
        self.assertEqual(302, response.status_code)
        self.assertEqual(flask.url_for('.index', _external=True), response.location)

    def test_tools(self):
        # legacy test, can remove at some point
        response = self.client.get("/brigade/tools/")
        self.assertEqual(302, response.status_code)

    def test_software(self):
        response = self.client.get("/resources/software")
        self.assertEqual(200, response.status_code)

    def test_software_show(self):
        ''' test a couple common free software pages to make sure they render '''
        response = self.client.get("/resources/software/aws")
        self.assertEqual(200, response.status_code)
        response = self.client.get("/resources/software/heroku")
        self.assertEqual(200, response.status_code)
        response = self.client.get("/resources/software/gsuite")
        self.assertEqual(200, response.status_code)

    def test_sitemap(self):
        with httmock.HTTMock(self.response_content):
            response = self.client.get('/sitemap.xml')
            self.assertEqual(200, response.status_code)
            self.assertIn('<loc>http://localhost/brigades/TEST-ORG/</loc>', response.data)

    def test_filter_datetime(self):
        from filters import format_time
        test_time = "2018-12-25 18:30:00 -0800"
        formatted_time = format_time(test_time)
        self.assertEqual(formatted_time, "Tuesday, Dec 25, 2018 @ 6:30 PM")

    def test_join_list(self):
        from filters import join_list

        self.assertEqual(join_list([]), "")
        self.assertEqual(join_list(["thing"]), "thing")
        self.assertEqual(join_list(["thing", "other thing"]), "thing and other thing")
        self.assertEqual(join_list(["thing", "other thing", "last thing"]), "thing, other thing, and last thing")

        # test that it escapes html normally
        self.assertEqual(
            join_list(["<p>html</p>", "foo"]),
            "&lt;p&gt;html&lt;/p&gt; and foo"
        )
        self.assertEqual(
            join_list(["<p>html</p>", "foo", "bar"]),
            "&lt;p&gt;html&lt;/p&gt;, foo, and bar"
        )

        # test that it does not escape html in Markup objects
        self.assertEqual(
            join_list([Markup("<p>html</p>"), "foo"]),
            "<p>html</p> and foo"
        )
        self.assertEqual(
            join_list([Markup("<p>html</p>"), "foo", "bar"]),
            "<p>html</p>, foo, and bar"
        )

    def test_get_official_brigades_by_state(self):
        with httmock.HTTMock(self.response_content):
            from cfapi import get_official_brigades_by_state
            brigades = get_official_brigades_by_state()
            self.assertEqual(len(brigades), 2)
            self.assertIn("Georgia", brigades)
            self.assertEquals(brigades["Georgia"][0]['id'], "Code-for-Atlantis")
            self.assertEquals(brigades["Georgia"][1]['id'], "Code-for-Georgians")

    def test_nav_link(self):
        from filters import nav_link

        self.assertEqual(nav_link('brigade.events', 'Events'),
            "<a href='/events'>Events</a>")

        self.assertEqual(nav_link('brigade.events', 'Events', class_name="foo"),
            "<a href='/events' class='foo'>Events</a>")

        # when not on the active page
        self.assertEqual(nav_link('brigade.events', 'Events', class_name="foo", active_class_name="foo-active"),
            "<a href='/events' class='foo'>Events</a>")

    def test_nav_link_on_active_page(self):
        from filters import nav_link
        flask.request.path = '/events'
        self.assertEqual(nav_link('brigade.events', 'Events', class_name="foo", active_class_name="foo-active"),
                "<a href='/events' class='foo foo-active'>Events</a>")

        # when on a sub-page of a link
        flask.request.path = '/events/some-event'
        self.assertEqual(nav_link('brigade.events', 'Events', class_name="foo", active_class_name="foo-active"),
                "<a href='/events' class='foo foo-active'>Events</a>")


if __name__ == '__main__':
    unittest.main()
