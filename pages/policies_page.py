import allure
from playwright.sync_api import Page, TimeoutError

from pages.base_page import BasePage


@allure.severity(allure.severity_level.CRITICAL)
@allure.story("policies page")
class PoliciesPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.start_scan_button = page.get_by_role("button", name="Start new security scan")
        self.reset_data_button = page.locator("button[aria-label='Reset environment']").filter(has_text="Reset data")
        self.reset_confirm_input = page.locator("#reset-confirm-input")
        self.reset_environment_button = page.locator("button[aria-label='Reset environment']").filter(
            has_text="Reset environment")
        self.scan_status_banner = page.get_by_test_id("scan-status-banner")

    @allure.step("Start scan and wait until finished")
    def start_scan_and_wait_until_finished(self):
        self.click(self.start_scan_button)

        try:
            self.scan_status_banner.wait_for(state="visible", timeout=5000)
        except TimeoutError:
            pass

        self.wait_hidden(self.scan_status_banner, timeout=60000)

    @allure.step("Reset environment")
    def reset_environment(self):
        self.click(self.reset_data_button, force=True)
        self.fill(self.reset_confirm_input, "RESET")
        self.wait_enabled(self.reset_environment_button, timeout=30000)
        self.click(self.reset_environment_button)