"""Page Object Model for the SauceDemo hamburger navigation menu."""
import logging

from playwright.sync_api import Page

logger = logging.getLogger(__name__)


class MenuItems:
    """Encapsulates interactions with the slide-out navigation menu."""

    def __init__(self, page: Page):
        """Initialise the menu object and set up locators for all menu elements."""
        self.page = page
        self.menu_button = self.page.locator("#react-burger-menu-btn")
        self.logout = self.page.locator("#logout_sidebar_link")
        self.all_items = self.page.locator("#inventory_sidebar_link")
        self.menu_close = self.page.locator("#react-burger-cross-btn")
        self.reset_app_state = self.page.locator("#reset_sidebar_link")

    def open_menu(self):
        """Click the hamburger button to open the navigation menu."""
        self.menu_button.click()
        logger.info("Clicking menu button ---> menu sidebar should be visible")

    def close_menu(self):
        """Click the X button to close the navigation menu."""
        self.menu_close.click()
        logger.info("Clicking menu close button ---> menu sidebar should be closed")

    def click_logout(self):
        """Click the Logout link to sign out of the application."""
        self.logout.click()
        logger.info("Clicking 'Logout' menu item ---> should navigate to login page")

    def click_all_items(self):
        """Click the All Items link to navigate to the inventory page."""
        self.all_items.click()
        logger.info("Clicking 'All Items' menu item ---> should navigate to inventory page")

    def click_reset_app_state(self):
        """Click the Reset App State link to clear the cart and reset the session."""
        self.reset_app_state.click()
        logger.info("Clicking 'Reset App State' menu item ---> should reset the app state (e.g. clear cart contents)")
