from selenium.webdriver.common.keys import Keys
from .base import wait


class ListPage(object):

    def __init__(self, test):
        self.test = test

    def get_table_rows(self):
        return self.test.browser.find_elements_by_css_selector(
            '#id_list_table tr'
        )

    @wait
    def wait_for_row_in_list_table(self, item_text, item_number):
        expected_row_text = f'{item_number}: {item_text}'
        rows = self.get_table_rows()
        self.test.assertIn(expected_row_text, [row.text for row in rows])

    def get_item_input_box(self):
        return self.test.browser.find_element_by_id('id_text')

    def add_list_item(self, item_text):
        new_item_no = len(self.get_table_rows()) + 1
        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table(item_text, new_item_no)
        return self

    def get_share_box(self):
        return self.test.browser.find_element_by_css_selector(
            'input[name="sharee"]'
        )

    def get_shared_with_list(self):
        return self.test.browser.find_elements_by_css_selector('.list-shareee')

    def share_list_with(self, email):
        self.get_share_box().send_keys(email)
        self.get_share_box().send_keys(Keys.ENTER)
        self.test.wait_for(lambda: self.test.assertIn(
            email, [item.text for item in self.get_shared_with_list()]
        ))

    def get_email_box(self):
        return self.test.browser.find_element_by_name('email')

    def get_logout_link(self):
        return self.test.browser.find_element_by_link_text('Log out')

    def get_navbar(self):
        return self.test.browser.find_element_by_css_selector('.navbar')

    @wait
    def wait_to_be_logged_in(self, email):
        self.get_logout_link()
        navbar = self.get_navbar()
        self.test.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):
        self.get_email_box()
        navbar = self.get_navbar()
        self.test.assertNotIn(email, navbar.text)

    def get_my_lists_link(self):
        return self.test.browser.find_element_by_link_text('My lists')

    def get_header_text(self):
        return self.test.browser.find_element_by_tag_name('h1').text
