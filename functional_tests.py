from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: buy new water bottle and cage', [row.text for row in rows])

        # There is still a text box inviting him to enter another item
        # he adds 'clean bicycle'
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('clean bicycle')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again and he can now see both items
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: buy new water bottle and cage', [row.text for row in rows])
        self.assertIn('1: clean', [row.text for row in rows])

        # He wonders whether the site will remember his list, then he see's
        # that the site has generated a unique url for him, there is some explanatory
        # text to that effect.
        self.fail("Finish the tests")

        # He visits that url - his to-do list is still there

if __name__ == '__main__':
    unittest.main()





