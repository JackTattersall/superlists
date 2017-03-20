from .base import FunctionalTest


class LoginTest(FunctionalTest):

    def test_login(self):
        # Edith navigates to the superlists site and notices a log in page
        self.browser.get(self.live_server_url)
        page_name = self.browser.find_element_by_tag_name('h1')
        self.assertEqual(page_name.text, 'Please sign in!')

        # She then enters her login details
        user_name_field = self.browser.find_element_by_id('id_username')
        user_name_field.send_keys('jack')
        password_field = self.browser.find_element_by_id('id_password')
        password_field.send_keys('paigeleah1')

        # When she presses the login button she is logged in
        login_button = self.browser.find_element_by_id('id_sign_in')
        login_button.click()
        self.wait_for(lambda: self.browser.find_elements_by_id(
            'id_logout'))

        # She then decides to log out and clicks the logout button and is then logged out
        logout_button = self.browser.find_element_by_id('id_logout')
        logout_button.click()
        page_name = self.wait_for(lambda: self.browser.find_elements_by_tag_name(
            'h1'))
        self.assertEqual(page_name.text, 'Login')