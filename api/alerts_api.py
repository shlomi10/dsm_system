import time

from utils.constants import ALERTS_ENDPOINT, RESOLUTION_COMMENT


class AlertsApi:
    def __init__(self, api_client):
        self.api_client = api_client

    def get_alerts(self):
        response = self.api_client.get(ALERTS_ENDPOINT)
        return response if isinstance(response, list) else response.get("alerts", [])

    def get_alert_id(self, alert: dict):
        return alert.get("id") or alert.get("alertId")

    def normalize_text(self, value) -> str:
        return str(value).replace("_", " ").strip().lower()

    def get_status(self, alert: dict):
        return self.normalize_text(alert.get("status", ""))

    def get_nested_value(self, alert: dict, paths: list[list[str]]):
        for path in paths:
            current = alert

            for key in path:
                if not isinstance(current, dict) or key not in current:
                    current = None
                    break

                current = current[key]

            if current is not None:
                return current

        return None

    def get_auto_remediate(self, alert: dict) -> bool:
        value = self.get_nested_value(
            alert,
            [
                ["autoRemediate"],
                ["auto_remediate"],
                ["remediation", "autoRemediate"],
                ["policySnapshot", "autoRemediate"],
            ],
        )

        if isinstance(value, bool):
            return value

        return self.normalize_text(value) in ["on", "true", "yes", "enabled"]

    def find_auto_remediation_alert(self):
        alerts = self.get_alerts()

        for alert in alerts:
            status = self.get_status(alert)
            auto_remediate = self.get_auto_remediate(alert)

            if status in ["open", "remediation in progress"] and auto_remediate:
                return alert

        raise AssertionError(f"No auto-remediation alert found. Alerts response: {alerts}")

    def wait_until_remediation_completed(self, alert_id: str, timeout: int = 80):
        end_time = time.time() + timeout
        last_status = None
        last_alert = None

        completed_statuses = [
            "awaiting user verification",
            "awaiting customer",
            "remediated waiting for customer",
        ]

        while time.time() < end_time:
            for alert in self.get_alerts():
                if self.get_alert_id(alert) == alert_id:
                    last_alert = alert

                    status = self.get_status(alert)
                    was_remediated = alert.get("wasRemediated")
                    remediation_origin = alert.get("remediationOrigin")

                    if status != last_status:
                        self.api_client.logger.info(
                            f"Alert {alert_id} status={status}, "
                            f"wasRemediated={was_remediated}, "
                            f"remediationOrigin={remediation_origin}"
                        )
                        last_status = status

                    if status in completed_statuses:
                        return alert

                    if was_remediated is True:
                        return alert

            time.sleep(1)

        raise AssertionError(
            f"Auto-remediation was not completed for alert {alert_id}. "
            f"Last alert state: {last_alert}"
        )

    def resolve_alert(self, alert_id: str):
        return self.api_client.patch(
            f"{ALERTS_ENDPOINT}/{alert_id}",
            {"status": "RESOLVED"}
        )

    def add_comment(self, alert_id: str):
        return self.api_client.post(
            f"{ALERTS_ENDPOINT}/{alert_id}/comments",
            {"message": RESOLUTION_COMMENT}
        )

    def alert_identity(self, alert: dict):
        return (
            alert.get("policyId") or alert.get("policy_id") or alert.get("policyName") or alert.get("policy"),
            alert.get("assetId") or alert.get("asset_id") or alert.get("assetName") or alert.get("asset"),
            alert.get("type") or alert.get("violationType") or alert.get("category"),
        )

    def find_identical_alerts(self, original_alert: dict):
        original_id = self.get_alert_id(original_alert)
        original_identity = self.alert_identity(original_alert)

        return [
            alert for alert in self.get_alerts()
            if self.get_alert_id(alert) != original_id
            and self.alert_identity(alert) == original_identity
        ]