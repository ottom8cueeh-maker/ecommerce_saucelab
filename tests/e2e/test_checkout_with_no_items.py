"""End-to-end test verifying checkout cannot be initiated with an empty cart on the SauceDemo website."""

import logging
import pytest
from playwright.sync_api import expect
from pom.inventory import InventoryPage
from pom.login import LoginPage
from pom.shopping_cart import ShoppingCart
from pom.startingpage import StartingPage

logger = logging.getLogger(__name__)

@pytest.mark.SMOKE
@pytest.mark.xfail(reason="Click checkout button with cart empty: goes to checkout step one page instead of remaining on cart page, with error displayed")
def test_checkout_with_no_items(page, base_url):
    """
    Verify that a user cannot proceed to checkout when the shopping cart is empty.

    Steps:
        1. Log in with valid credentials.
        2. Navigate to the inventory page.
        3. Verify the shopping cart is empty (0 items).
        4. Navigate to the shopping cart page.
        5. Attempt to click the checkout button with no items in the cart.
        6. Verify the user remains on the cart page and is not advanced to checkout step one.
    """
    # Initialize page objects
    login_page = LoginPage(page)
    starting_page = StartingPage(page)
    shopping_cart = ShoppingCart(page)
    inventory_page = InventoryPage(page)

    products_url = f"{base_url}inventory.html"
    cart_url = f"{base_url}cart.html"

    starting_page.goto_url(base_url)
    # ------------------------------- Login page -----------------------------------
    page.wait_for_url(base_url)
    assert page.url == base_url, f"Expected URL {base_url}, got {page.url}"
    logger.info("%s loaded successfully", base_url)

    # TEST happy path login using credentials from environment variables
    logger.info("Logging in with valid credentials...")
    login_page.login(login_page.valid_username1, login_page.valid_password)
    logger.info("Verify:  Login is successful --> waiting for products page to load")

    # --------------------------- inventory page -----------------------------------
    # wait for page to load
    expect(page).to_have_url(products_url)
    expect(inventory_page.shopping_cart).to_be_visible()
    logger.info("%s loaded successfully", products_url)

    #verify cart icon item count is updated
    expect(shopping_cart.shopping_cart_badge, message="Expected 0 items in cart badge").to_have_text("0")
    logger.info("Verify: 0 item(s) successfully added to shopping cart")

    shopping_cart.click_shopping_cart_icon()

    # -------------------------------------- shopping cart page -----------------------------------
    # wait for page to load
    expect(page).to_have_url(cart_url)
    expect(shopping_cart.continue_shopping_button).to_be_visible()
    logger.info("%scart.html loaded successfully", base_url)

    shopping_cart.click_checkout_button()
    logger.info("Navigate: Clicking checkout button on shopping cart page with NO ITEMS...should NOT advance to checkout step one page...")
    expect(page, message=f"Expected to stay on cart page but navigated away to: {page.url}").to_have_url(cart_url)
    logger.info("Verify: User is NOT advanced to checkout step one page with empty cart - PASSED")
