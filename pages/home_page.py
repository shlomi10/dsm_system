import allure

from pages.base_page import BasePage

"""
This file contains the homepage
"""


@allure.severity(allure.severity_level.CRITICAL)
@allure.story("Home page")
class HomePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.alerts_tab = page.get_by_role("link", name="Alerts")
        self.policies_tab = page.get_by_role("link", name="Policies")

    @allure.step("select the policies tab")
    def select_the_policies_tab(self) -> None:
        self.click(self.policies_tab)

    @allure.step("select the alerts tab")
    def select_the_alerts_tab(self) -> None:
        self.click(self.alerts_tab)
