from django.core import mail
import os
import poplib
import re
import time
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
from .list_page import ListPage

SUBJECT = 'Your login link for Superlists'


class LoginTest(FunctionalTest):

    def wait_for_email(self, test_email, subject):
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body

        email_id = None
        start = time.time()
        try:
            while time.time() - start < 60:
                inbox = poplib.POP3_SSL(os.environ['POP3_SSL'])
                inbox.user(test_email)
                inbox.pass_(os.environ['TEST_EMAIL_PASSWORD'])

                # get 10 newest messages
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count - 10), count + 1)):
                    print('getting msg', i)
                    _, lines, __ = inbox.retr(i)
                    lines = [l.decode('utf8') for l in lines]
                    if f'Subject: {subject}' in lines:
                        email_id = i
                        body = '\n'.join(lines)
                        return body

                inbox.quit()
                time.sleep(5)

        finally:
            if email_id:
                inbox.dele(email_id)
            inbox.quit()

    def test_can_get_email_link_to_log_in(self):
        # Edith goes to the awesome superlists site and notices a "Log in"
        # section in the navbar for the first time. It's telling her to ender
        # her email address, so she does
        if self.staging_server:
            test_email = f'recent:{os.environ["TEST_EMAIL"]}'
        else:
            test_email = 'edith@example.com'

        self.browser.get(self.live_server_url)
        list_page = ListPage(self)
        list_page.get_email_box().send_keys(test_email)
        list_page.get_email_box().send_keys(Keys.ENTER)

        # A message appears telling her an email has been sent
        self.wait_for(lambda: self.assertIn(
            'Check your email',
            self.browser.find_element_by_tag_name('body').text
        ))

        # She checks her email and finds a message
        body = self.wait_for_email(test_email, SUBJECT)

        # It has a url link in it
        self.assertIn('Use this link to log in', body)
        url_search = re.search(r'http://.+/.+$', body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # She clicks it
        self.browser.get(url)

        # She is logged in!
        list_page.wait_to_be_logged_in(test_email)

        # Now she logs out
        list_page.get_logout_link().click()

        # She is logged out
        list_page.wait_to_be_logged_out(test_email)
