"""Page Object Model for the SauceDemo checkout step one page."""
import logging
from playwright.sync_api import Page
from pom.menu import MenuItems

logger = logging.getLogger(__name__)

class CheckoutStepOnePage:
    """Encapsulates interactions with the checkout step one (customer info) page."""

    def __init__(self, page: Page):
        """Initialise the page object and set up locators for all form elements."""
        self.page = page
        self.menu = MenuItems(page)
        self.first_name_input = self.page.locator("#first-name")
        self.last_name_input = self.page.locator("#last-name")
        self.zip_code_input = self.page.locator("#postal-code")
        self.continue_button = self.page.locator("#continue")
        self.cancel_button = self.page.locator("#cancel")
        self.error_message = self.page.locator("[data-test='error']")

    def enter_info(self, first_name: str = "", last_name: str = "", zip_code: str = ""):
        """Convenience method to fill all three form fields with the given values."""
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.zip_code_input.fill(zip_code)
        logger.info("Filled checkout step one form fields: first_name='%s', last_name='%s', zip_code='%s'", first_name, last_name, zip_code)

    def click_continue_button(self):
        """Click the Continue button to advance to checkout step two."""
        self.continue_button.click()

    def click_cancel_button(self):
        """Click the Cancel button to return to the shopping cart."""
        self.cancel_button.click()
