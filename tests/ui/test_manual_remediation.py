import allure
import pytest

from utils.constants import BASE_URL
from utils.logger import get_logger


@allure.epic("DSPM")
@allure.feature("Alert Lifecycle")
@allure.story("Manual Remediation")
@pytest.mark.ui
class TestManualRemediation:
    logger = get_logger(__name__)

    @allure.title("Manual remediation flow resolves an open alert")
    @pytest.mark.flaky(reruns=1)
    def test_manual_remediation_flow(self, page_setup):
        with allure.step("Run manual remediation flow"):
            self.logger.info("Starting manual remediation test")

            page_setup.page.goto(BASE_URL)
            page_setup.login_page.enter_user_name_and_password()
            page_setup.login_page.click_login()

            try:
                self.logger.info("Starting scan from Policies page")
                page_setup.home_page.select_the_policies_tab()
                page_setup.policies_page.start_scan_and_wait_until_finished()

                self.logger.info("Opening Alerts page")
                page_setup.home_page.select_the_alerts_tab()

                self.logger.info("Running manual remediation flow")
                page_setup.alerts_page.complete_manual_remediation_flow()

                self.logger.info("Manual remediation test completed successfully")

            finally:
                self.logger.info("Resetting environment")
                page_setup.home_page.select_the_policies_tab()
                page_setup.policies_page.reset_environment()
