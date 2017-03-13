from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page


# Create your tests here.
class HomePageTest(TestCase):

    # resolves that the function called when the route '/' is navigated to is home_page
    def test_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()            # create a request object
        response = home_page(request)      # pass it to our home_page view and store the response html
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)


