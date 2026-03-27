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
    login_page = LoginPage(page)
    products_url = f"{base_url}inventory.html"
    starting_page = StartingPage(page)
    starting_page.goto_url(base_url)

     # ------------------------------- Login page -----------------------------------
    page.wait_for_url(base_url)
    assert page.url == base_url, f"Expected URL {base_url}, got {page.url}"
    logger.info("%s loaded successfully", base_url)

    # TEST happy path login using credentials from environment variables
    logger.info("Logging in with valid credentials...")
    login_page.enter_username(login_page.valid_username1)
    login_page.enter_password(login_page.valid_password)
    login_page.click_login()
    logger.info("Login is successful --> waiting for products page to load")

     # --------------------------- inventory page -----------------------------------
    # wait for inventory page to load
    page.wait_for_url(products_url)
    inventory_page = InventoryPage(page)
    page.wait_for_load_state("domcontentloaded")
    expect(inventory_page.shopping_cart).to_be_visible()
    assert page.url == products_url, f"Expected URL {products_url}, got {page.url}"
    logger.info("%s loaded successfully", products_url)

    # click on item name
    page.get_by_text(ProductName.BACKPACK.value).click()
    inventory_item_page = InventoryItemPage(page)
    inventory_item_page.add_to_cart_button.click()
    logger.info("Added item to cart from inventory item details page")

    shopping_cart = ShoppingCart(page)
    cart_count = shopping_cart.get_cart_items_count()
    assert cart_count == 1, f"Expected 1 item in cart, but found {cart_count}"
    logger.info("Verify: Total of %d item(s) are in the shopping cart", cart_count)

    inventory_item_page.back_to_products_button.click()

    page.get_by_text(ProductName.BIKE_LIGHT.value).click()
    inventory_item_page.add_to_cart_button.click()
    logger.info("Inventory-item page: Added item to cart from inventory item details page")

    cart_count = shopping_cart.get_cart_items_count()
    assert cart_count == 2, f"Expected 2 items in cart, but found {cart_count}"
    logger.info("Verify: Total of %d item(s) are in the shopping cart", cart_count)

    inventory_item_page.back_to_products_button.click()

    page.get_by_text(ProductName.BACKPACK.value).click()
    inventory_item_page.remove_from_cart_button.click()
    logger.info("Inventory-item page: Removed item from cart from inventory item details page")

    cart_count = shopping_cart.get_cart_items_count()
    assert cart_count == 1, f"Expected 1 item in cart, but found {cart_count}"
    logger.info("Verify: Total of %d item(s) are in the shopping cart", cart_count)
