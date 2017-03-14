from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest, time


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(10)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):

        # Jack has heard about a new cool to-do list app
        # He goes to check out its homepage
        self.browser.get(self.live_server_url)

        # He Notices the page title and header mentions to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # He is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # He types 'buy new water bottle and cage' into a text box
        inputbox.send_keys('buy new water bottle and cage')

        # When he hits enter the page updates and now the page lists
        # "1: buy new water bottle and cage" as an item in the to-do list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(0.2)
        jack_lists_url = self.browser.current_url
        self.assertRegex(jack_lists_url, '/lists/.+')
        self.check_for_row_in_list_table('1: buy new water bottle and cage')

        # There is still a text box inviting him to enter another item
        # he adds 'clean bicycle'
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('clean bicycle')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again and he can now see both items
        self.check_for_row_in_list_table('1: buy new water bottle and cage')
        self.check_for_row_in_list_table('2: clean bicycle')

        # Now a user Nicole comes along to the site

        # We use a new browser session to make sure no information
        # of Jack's is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Nicole visits the homepage, there is no sign of Jack's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('buy new water bottle and cage', page_text)
        self.assertNotIn('clean bicycle', page_text)

        # Nicole starts a new list by entering a new item, she is
        # less interesting than Jack
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy Milk')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(0.2)

        # Nicole gets her own unique url
        nicole_lists_url = self.browser.current_url
        self.assertRegex(nicole_lists_url, '/lists/.+')
        self.assertNotEqual(jack_lists_url, nicole_lists_url)

        # Again there is no sight of Jack's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('buy new water bottle and cage', page_text)
        self.assertIn('Buy Milk', page_text)

    # Helper methods ------
    def check_for_row_in_list_table(self, row_text):
        time.sleep(0.2)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')

        self.assertIn(row_text, [row.text for row in rows])






