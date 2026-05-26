import allure
import pytest


@allure.epic("DSPM")
@allure.feature("Alert Lifecycle")
@allure.story("Auto Remediation Rescan Verification")
@pytest.mark.api
class TestAutoRemediationRescan:

    @allure.title("Auto remediation should not recreate identical alert after rescan")
    @pytest.mark.xfail(
        reason="Assignment expects identical alert to be recreated after rescan",
        strict=True
    )
    def test_auto_remediation_rescan_verification(self, api_setup):
        api_setup.scans_api.start_scan()
        api_setup.scans_api.wait_until_scan_finished()

        alert = api_setup.alerts_api.find_auto_remediation_alert()
        alert_id = api_setup.alerts_api.get_alert_id(alert)

        api_setup.alerts_api.wait_until_remediation_completed(alert_id)
        api_setup.alerts_api.resolve_alert(alert_id)
        api_setup.alerts_api.add_comment(alert_id)

        api_setup.scans_api.start_scan()
        api_setup.scans_api.wait_until_scan_finished()

        identical_alerts = api_setup.alerts_api.find_identical_alerts(alert)

        assert len(identical_alerts) == 0
