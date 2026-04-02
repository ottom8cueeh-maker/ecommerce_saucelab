"""Tests for valid login credentials on the SauceDemo login page."""
import logging
import pytest
from pom.inventory import InventoryPage
from pom.login import LoginPage
from pom.menu import MenuItems
from pom.startingpage import StartingPage

logger = logging.getLogger(__name__)

@pytest.mark.SMOKE
def test_valid_credentials(page, base_url, products_url):
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
    login_page = LoginPage(page)
    starting_page = StartingPage(page)
    starting_page.goto_url(base_url)
    sl_menu = MenuItems(page)

    page.wait_for_url(base_url)
    assert page.url == base_url, f"Expected URL {base_url}, got {page.url}"
    logger.info("%s loaded successfully", base_url)

    # TEST SCENARIO #1: happy path login using credentials from environment variables
    logger.info("Test step: Logging in with valid credentials...")
    login_page.login(login_page.valid_username1, login_page.valid_password)

    # Verify successful login:  landing in inventory page
    page.wait_for_url(products_url)
    assert page.url == products_url, f"Expected URL {products_url}, got {page.url}"
    logger.info("%s loaded successfully", products_url)

    inventory_page = InventoryPage(page)
    assert inventory_page.items_filter_sorter.is_visible(), "Item filter sorter is not visible"
    logger.info("Result: Item filter sorter is visible, test passed")

    sl_menu.open_menu()
    sl_menu.click_logout()
