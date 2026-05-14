import allure
import pytest

from utils.constants import (
    HEALTH_ENDPOINT,
    POLICY_CONFIG_ENDPOINT,
    ALERTS_ENDPOINT,
    SCANS_ENDPOINT,
    RESET_ENDPOINT,
)


@allure.epic("DSPM")
@allure.feature("API Components")
@allure.story("Basic API validation")
@pytest.mark.api
class TestApiComponents:

    @allure.title("Health endpoint returns healthy status")
    def test_health_check(self, api_client):
        response = api_client.get(HEALTH_ENDPOINT)

        assert response["status"] == "healthy"
        assert response["service"] == "mock-dspm-api"

    @allure.title("Policy config endpoint returns valid response")
    def test_policy_config(self, api_client):
        response = api_client.get(POLICY_CONFIG_ENDPOINT)

        assert response is not None
        assert isinstance(response, (dict, list))

    @allure.title("Alerts endpoint returns alerts collection")
    def test_get_alerts(self, api_client):
        response = api_client.get(ALERTS_ENDPOINT)

        assert response is not None
        assert isinstance(response, (dict, list))

    @allure.title("Start scan endpoint returns valid response")
    def test_start_scan(self, api_client):
        response = api_client.post(SCANS_ENDPOINT)

        assert response is None or isinstance(response, dict)

    @allure.title("Reset environment endpoint returns valid response")
    def test_reset_environment(self, api_client):
        response = api_client.post(RESET_ENDPOINT, {"confirm": "RESET"})

        assert response is None or isinstance(response, dict)