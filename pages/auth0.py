# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import pyotp
import requests
from pypom import Page
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected

from pages.github import Github


class Auth0(Page):

    _email_locator = (By.ID, 'field-email')
    _enter_locator = (By.ID, 'enter-initial')
    _send_email_locator = (By.CSS_SELECTOR, 'button[data-handler=send-passwordless-link]')
    _login_with_github_button_locator = (By.CSS_SELECTOR, 'button[data-handler="authorise-github"]')
    _password_locator = (By.ID, 'field-password')
    _enter_button_locator = (By.ID, 'authorise-ldap-credentials')
    _enter_passcode_button_locator = (By.CSS_SELECTOR, '.passcode-label .positive.auth-button')
    _passcode_field_locator = (By.CSS_SELECTOR, '.passcode-label input[name="passcode"]')

    def request_login_link(self, username):
        self.wait.until(expected.visibility_of_element_located(
            self._email_locator)).send_keys(username)
        self.find_element(*self._enter_locator).click()
        self.wait.until(expected.visibility_of_element_located(
            self._send_email_locator)).click()

    def click_login_with_github(self):
        self.find_element(*self._login_with_github_button_locator).click()
        return Github(self.selenium, self.base_url)

    def login_with_ldap(self, email, password, counter_api, secret):
        self.wait.until(expected.visibility_of_element_located(
            self._email_locator)).send_keys(email)
        self.find_element(*self._enter_locator).click()
        self.wait.until(expected.visibility_of_element_located(
            self._password_locator)).send_keys(password)
        self.find_element(*self._enter_button_locator).click()
        self.selenium.switch_to_frame('duo_iframe')
        self.find_element(*self._enter_passcode_button_locator).click()

        # Counter API is needed for generating counter-based OTPs and it increases its value everytime it gets called
        # https://github.com/pyotp/pyotp#counter-based-otps
        counter = requests.get(counter_api).json()
        passcode = pyotp.HOTP(secret).at(counter)
        passcode_field = self.find_element(*self._passcode_field_locator)
        passcode_field.clear()
        passcode_field.send_keys(passcode)
        self.find_element(*self._enter_passcode_button_locator).click()
        self.selenium.switch_to_default_content()
