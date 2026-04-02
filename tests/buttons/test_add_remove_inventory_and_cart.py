"""Tests for add-to-cart and remove-from-cart button behaviour on the inventory and cart pages."""
import logging
import pytest
from playwright.sync_api import expect
from pom.inventory import InventoryPage
from pom.items import ProductName, add_to_cart, remove_from_cart
from pom.login import LoginPage
from pom.shopping_cart import ShoppingCart
from pom.startingpage import StartingPage

logger = logging.getLogger(__name__)

@pytest.mark.SMOKE
@pytest.mark.FUNCTIONAL
def test_add_remove_buttons(page, base_url):
    """
    Verify that items can be added to and removed from the cart on both the inventory and cart pages.

    Steps:
        1. Log in with valid credentials.
        2. Add all six items to the cart from the inventory page.
        3. Remove two items from the cart on the inventory page and verify the cart count.
        4. Navigate to the shopping cart page.
        5. Remove two more items from the cart on the cart page and verify the cart count.
    """
    login_page = LoginPage(page)
    starting_page = StartingPage(page)
    products_url = f"{base_url}inventory.html"
    starting_page.goto_url(base_url)

     # ------------------------------- Login page -----------------------------------
    page.wait_for_url(base_url)
    assert page.url == base_url, f"Expected URL {base_url}, got {page.url}"
    logger.info("%s loaded successfully", base_url)

    # TEST happy path login using credentials from environment variables
    logger.info("Logging in with valid credentials...")
    login_page.login(login_page.valid_username1, login_page.valid_password)

    # --------------------------- inventory page -----------------------------------
    # wait for inventory page to load
    page.wait_for_url(products_url)
    inventory_page = InventoryPage(page)
    page.wait_for_load_state("domcontentloaded")
    expect(inventory_page.shopping_cart).to_be_visible()
    assert page.url == products_url, f"Expected URL {products_url}, got {page.url}"
    logger.info("%s loaded successfully", products_url)

    # inventory page: Add  item(s) to shopping cart
    items = inventory_page.get_all_inventory_items()
    add_to_cart(items[ProductName.BACKPACK.value])
    add_to_cart(items[ProductName.BIKE_LIGHT.value])
    add_to_cart(items[ProductName.BOLT_T_SHIRT.value])
    add_to_cart(items[ProductName.FLEECE_JACKET.value])
    add_to_cart(items[ProductName.ONESIE.value])
    add_to_cart(items[ProductName.ALL_THE_THINGS_T_SHIRT.value])

    logger.info("Inventory page: Added 6 items to shopping cart...")

    # inventory page: verify cart icon item count is updated
    shopping_cart = ShoppingCart(page)
    cart_count = shopping_cart.get_cart_items_count()
    assert cart_count == 6, f"Expected 6 items in cart, but found {cart_count}"
    logger.info("Verify: Total of %d item(s) successfully added to shopping cart", cart_count)

    # inventory page: remove item(s) from shopping cart
    remove_from_cart(items[ProductName.BACKPACK.value])
    remove_from_cart(items[ProductName.BIKE_LIGHT.value])
    remove_from_cart(items[ProductName.ONESIE.value])

    # verify cart icon item count is updated
    shopping_cart = ShoppingCart(page)
    cart_count = shopping_cart.get_cart_items_count()
    assert cart_count == 3, f"Expected 3 items in cart, but found {cart_count}"
    logger.info("Verify: Total of %d item(s) are in the shopping cart", cart_count)

    shopping_cart.click_shopping_cart_icon()

    # -------------------------------------- shopping cart page -----------------------------------
    # wait for page to load
    page.wait_for_load_state("domcontentloaded")
    expect(shopping_cart.continue_shopping_button).to_be_visible()

    assert page.url == f"{base_url}cart.html", f"Expected URL {base_url}cart.html, got {page.url}"
    logger.info("%scart.html loaded successfully", base_url)

    cart = ShoppingCart(page)
    cart_items = cart.get_items()
    cart_item_name = {item.name: item for item in cart_items}

    # remove method #1: remove items from cart.html page
    remove_from_cart(cart_item_name[ProductName.BOLT_T_SHIRT.value])
    remove_from_cart(cart_item_name[ProductName.FLEECE_JACKET.value])

    # grab cart items for comparison later
    cart_count = shopping_cart.get_cart_items_count()
    assert cart_count == 1, f"Expected 1 item in cart, but found {cart_count}"
    logger.info("Verify: Total of %d item(s) are in the shopping cart", cart_count)
