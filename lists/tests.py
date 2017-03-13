import os

from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page
import re


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
        expected_html = remove('csrfmiddlewaretoken', expected_html)
        print(expected_html)

        response_html = remove('csrfmiddlewaretoken', response.content.decode())
        print(response_html)

        self.assertEqual(response_html, expected_html, expected_html + "\n\n\n\n" + response_html)

    def test_homepage_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'                         # set the request to a POST
        request.POST['item_text'] = 'A new list item'   # post this text into the named input 'item_text'

        response = home_page(request)                   # capture the response

        # assert that the input text appears in the response html
        self.assertIn('A new list item', response.content.decode())

        expected_html = render_to_string(
            'home.html',
            {'new_item_text': 'A new list item'}
        )

        self.assertIn('A new list item', expected_html)


# Function that removes a line from a string if the line contains 'rem' and removes empty lines also
def remove(rem, my_string):
    my_string = re.sub(".*" + rem + ".*\n?", "", my_string)
    my_string = os.linesep.join([s for s in my_string.splitlines() if s.strip()])
    return my_string


