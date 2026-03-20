"""Tests for the sidebar menu functionality on the SauceDemo website."""
import logging
from playwright.sync_api import expect
from pom.inventory import InventoryPage
from pom.login import LoginPage
from pom.menu import Menu_Items
from pom.shopping_cart import ShoppingCart
from pom.startingpage import StartingPage

logger = logging.getLogger(__name__)

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
    sl_menu = Menu_Items(page)

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
      
    shopping_cart = ShoppingCart(page)
    shopping_cart.click_shopping_cart_icon()
    logger.info("Navigate: Clicking shopping cart icon ---> shopping cart page...")
    
    # click menu button:  open menu
    sl_menu.menu_button.click()
    logger.info("Clicking menu button ---> menu sidebar should be visible")
    
    # verify menu items are visible
    expect(sl_menu.logout).to_be_visible()
    expect(sl_menu.inventory).to_be_visible()
    expect(sl_menu.reset_app_state).to_be_visible()
    expect(sl_menu.menu_close).to_be_visible()
    logger.info("Verify: All menu items are visible when menu is opened")
    
    # click close menu button:  menu should be closed
    sl_menu.menu_close.click()
    logger.info("Clicking menu close button ---> menu sidebar should be closed")    
    
    # reopen menu
    sl_menu.menu_button.click()
    logger.info("Clicking menu button ---> menu sidebar should be visible")
    
    # click inventory menu item
    sl_menu.click_inventory()
    logger.info("Clicking 'Inventory' menu item ---> should navigate to inventory page")
    page.wait_for_url(products_url)
    assert page.url == products_url, f"Expected URL {products_url}, got {page.url}"
    logger.info("Verify: Clicking 'Inventory' menu item navigates to inventory page")
    
    # reopen menu
    sl_menu.menu_button.click()
    logger.info("Clicking menu button ---> menu sidebar should be visible")
    
    # click logout menu item
    sl_menu.click_logout()  
    logger.info("Clicking 'Logout' menu item ---> should navigate to login page")
    page.wait_for_url(base_url)
    assert page.url == base_url, f"Expected URL {base_url}, got {page.url}"
    logger.info("Verify: Clicking 'Logout' menu item navigates to login page")
