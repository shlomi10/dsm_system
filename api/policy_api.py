class PolicyApi:
    BASE = "/api/policy-config"

    def __init__(self, api_client):
        self.api_client = api_client

    def get_policy_config(self):
        return self.api_client.get(self.BASE)
