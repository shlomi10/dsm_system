import allure
import pytest
from pages.policies_page import PoliciesPage
from pathlib import Path
from playwright.sync_api import Page

from pages.login_page import Loginpage
from pages.alerts_page import AlertsPage
from pages.home_page import HomePage
from api.api_client import ApiClient
from utils.constants import API_BASE_URL, LOGIN_ENDPOINT, API_USERNAME, API_PASSWORD

PROJECT_ROOT = Path.cwd()
ARTIFACTS_DIR = PROJECT_ROOT / "reports"
SCREENSHOTS_DIR = ARTIFACTS_DIR / "screenshots"
TRACES_DIR = ARTIFACTS_DIR / "traces"


# Define a class to hold all page objects
class Pages:
    def __init__(self, page: Page):
        self.login_page = Loginpage(page)
        self.home_page = HomePage(page)
        self.alerts_page = AlertsPage(page)
        self.policies_page = PoliciesPage(page)
        self.page = page  # Also provide direct access to the playwright page object


@pytest.fixture(scope="function")
def initialize(request, playwright):
    browser = playwright.chromium.launch(headless=False, args=["--start-maximized"])
    context = browser.new_context(no_viewport=True)
    page = context.new_page()

    # Ensure the window is maximized using JavaScript
    page.evaluate("window.moveTo(0, 0); window.resizeTo(screen.availWidth, screen.availHeight);")

    # Get the actual window size from the browser and adjust viewport
    window_size = page.evaluate("""() => {
            return {width: window.innerWidth, height: window.innerHeight};
        }""")
    page.set_viewport_size(window_size)

    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield page

    # Capture screenshot if test fails
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:  # Checks if test failed
        SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        screenshot_path = SCREENSHOTS_DIR / f"{request.node.name}.png"
        page.screenshot(path=str(screenshot_path), full_page=True)
        with open(screenshot_path, "rb") as image_file:
            allure.attach(image_file.read(), name="screenshot", attachment_type=allure.attachment_type.PNG)

    TRACES_DIR.mkdir(parents=True, exist_ok=True)
    context.tracing.stop(path=str(TRACES_DIR / f"{request.node.name}.zip"))
    page.close()
    context.close()
    browser.close()


@pytest.fixture()
def page_setup(initialize: Page) -> Pages:
    # 'initialize' fixture now provides the playwright 'page' object
    return Pages(initialize)


@pytest.fixture(scope="session")
def api_context(playwright):
    login_context = playwright.request.new_context(base_url=API_BASE_URL)

    login_response = login_context.post(
        LOGIN_ENDPOINT,
        data={
            "username": API_USERNAME,
            "password": API_PASSWORD,
        }
    )

    assert login_response.status == 200

    token = login_response.json()["token"]

    context = playwright.request.new_context(
        base_url=API_BASE_URL,
        extra_http_headers={
            "Authorization": f"Bearer {token}"
        }
    )

    yield context

    context.dispose()
    login_context.dispose()


@pytest.fixture()
def api_client(api_context):
    return ApiClient(api_context)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

    if rep.when != "call" or rep.passed:
        return

    page_setup = item.funcargs.get("page_setup")
    if page_setup is None:
        return

    png = page_setup.page.screenshot(full_page=True)
    allure.attach(
        png,
        name=f"{item.name}-failure",
        attachment_type=allure.attachment_type.PNG
    )
