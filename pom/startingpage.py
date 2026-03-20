"""Page Object Model base class providing common navigation behaviour."""

import logging
from dotenv import load_dotenv
from playwright.sync_api import Page

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

class StartingPage:
    """Base page object that all POM pages inherit shared navigation helpers from."""

    def __init__(self, page: Page):
        """Initialise the page object with the Playwright page instance."""
        self.page = page

    def goto_url(self, url: str | None = None):
        """Navigate the browser to the login page.

        If `url` is not supplied it will fall back to the BASE_URL
        class attribute (useful for CI or different environments).
        """
        target = url or self.base_url
        logger.info("Navigating to %s", target)
        self.page.goto(target)
