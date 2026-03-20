"""Page Object Model for the SauceDemo login page."""

import os
import logging
from dotenv import load_dotenv
from playwright.sync_api import Page

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

class LoginPage:
    """Encapsulates interactions with the SauceDemo login page."""

    # Class attributes for credentials and base URL
    valid_username1 = os.getenv('TEST_VALID_USERNAME1')
    valid_password = os.getenv('TEST_VALID_PASSWORD')
    bad_username = os.getenv('TEST_BAD_USERNAME')
    bad_password = os.getenv('TEST_BAD_PASSWORD')

    def __init__(self, page: Page):
        """Initialise the LoginPage with locators for all interactive elements."""
        self.page = page
        self.username_input = self.page.locator("#user-name")
        self.password_input = self.page.locator("#password")
        self.login_button = self.page.locator("#login-button")

    def enter_username(self, a_username: str):
        """Type the given username into the username input field."""
        logger.info("Entering username: %s", a_username)
        self.username_input.fill(a_username)

    def enter_password(self, a_password: str):
        """Type the given password into the password input field."""
        logger.info("Entering password: %s", a_password)
        self.password_input.fill(a_password)

    def click_login(self):
        """Click the login button to submit the login form."""
        logger.info("Clicking login button")
        self.login_button.click()
