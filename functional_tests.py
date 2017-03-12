from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Jack has heard about a new cool to-do list app
        # He goes to check out its homepage
        self.browser.get('http://localhost:8000')

        # He Notices the page title and header mentions to-do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail("Finish the test")

        # He is invited to enter a to-do item straight away

        # He types 'buy new water bottle and cage' into a text box

        # When he hits enter the page updates and now the page lists
        # "1: buy new water bottle and cage" as an item in the to-do list

        # There is still a text box inviting him to enter another item
        # he adds 'clean bicycle'

        # The page updates again and he can now see both items

        # He wonders whether the site will remember his list, then he see's
        # that the site has generated a unique url for him, there is some explanatory
        # text to that effect.

        # He visits that url - his to-do list is still there

if __name__ == '__main__':
    unittest.main()





