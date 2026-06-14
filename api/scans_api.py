import time


class ScansApi:
    BASE = "/api/scans"

    def __init__(self, api_client):
        self.api_client = api_client

    def start_scan(self):
        return self.api_client.post(self.BASE)

    def get_scans(self):
        response = self.api_client.get(self.BASE)
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