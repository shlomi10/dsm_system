import allure
import pytest

from api.alerts_api import AlertsApi
from api.scans_api import ScansApi
from api.reset_api import ResetApi


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
    def test_auto_remediation_rescan_verification(self, api_client):
        alerts_api = AlertsApi(api_client)
        scans_api = ScansApi(api_client)
        reset_api = ResetApi(api_client)

        try:
            reset_api.reset_environment()

            scans_api.start_scan()
            scans_api.wait_until_scan_finished()

            alert = alerts_api.find_auto_remediation_alert()
            alert_id = alerts_api.get_alert_id(alert)

            alerts_api.wait_until_remediation_completed(alert_id)
            alerts_api.resolve_alert(alert_id)
            alerts_api.add_comment(alert_id)

            scans_api.start_scan()
            scans_api.wait_until_scan_finished()

            identical_alerts = alerts_api.find_identical_alerts(alert)

            assert len(identical_alerts) == 0

        finally:
            reset_api.reset_environment()