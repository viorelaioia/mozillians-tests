# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pypom import Region
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected

from pages.base import Base


class EditGroupPage(Base):
    _description_button_locator = (By.ID, 'description-tab')
    _description_tab_locator = (By.ID, 'description')
    _access_button_locator = (By.ID, 'access-tab')
    _access_tab_locator = (By.ID, 'access')
    _invitations_button_locator = (By.ID, 'invitations-tab')
    _invitations_tab_locator = (By.ID, 'invitations')

    def wait_for_page_to_load(self):
        self.wait.until(lambda s: self.is_element_displayed(*self._description_button_locator))
        return self

    @property
    def description(self):
        self.find_element(*self._description_button_locator).click()
        return self.DescriptionTab(self, self.find_element(*self._description_tab_locator))

    @property
    def access(self):
        self.find_element(*self._access_button_locator).click()
        return self.AccessTab(self, self.find_element(*self._access_tab_locator))

    @property
    def invitations(self):
        self.wait.until(expected.visibility_of_element_located(
            self._invitations_button_locator)).click()
        return self.InvitationsTab(self, self.find_element(*self._invitations_tab_locator))

    class DescriptionTab(Region):
        _description_form_locator = (By.ID, 'description-form')
        _delete_panel_locator = (By.CSS_SELECTOR, '.panel-danger')

        @property
        def description_info(self):
            return self.DescriptionForm(self.page, self.find_element(*self._description_form_locator))

        @property
        def delete_group(self):
            return self.DeletePanel(self.page, self.find_element(*self._delete_panel_locator))

        class DescriptionForm(Region):
            _description_locator = (By.ID, 'id_description')
            _irc_channel_locator = (By.ID, 'id_irc_channel')
            _update_locator = (By.ID, 'form-submit-description')

            def set_description(self, description_text):
                element = self.find_element(*self._description_locator)
                element.clear()
                element.send_keys(description_text)

            def set_irc_channel(self, irc_channel):
                element = self.find_element(*self._irc_channel_locator)
                element.clear()
                element.send_keys(irc_channel)

            def click_update(self):
                el = self.find_element(*self._update_locator)
                el.click()
                self.wait.until(expected.staleness_of(el))
                self.wait.until(expected.presence_of_element_located(
                    self._update_locator))

        class DeletePanel(Region):
            _delete_acknowledgement_locator = (By.ID, 'delete-checkbox')
            _delete_group_button_locator = (By.ID, 'delete-group')

            def check_acknowledgement(self):
                self.find_element(*self._delete_acknowledgement_locator).click()

            @property
            def is_delete_button_enabled(self):
                return 'disabled' not in self.find_element(*self._delete_group_button_locator).get_attribute('class')

            def click_delete_group(self):
                self.find_element(*self._delete_group_button_locator).click()
                from pages.groups_page import GroupsPage
                return GroupsPage(self.page.selenium, self.page.base_url)

    class AccessTab(Region):
        _group_type_form_locator = (By.ID, 'grouptype-form')
        _curators_form_locator = (By.ID, 'curators-form')
        _access_type_form_locator = (By.ID, 'access-form')

        @property
        def group_type(self):
            return self.GroupTypeForm(self.page, self.find_element(*self._group_type_form_locator))

        @property
        def curators_form(self):
            return self.CuratorsForm(self.page, self.find_element(*self._curators_form_locator))

        @property
        def access_form(self):
            return self.AccessForm(self.page, self.find_element(*self._access_type_form_locator))

        class GroupTypeForm(Region):
            _reviewed_type_locator = (By.ID, 'id_accepting_new_members_1')
            _new_member_criteria_locator = (By.ID, 'id_new_member_criteria_fieldset')
            _group_types_locator = (By.CSS_SELECTOR, '#group_type .form-group label')

            def set_reviewed_group_type(self):
                self.find_element(*self._reviewed_type_locator).click()

            @property
            def is_member_criteria_visible(self):
                return self.find_element(*self._new_member_criteria_locator).is_displayed()

            @property
            def current_group_type(self):
                group_types = self.find_elements(*self._group_types_locator)
                return [item.text for item in group_types if item.find_element(By.CSS_SELECTOR, 'input').is_selected()]

        class CuratorsForm(Region):
            _curators_input_locator = (By.CSS_SELECTOR, '.select2-search__field')
            _curators_list_locators = (By.CSS_SELECTOR, '.select2-selection__choice')
            _curators_results_locators = (By.XPATH, '//*[@id="select2-id_curators-results"]/li')

            @property
            def curators_list(self):
                self.wait.until(expected.visibility_of_element_located(self._curators_results_locators))
                return [item.text for item in self.find_elements(*self._curators_results_locators)]

            def search_for_curator(self, full_name):
                curator = self.find_element(*self._curators_input_locator)
                curator.send_keys(full_name)

        class AccessForm(Region):
            _access_forms_locator = (By.CSS_SELECTOR, '#access_type .form-group label')

            @property
            def selected_access_type(self):
                access_types = self.find_elements(*self._access_forms_locator)
                return [item.text for item in access_types if item.find_element(By.CSS_SELECTOR, 'input').is_selected()]

    class InvitationsTab(Region):
        _invite_form_locator = (By.ID, 'invite-form')
        _invitations_list_form_locator = (By.ID, 'invitations-form')

        @property
        def invitations_list(self):
            return self.InvitationsForm(self.page, self.find_element(*self._invitations_list_form_locator))

        @property
        def invite(self):
            return self.InviteForm(self.page, self.find_element(*self._invite_form_locator))

        class InvitationsForm(Region):
            _invitatation_list_locator = (By.CSS_SELECTOR, '.invitee')

            @property
            def search_invitation_list(self):
                return [self.SearchResult(self.page, el) for el in
                        self.find_elements(*self._invitatation_list_locator)]

            class SearchResult(Region):
                _name_locator = (By.CSS_SELECTOR, '.invitee a:nth-child(2)')

                @property
                def name(self):
                    return self.find_element(*self._name_locator).text

        class InviteForm(Region):
            _invite_search_locator = (By.CSS_SELECTOR, '.select2-search__field')
            _invite_locator = (By.ID, 'form-submit-invite')
            _invites_list_locator = (By.CSS_SELECTOR, '.select2-selection__choice')
            _invites_results_locator = (By.XPATH, '//*[@id="select2-id_invites-results"]/li')

            @property
            def invites_list(self):
                return self.find_elements(*self._invites_list_locator)

            @property
            def invites_results(self):
                self.wait.until(expected.visibility_of_element_located(self._invites_results_locator))
                return [item.text for item in self.find_elements(*self._invites_results_locator)]

            def invite_new_member(self, mozillian):
                search = self.find_element(*self._invite_search_locator)
                search.send_keys(mozillian)
                self.wait.until(expected.visibility_of_element_located((
                    By.XPATH, '//li[contains(text(), "{0}")]'.format(mozillian)))).click()

            def search_for_member(self, mozillian):
                search = self.find_element(*self._invite_search_locator)
                search.send_keys(mozillian)

            def click_invite(self):
                self.find_element(*self._invite_locator).click()
