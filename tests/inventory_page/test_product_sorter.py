"""Tests for the product sorting functionality on the SauceDemo inventory page."""
import logging
from playwright.sync_api import expect
import pytest
from pom.inventory import InventoryPage
from pom.items import get_item_prices
from pom.startingpage import StartingPage
from pom.login import LoginPage

logger = logging.getLogger(__name__)

@pytest.mark.FUNCTIONAL
def test_product_sorter(page, base_url):
    """
    Verify that the product sorting functionality on the inventory page works correctly.

    Steps:
        1. Log in with valid credentials.
        2. Sort products by price (low to high) and verify the order is correct.
        3. Sort products by price (high to low) and verify the order is correct.
        4. Sort products by name (A to Z) and verify the order is correct.
        5. Sort products by name (Z to A) and verify the order is correct.
    """
    # Initialize page objects
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    # Define URLs for verification
    products_url = f"{base_url}inventory.html"

    starting_page = StartingPage(page)
    starting_page.goto_url(base_url)

    # ------------------------------- Login page -----------------------------------
    expect(page).to_have_url(base_url)
    expect(login_page.login_button, message="Login button is not visible on the login page").to_be_visible()
    logger.info("Login page: Logging in with valid credentials...")

    # TEST happy path login using credentials from environment variables
    logger.info("Logging in with valid credentials...")
    login_page.login(login_page.valid_username1, login_page.valid_password)

     # --------------------------- inventory page -----------------------------------
    # wait for inventory page to load
    expect(page).to_have_url(products_url)
    expect(inventory_page.shopping_cart).to_be_visible()
    logger.info("%s loaded successfully", products_url)

    # sort prices low to high and verify
    inventory_page.sort_items("lohi" )
    logger.info("Sorting products by price (low to high)...")
    items = inventory_page.get_all_inventory_items()
    prices = get_item_prices(items.values())
    assert prices == sorted(prices), "Products are not sorted by price (low to high)"
    logger.info("Verified products are sorted by price (low to high)")

    # sort prices high to low and verify
    inventory_page.sort_items("hilo")
    logger.info("Sorting products by price (high to low)...")
    items = inventory_page.get_all_inventory_items()
    prices = get_item_prices(items.values())
    assert prices == sorted(prices, reverse=True), "Products are not sorted by price (high to low)"
    logger.info("Verified products are sorted by price (high to low)")

    # sort names A to Z and verify
    inventory_page.sort_items("az")
    logger.info("Sorting products by name (A to Z)...")
    items = inventory_page.get_all_inventory_items()
    names = [item.name for item in items.values()]
    assert names == sorted(names), "Products are not sorted by name (A to Z)"
    logger.info("Verified products are sorted by name (A to Z)")

    # sort names Z to A and verify
    inventory_page.sort_items("za")
    logger.info("Sorting products by name (Z to A)...")
    items = inventory_page.get_all_inventory_items()
    names = [item.name for item in items.values()]
    assert names == sorted(names, reverse=True), "Products are not sorted by name (Z to A)"
    logger.info("Verified products are sorted by name (Z to A)")
