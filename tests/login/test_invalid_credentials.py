"""Tests for invalid login credentials on the SauceDemo login page."""
import logging
import pytest
from playwright.sync_api import expect
from pom.login import LoginPage
from pom.startingpage import StartingPage

logger = logging.getLogger(__name__)

@pytest.mark.SMOKE
def test_invalid_credentials(page, base_url):
    """
    Verify invalid credentials are rejected.

    Steps:
        1. Navigate to the login page.
        2. Enter invalid username and password.
        3. Click login.

    Expected:
        - Remains on the login page.
        - Error message is displayed.
        - Inventory list is not visible.
    """
    # Initialize page objects
    login_page = LoginPage(page)
    starting_page = StartingPage(page)

    starting_page.goto_url(base_url)

    expect(page).to_have_url(base_url)
    logger.info("%s loaded successfully", base_url)

    # TEST SCENARIO #2: login using invalid credentials from environment variables
    logger.info("Test step: Logging in with invalid credentials...")
    login_page.login(login_page.bad_username, login_page.bad_password)

    # Verify unsuccessful login:  still on login page
    expect(page).to_have_url(base_url)

    error = page.locator('[data-test="error"]')
    expect(error).to_be_visible()
    expect(error).to_contain_text("Username and password do not match")
    logger.info("Result: 'Username and password do not match' error message is displayed on login page")
