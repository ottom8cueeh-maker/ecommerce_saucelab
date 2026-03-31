"""Tests for the sidebar menu functionality on the SauceDemo website."""
import logging
from playwright.sync_api import expect
import pytest
from pom.inventory import InventoryPage
from pom.items import ProductName, add_to_cart
from pom.login import LoginPage
from pom.menu import MenuItems
from pom.shopping_cart import ShoppingCart
from pom.startingpage import StartingPage

logger = logging.getLogger(__name__)

@pytest.mark.FUNCTIONAL
def test_menu_sidebar(page, base_url, products_url):
    """
    Verify menu items are visible and functional.

    Steps:
        1. Log in with valid credentials.
        2. Click the menu button.
        3. Verify all menu items are visible.
        4. Click each menu item and verify expected behavior.
    Expected:
        - All menu items are visible when menu is opened.
        - Clicking "All Items" navigates to inventory page.
        - Clicking "Logout" logs the user out and navigates to login page.
        - Clicking "Reset App State" resets the app state (e.g. cart contents).
    """
    login_page = LoginPage(page)
    starting_page = StartingPage(page)
    starting_page.goto_url(base_url)
    sl_menu = MenuItems(page)

    # ------------------------------- Login page -----------------------------------
    page.wait_for_url(base_url)
    assert page.url == base_url, f"Expected URL {base_url}, got {page.url}"
    logger.info("%s loaded successfully", base_url)

    # TEST happy path login using credentials from environment variables
    logger.info("Logging in with valid credentials...")
    login_page.enter_username(login_page.valid_username1)
    login_page.enter_password(login_page.valid_password)
    login_page.click_login()
    logger.info("Verify:  Login is successful --> waiting for products page to load")

    # --------------------------- inventory page -----------------------------------
    # wait for page to load
    page.wait_for_url(products_url)
    inventory_page = InventoryPage(page)
    page.wait_for_load_state("domcontentloaded")
    expect(inventory_page.shopping_cart).to_be_visible()

    assert page.url == products_url, f"Expected URL {products_url}, got {page.url}"
    logger.info("%s loaded successfully", products_url)

    # open menu from shopping cart page to verify menu is accessible from there as well; setup to test click 'all items' later
    shopping_cart = ShoppingCart(page)
    shopping_cart.click_shopping_cart_icon()

    # click menu button:  open menu
    sl_menu.open_menu()

    # ---------- test menu open/close & items visibility ----------
    # verify menu items are visible
    expect(sl_menu.logout).to_be_visible()
    expect(sl_menu.all_items).to_be_visible()
    expect(sl_menu.reset_app_state).to_be_visible()
    expect(sl_menu.menu_close).to_be_visible()
    logger.info("Verify: All menu items are visible when menu is opened")

    # click close menu button:  menu should be closed
    sl_menu.close_menu()

    # reopen menu
    sl_menu.open_menu()

    # ---------- click menu item:  All items ----------
    sl_menu.click_all_items()
    page.wait_for_url(products_url)
    assert page.url == products_url, f"Expected URL {products_url}, got {page.url}"
    logger.info("Verify: Clicking 'All Items' menu item navigates to inventory page")

    # ---------- reset app state ----------
    # inventory page: Add  item(s) to shopping cart
    items = inventory_page.get_all_inventory_items()

    # setup: add item to cart so we can verify it gets cleared by reset app state
    add_to_cart(items[ProductName.BACKPACK.value])
    add_to_cart(items[ProductName.BIKE_LIGHT.value])
    logger.info("Inventory page: added 2 item(s) to shopping cart...")

    # reopen menu from inventory page
    sl_menu.open_menu()
    sl_menu.click_reset_app_state()

    # verify cart is cleared after reset app state
    cart_count = shopping_cart.get_cart_items_count()
    assert cart_count == 0, f"Expected 0 items in cart, but found {cart_count}"
    logger.info("Verify: Cart is empty after resetting app state")

    # ---------- click menu item:  Logout ----------
    # Menu is still open
    sl_menu.click_logout()
    page.wait_for_url(base_url)
    assert page.url == base_url, f"Expected URL {base_url}, got {page.url}"
    logger.info("Verify: Clicking 'Logout' menu item navigates to login page")
