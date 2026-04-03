"""
Tests for adding and removing items from the cart via the inventory item details page.

Covers:
    - Navigating to an individual item's detail page from the inventory.
    - Adding items to the cart and verifying the cart count.
    - Removing items from the cart and verifying the cart count.
"""
import logging
import pytest
from playwright.sync_api import expect
from pom.inventory import InventoryItemPage, InventoryPage
from pom.shopping_cart import ShoppingCart
from pom.startingpage import StartingPage
from pom.login import LoginPage
from pom.items import ProductName

logger = logging.getLogger(__name__)

@pytest.mark.SMOKE
@pytest.mark.FUNCTIONAL
def test_add_remove_inventoryitem(page, base_url):
    """
    Verify that an item can be added to and removed from the cart on the inventory item details page.

    Steps:
        1. Log in with valid credentials.
        2. Click on the first inventory item to navigate to its details page.
        3. Add the item to the cart and verify the cart count updates.
        4. Remove the item from the cart and verify the cart count updates.
    """
    # Initialize page objects
    login_page = LoginPage(page)
    starting_page = StartingPage(page)
    inventory_page = InventoryPage(page)
    inventory_item_page = InventoryItemPage(page)
    shopping_cart = ShoppingCart(page)
    
    # Define URLs for verification
    products_url = f"{base_url}inventory.html"

    starting_page.goto_url(base_url)

    # ------------------------------- Login page -----------------------------------
    expect(page).to_have_url(base_url)
    expect(login_page.login_button, message="Login button is not visible on the login page").to_be_visible()
    logger.info("Login page: Logging in with valid credentials...")

    # TEST happy path login using credentials from environment variables
    login_page.login(login_page.valid_username1, login_page.valid_password)

     # --------------------------- inventory page -----------------------------------
    # wait for inventory page to load
    expect(page).to_have_url(products_url)
    expect(inventory_page.shopping_cart).to_be_visible()
    logger.info("%s loaded successfully", products_url)

    # click on item name
    inventory_page.click_item_name(ProductName.BACKPACK.value)
    inventory_item_page.add_to_cart()

    expect(shopping_cart.shopping_cart_badge, message="Expected 1 items in cart badge").to_have_text("1")
    logger.info("Verify: Total of 1 item(s) are in the shopping cart")

    inventory_item_page.back_to_products_button.click()

    inventory_page.click_item_name(ProductName.BIKE_LIGHT.value)
    inventory_item_page.add_to_cart()

    expect(shopping_cart.shopping_cart_badge, message="Expected 2 items in cart badge").to_have_text("2")
    logger.info("Verify: Total of 2 item(s) are in the shopping cart")

    inventory_item_page.back_to_products_button.click()

    inventory_page.click_item_name(ProductName.BACKPACK.value)
    inventory_item_page.remove_from_cart()

    expect(shopping_cart.shopping_cart_badge, message="Expected 1 items in cart badge").to_have_text("1")
    logger.info("Verify: Total of 1 item(s) are in the shopping cart")
