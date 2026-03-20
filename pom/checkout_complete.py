"""Page Object Model for the SauceDemo checkout complete page."""
import logging
from playwright.sync_api import Page
from pom.menu import Menu_Items

logger = logging.getLogger(__name__)

class CheckoutCompletePage:
    """Encapsulates interactions with the checkout complete confirmation page."""

    def __init__(self, page: Page):
        """Initialise the page object and set up locators for all elements."""
        self.page = page
        self.menu = Menu_Items(page)
        self.complete_header = self.page.locator(".complete-header")
        self.complete_text = self.page.locator(".complete-text")
        self.back_home_button = self.page.locator("#back-to-products")
        self.checkout_status = self.page.locator('[data-test="title"]')

    def get_complete_header(self) -> str:
        """Return the completion header text (e.g. 'Thank you for your order!')."""
        return self.complete_header.inner_text()

    def get_complete_text(self) -> str:
        """Return the body message shown after a successful order."""
        return self.complete_text.inner_text()

    def get_checkout_status(self) -> str:
        """Return the page title/status label (e.g. 'Checkout: Complete!')."""
        return self.checkout_status.inner_text()

    def click_back_home_button(self):
        """Click the 'Back Home' button to return to the inventory page."""
        self.back_home_button.click()