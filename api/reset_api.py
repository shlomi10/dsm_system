class ResetApi:
    BASE = "/api/admin/reset"

    def __init__(self, api_client):
        self.api_client = api_client

    def reset_environment(self):
        return self.api_client.post(self.BASE, {"confirm": "RESET"})