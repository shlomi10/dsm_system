class HealthApi:
    BASE = "/api/health"

    def __init__(self, api_client):
        self.api_client = api_client

    def get_health(self):
        return self.api_client.get(self.BASE)
