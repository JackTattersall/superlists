import os

from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page
from lists.models import Item
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

        response_html = remove('csrfmiddlewaretoken', response.content.decode())

        self.assertEqual(response_html, expected_html)


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'The second list item'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first list item')
        self.assertEqual(second_saved_item.text, 'The second list item')


class ListViewTest(TestCase):
    def test_displays_all_items(self):
        Item.objects.create(text='item1')
        Item.objects.create(text='item2')

        response = self.client.get('/lists/only-list/')

        self.assertContains(response, 'item1')
        self.assertContains(response, 'item2')

    def test_uses_list_template(self):
        response = self.client.get('/lists/only-list/')
        self.assertTemplateUsed(response, 'list.html')


class NewListTets(TestCase):

    def test_saving_a_POST_request(self):
        self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )

        self.assertEqual(Item.objects.count(), 1)       # check that 1 new item has been saved to the database
        new_item = Item.objects.first()                 # grabs the first entry
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_post(self):
        response = self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )

        # assert that the post redirects to '/'
        self.assertRedirects(response, '/lists/only-list/')

# <editor-fold desc = "Helper Functions" >
# Function that removes a line from a string if the line contains 'rem' and removes empty lines also
def remove(rem, my_string):
    my_string = re.sub(".*" + rem + ".*\n?", "", my_string)
    my_string = os.linesep.join([s for s in my_string.splitlines() if s.strip()])
    return my_string
# </editor-fold>


