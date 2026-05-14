import allure
from playwright.sync_api import Page, Locator

from pages.base_page import BasePage


@allure.severity(allure.severity_level.CRITICAL)
@allure.story("alerts page")
class AlertsPage(BasePage):
    ALERT_TITLE_COLUMN_INDEX = 0
    STATUS_COLUMN_INDEX = 3
    AUTO_REMEDIATE_COLUMN_INDEX = 4

    OPEN_STATUS = "Open"
    IN_PROGRESS_STATUS = "In Progress"
    REMEDIATION_COMPLETE_STATUS = "Awaiting User Verification"
    RESOLVED_STATUS = "Resolved"
    AUTO_REMEDIATE_OFF = "OFF"
    SECURITY_ANALYST = "Security Analyst"
    REMEDIATION_NOTE = "Manual remediation completed by Security Analyst"
    RESOLUTION_COMMENT = "Remediation verified successfully and issue is resolved"

    REMEDIATION_TIMEOUT = 80000
    NOTIFICATION_TIMEOUT = 15000

    def __init__(self, page: Page):
        super().__init__(page)

        self.alerts_table = page.locator("table").first
        self.alert_rows = self.alerts_table.locator("tbody tr")

        self.status_dropdown = page.locator("#alert-status")
        self.assignee_dropdown = page.locator("#alert-assignee")

        self.remediation_section_button = page.get_by_role("button", name="Remediation")
        self.remediation_section = page.locator("#section-remediation")
        self.remediation_notes_input = self.remediation_section.locator("textarea")
        self.remediate_button = self.remediation_section.get_by_role("button", name="Remediate")

        self.comment_textarea = page.get_by_label("Comment message")
        self.post_comment_button = page.get_by_role("button", name="Post comment")

        self.notifications = page.get_by_role("alert")

    def wait_for_alerts_table(self):
        self.wait_visible(self.alerts_table)
        self.wait_visible(self.alert_rows.first)

    def cell(self, row: Locator, index: int) -> Locator:
        return row.locator("td").nth(index)

    def cell_text(self, row: Locator, index: int) -> str:
        return self.get_clean_text(self.cell(row, index))

    def status_text(self, row: Locator) -> str:
        return self.cell_text(row, self.STATUS_COLUMN_INDEX)

    def auto_remediate_text(self, row: Locator) -> str:
        return self.cell_text(row, self.AUTO_REMEDIATE_COLUMN_INDEX)

    def wait_for_notifications_to_disappear(self):
        self.wait_count(self.notifications, 0, timeout=self.NOTIFICATION_TIMEOUT)

    @allure.step("Find first alert with status Open and Auto Remediate OFF")
    def find_manual_remediation_alert_row(self) -> Locator:
        self.wait_for_alerts_table()

        for index in range(self.alert_rows.count()):
            row = self.alert_rows.nth(index)

            if (
                self.status_text(row).lower() == self.OPEN_STATUS.lower()
                and self.auto_remediate_text(row).lower() == self.AUTO_REMEDIATE_OFF.lower()
            ):
                return row

        raise AssertionError("No alert found with status Open and Auto Remediate OFF")

    @allure.step("Open first manual remediation alert")
    def open_manual_remediation_alert(self):
        row = self.find_manual_remediation_alert_row()
        self.click(self.cell(row, self.ALERT_TITLE_COLUMN_INDEX), force=True)

    @allure.step("Change alert status to In Progress")
    def change_status_to_in_progress(self):
        self.select_dropdown_option(self.status_dropdown, self.IN_PROGRESS_STATUS)
        self.wait_text(self.status_dropdown, self.IN_PROGRESS_STATUS)
        self.wait_for_notifications_to_disappear()

    @allure.step("Assign alert to Security Analyst")
    def assign_to_security_analyst(self):
        self.select_dropdown_option(self.assignee_dropdown, self.SECURITY_ANALYST)
        self.wait_text(self.assignee_dropdown, self.SECURITY_ANALYST)
        self.wait_for_notifications_to_disappear()

    @allure.step("Open remediation section")
    def open_remediation_section(self):
        if self.remediation_section_button.get_attribute("aria-expanded") != "true":
            self.click(self.remediation_section_button)

        self.wait_visible(self.remediation_section)

    @allure.step("Add remediation notes")
    def add_remediation_notes(self):
        self.open_remediation_section()
        self.fill(self.remediation_notes_input, self.REMEDIATION_NOTE)

    @allure.step("Click Remediate")
    def click_remediate(self):
        self.click(self.remediate_button)
        self.wait_for_notifications_to_disappear()

    @allure.step("Wait until remediation is complete")
    def wait_until_remediation_complete(self):
        self.wait_visible(self.status_dropdown, timeout=self.REMEDIATION_TIMEOUT)
        self.wait_text(
            self.status_dropdown,
            self.REMEDIATION_COMPLETE_STATUS,
            timeout=self.REMEDIATION_TIMEOUT
        )

    @allure.step("Change alert status to Resolved")
    def change_status_to_resolved(self):
        self.wait_until_remediation_complete()
        self.select_dropdown_option(self.status_dropdown, self.RESOLVED_STATUS)
        self.wait_text(self.status_dropdown, self.RESOLVED_STATUS)
        self.wait_for_notifications_to_disappear()

    @allure.step("Add resolved comment")
    def add_resolved_comment(self):
        self.fill(self.comment_textarea, self.RESOLUTION_COMMENT)
        self.click(self.post_comment_button)
        self.wait_for_notifications_to_disappear()

    @allure.step("Close alert details panel")
    def close_alert_details_panel(self):
        self.click_screen_center()

    @allure.step("Complete manual remediation flow")
    def complete_manual_remediation_flow(self):
        self.logger.info("Searching for first alert with Open status and Auto Remediate OFF")
        self.open_manual_remediation_alert()
        self.change_status_to_in_progress()
        self.assign_to_security_analyst()
        self.add_remediation_notes()
        self.click_remediate()
        self.change_status_to_resolved()
        self.add_resolved_comment()
        self.close_alert_details_panel()