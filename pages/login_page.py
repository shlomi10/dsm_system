import allure
from playwright.sync_api import expect, Page

from pages.base_page import BasePage
from utils.constants import API_USERNAME, API_PASSWORD

"""
This file contains the login page
"""

@allure.severity(allure.severity_level.CRITICAL)
@allure.story("Login page")
class Loginpage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username = page.locator("#username")
        self.password = page.locator("#password")
        self.submit_btn = page.get_by_role("button", name="Sign in")

    @allure.step("type username and password")
    def enter_user_name_and_password(self) -> None:
        expect(self.submit_btn).to_be_visible(timeout=5000)
        self.fill(self.username, API_USERNAME)
        self.fill(self.password, API_PASSWORD)

    @allure.step("click login")
    def click_login(self) -> None:
        self.click(self.submit_btn)
