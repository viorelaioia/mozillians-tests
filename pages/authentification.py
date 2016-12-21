#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import imaplib
import email

import time
from tempmail import TempMail
from selenium.webdriver.common.by import By

from pages.base import Base


class Authentification(Base):

    _login_with_email_button_locator = (By.CSS_SELECTOR, '.auth0-lock-passwordless-button.auth0-lock-passwordless-big-button')
    _email_input = (By.CSS_SELECTOR, '.auth0-lock-passwordless-pane>div>div>input')
    _send_email_button_locator = (By.CSS_SELECTOR, '.auth0-lock-passwordless-submit')
    _email_sent_successful_message_locator = (By.CSS_SELECTOR, '.auth0-lock-passwordless-confirmation>p')


    def sign_in(self, email):
        self.wait_for_element_visible(*self._login_with_email_button_locator)
        self.selenium.find_element(*self._login_with_email_button_locator).click()
        self.wait_for_element_visible(*self._email_input)
        self.selenium.find_element(*self._email_input).send_keys(email)
        self.selenium.find_element(*self._send_email_button_locator).click()
        # Wait for the email to be received 5 seconds after login
        time.sleep(5)

    def get_link(self, email_address, password):

        mail = imaplib.IMAP4_SSL('imap.mail.com', 993)
        mail.login(email_address, password)
        mail.list()
        mail.select('inbox')
        typ, data = mail.search(None, 'UNSEEN')
        for num in data[0].split():
            mail.store(num, '+FLAGS', '\\Seen')
        i = len(data[0].split())
        for x in range(i):
            latest_email_uid = data[0].split()[x]
            result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
            raw_email = email_data[0][1]
            raw_email_string = raw_email.decode('utf-8')
            email_message = email.message_from_string(raw_email_string)
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True)
                    mail = body.decode('utf-8').replace('\n', ' ').replace('amp;', '').split(" ")
                    for item in mail:
                        if item.startswith("http"):
                            return item
                else:
                    continue

    def get_link_from_new_user_email(self, email_address):
        temp_mail = TempMail(login=email_address.split('@')[0], domain="@"+email_address.split('@')[1])
        mails_list = temp_mail.get_mailbox()
        latest_mail = mails_list[len(mails_list) - 1]
        mail_text_index = latest_mail.keys().index("mail_text")
        mail = latest_mail.values()[mail_text_index]
        mail_content = mail.replace('\n', ' ').replace('amp;', '').split(" ")
        for item in mail_content:
            if item.startswith("http"):
                return item
