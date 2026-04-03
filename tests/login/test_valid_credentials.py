"""Tests for valid login credentials on the SauceDemo login page."""
import logging
import pytest
from playwright.sync_api import expect
from pom.inventory import InventoryPage
from pom.login import LoginPage
from pom.menu import MenuItems
from pom.startingpage import StartingPage

logger = logging.getLogger(__name__)

@pytest.mark.SMOKE
def test_valid_credentials(page, base_url):
    """
    Verify that a user can log in with valid credentials.

    Steps:
        1. Navigate to the login page.
        2. Enter valid username and password.
        3. Click login.

    Expected:
        - Redirected to the inventory/products page.
        - Inventory list filter sorter is visible.
    """
    # initialize page objects
    login_page = LoginPage(page)
    starting_page = StartingPage(page)
    inventory_page = InventoryPage(page)
    sl_menu = MenuItems(page)

    # Define URLs for verification
    products_url = f"{base_url}inventory.html"

    starting_page.goto_url(base_url)

    expect(page).to_have_url(base_url)
    expect(login_page.login_button, message="Login button is not visible on the login page").to_be_visible()

    # TEST SCENARIO #1: happy path login using credentials from environment variables
    logger.info("Test step: Logging in with valid credentials...")
    login_page.login(login_page.valid_username1, login_page.valid_password)

    # Verify successful login:  landing in inventory page
    expect(page).to_have_url(products_url)
    expect(inventory_page.shopping_cart).to_be_visible()
    logger.info("%s loaded successfully, test passed", products_url)

    sl_menu.open_menu()
    sl_menu.click_logout()
