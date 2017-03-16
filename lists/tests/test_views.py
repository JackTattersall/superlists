import os
from django.utils.html import escape
from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page
from lists.models import Item, List
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


class ListViewTest(TestCase):

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='item1', list=correct_list)
        Item.objects.create(text='item2', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='other list item1', list=other_list)
        Item.objects.create(text='other list item2', list=other_list)

        response = self.client.get('/lists/%d/' % correct_list.id)

        self.assertContains(response, 'item1')
        self.assertContains(response, 'item2')
        self.assertNotContains(response, 'other list item1')
        self.assertNotContains(response, 'other list item2')

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % list_.id)
        self.assertTemplateUsed(response, 'list.html')

    def test_can_save_a_post_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            '/lists/%d/' % correct_list.id,
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/%d/' % correct_list.id,
            data={'item_text': 'A new item for an existing list'}
        )
        self.assertRedirects(response, '/lists/%d/' % correct_list.id)

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.get('/lists/%d/' % correct_list.id)

        self.assertEqual(response.context['list'], correct_list)


class NewListTest(TestCase):

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

        new_list = List.objects.first()

        # assert that the post redirects to
        self.assertRedirects(response, '/lists/%d/' % new_list.id)

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)


# <editor-fold desc = "Helper Functions" >
# Function that removes a line from a string if the line contains 'rem' and removes empty lines also
def remove(rem, my_string):
    my_string = re.sub(".*" + rem + ".*\n?", "", my_string)
    my_string = os.linesep.join([s for s in my_string.splitlines() if s.strip()])
    return my_string
# </editor-fold>


