"""Page Object Model for the SauceDemo checkout step one page."""
import logging
from playwright.sync_api import Page
from pom.menu import Menu_Items

logger = logging.getLogger(__name__)

class CheckoutStepOnePage:
    """Encapsulates interactions with the checkout step one (customer info) page."""

    def __init__(self, page: Page):
        """Initialise the page object and set up locators for all form elements."""
        self.page = page
        self.menu = Menu_Items(page)
        self.first_name_input = self.page.locator("#first-name")
        self.last_name_input = self.page.locator("#last-name")
        self.postal_code_input = self.page.locator("#postal-code")
        self.continue_button = self.page.locator("#continue")
        self.cancel_button = self.page.locator("#cancel")

    def enter_first_name(self, first_name: str):
        """Fill the first name input field with the given value."""
        self.first_name_input.fill(first_name)

    def enter_last_name(self, last_name: str):
        """Fill the last name input field with the given value."""
        self.last_name_input.fill(last_name)

    def enter_postal_code(self, postal_code: str):
        """Fill the postal/zip code input field with the given value."""
        self.postal_code_input.fill(postal_code)

    def click_continue_button(self):
        """Click the Continue button to advance to checkout step two."""
        self.continue_button.click()

    def click_cancel_button(self):
        """Click the Cancel button to return to the shopping cart."""
        self.cancel_button.click()
        