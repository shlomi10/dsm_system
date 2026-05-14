import time

from utils.constants import SCANS_ENDPOINT


class ScansApi:
    def __init__(self, api_client):
        self.api_client = api_client

    def start_scan(self):
        return self.api_client.post(SCANS_ENDPOINT)

    def get_scans(self):
        response = self.api_client.get(SCANS_ENDPOINT)
        return response if isinstance(response, list) else response.get("scans", [])

    def wait_until_scan_finished(self, timeout: int = 60):
        end_time = time.time() + timeout

        while time.time() < end_time:
            scans = self.get_scans()

            if scans:
                latest_scan = scans[0]
                status = str(latest_scan.get("status", "")).lower()

                if status in ["completed", "finished", "done", "success"]:
                    return latest_scan

            time.sleep(1)

        raise AssertionError("Scan did not finish")