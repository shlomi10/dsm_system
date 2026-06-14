import allure
import pytest


@allure.epic("DSPM")
@allure.feature("API Components")
@allure.story("Basic API validation")
@pytest.mark.api
class TestApiComponents:

    @allure.title("Health endpoint returns healthy status")
    def test_health_check(self, api_setup):
        response = api_setup.health_api.get_health()

        assert response["status"] == "healthy"
        assert response["service"] == "mock-dspm-api"

    @allure.title("Policy config endpoint returns valid response")
    def test_policy_config(self, api_setup):
        response = api_setup.policy_api.get_policy_config()

        assert response is not None
        assert isinstance(response, (dict, list))

    @allure.title("Alerts endpoint returns alerts collection")
    def test_get_alerts(self, api_setup):
        alerts = api_setup.alerts_api.get_alerts()

        assert alerts is not None
        assert isinstance(alerts, list)

    @allure.title("Start scan endpoint returns valid response")
    def test_start_scan(self, api_setup):
        response = api_setup.scans_api.start_scan()

        assert response is None or isinstance(response, dict)

    @allure.title("Reset environment endpoint returns valid response")
    def test_reset_environment(self, api_setup):
        response = api_setup.reset_api.reset_environment()

        assert response is None or isinstance(response, dict)
