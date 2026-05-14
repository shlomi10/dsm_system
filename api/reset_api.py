from utils.constants import RESET_ENDPOINT


class ResetApi:
    def __init__(self, api_client):
        self.api_client = api_client

    def reset_environment(self):
        return self.api_client.post(RESET_ENDPOINT, {"confirm": "RESET"})