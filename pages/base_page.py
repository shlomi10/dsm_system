from playwright.sync_api import Page, Locator, expect

from utils.logger import get_logger


class BasePage:
    DEFAULT_TIMEOUT = 10000

    def __init__(self, page: Page):
        self.page = page
        self.logger = get_logger(self.__class__.__name__)

    def click(self, element: Locator, timeout: int = DEFAULT_TIMEOUT, force: bool = False):
        try:
            self.logger.info(f"Click element: {element}")
            element.click(timeout=timeout, force=force)
        except Exception as error:
            self.logger.exception(f"Failed to click element: {element}")
            raise error

    def fill(self, element: Locator, text: str, timeout: int = DEFAULT_TIMEOUT):
        try:
            self.logger.info(f"Fill element: {element}")
            expect(element).to_be_visible(timeout=timeout)
            element.fill(text)
        except Exception as error:
            self.logger.exception(f"Failed to fill element: {element}")
            raise error

    def wait_visible(self, element: Locator, timeout: int = DEFAULT_TIMEOUT):
        try:
            self.logger.info(f"Wait visible: {element}")
            expect(element).to_be_visible(timeout=timeout)
        except Exception as error:
            self.logger.exception(f"Element was not visible: {element}")
            raise error

    def wait_hidden(self, element: Locator, timeout: int = DEFAULT_TIMEOUT):
        try:
            self.logger.info(f"Wait hidden: {element}")
            expect(element).to_be_hidden(timeout=timeout)
        except Exception as error:
            self.logger.exception(f"Element was not hidden: {element}")
            raise error

    def wait_enabled(self, element: Locator, timeout: int = DEFAULT_TIMEOUT):
        try:
            self.logger.info(f"Wait enabled: {element}")
            expect(element).to_be_enabled(timeout=timeout)
        except Exception as error:
            self.logger.exception(f"Element was not enabled: {element}")
            raise error

    def wait_text(self, element: Locator, text: str, timeout: int = DEFAULT_TIMEOUT):
        try:
            self.logger.info(f"Wait text '{text}' in element: {element}")
            expect(element).to_contain_text(text, timeout=timeout)
        except Exception as error:
            self.logger.exception(f"Text '{text}' was not found in element: {element}")
            raise error

    def wait_count(self, element: Locator, count: int, timeout: int = DEFAULT_TIMEOUT):
        try:
            self.logger.info(f"Wait count {count}: {element}")
            expect(element).to_have_count(count, timeout=timeout)
        except Exception as error:
            self.logger.exception(f"Element count was not {count}: {element}")
            raise error

    def get_clean_text(self, element: Locator) -> str:
        try:
            text = " ".join(element.inner_text().split())
            self.logger.info(f"Element text: {text}")
            return text
        except Exception as error:
            self.logger.exception(f"Failed to get text from element: {element}")
            raise error

    def select_dropdown_option(self, dropdown: Locator, option: str):
        try:
            self.logger.info(f"Select dropdown option: {option}")
            self.click(dropdown)
            self.click(self.page.get_by_role("option", name=option))
        except Exception as error:
            self.logger.exception(f"Failed to select dropdown option: {option}")
            raise error

    def click_screen_center(self):
        try:
            self.logger.info("Click screen center")
            size = self.page.evaluate("""() => ({
                width: window.innerWidth,
                height: window.innerHeight
            })""")
            self.page.mouse.click(size["width"] / 2, size["height"] / 2)
        except Exception as error:
            self.logger.exception("Failed to click screen center")
            raise error