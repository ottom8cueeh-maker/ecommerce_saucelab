"""End-to-end test for the purchase happy path on the SauceDemo website."""

import logging
import pytest
from playwright.sync_api import expect
from pom.checkout_step_one import CheckoutStepOnePage
from pom.checkout_step_two import CheckoutStepTwoPage
from pom.checkout_complete import CheckoutCompletePage
from pom.inventory import InventoryPage
from pom.items import ProductName, add_to_cart
from pom.login import LoginPage
from pom.shopping_cart import ShoppingCart
from pom.startingpage import StartingPage

logger = logging.getLogger(__name__)

@pytest.mark.SMOKE
@pytest.mark.FUNCTIONAL
def test_page_navigation_buttons(page, base_url, checkout_data):
    """
    Verify that a user can complete a purchase from login to checkout.

     Steps:
        1. Log in with valid credentials.
        2. Add item(s) to the shopping cart.
        3. Proceed to checkout
        4. Verify checkout information
        5. Complete the purchase.
"""
    login_page = LoginPage(page)
    starting_page = StartingPage(page)
    products_url = f"{base_url}inventory.html"
    checkout_step_one_url = f"{base_url}checkout-step-one.html"
    checkout_step_two_url = f"{base_url}checkout-step-two.html"
    starting_page.goto_url(base_url)

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> buttons to move forward >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    logger.info(">>>>>>>>>>>> Testing navigation buttons that move user forward to next pages... >>>>>>>>>>>>")

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

    # ------- from inventory page ---> cart page -------
    # start - already on inventory page from previous steps
    logger.info(">>> Start:  inventory page...")

    # Add  item(s) to shopping cart
    items = inventory_page.get_all_inventory_items()
    add_to_cart(items[ProductName.BACKPACK.value])
    logger.info("Added '%s' to shopping cart...", ProductName.BACKPACK.value)
    logger.info("Test step: Adding first item to shopping cart...")

    shopping_cart = ShoppingCart(page)

    # Click shopping cart icon
    shopping_cart.click_shopping_cart_icon()

    # wait for cart page to load
    page.wait_for_load_state("domcontentloaded")
    expect(shopping_cart.checkout_button).to_be_visible()
    logger.info("Verify: inventory page ---> Shopping cart page - passed")

    # ------- from shopping cart page ---> checkout step one page -------
    # start - already on cart page from previous steps
    logger.info(">>> Start:  shopping cart page...")

    shopping_cart.click_checkout_button()
    logger.info("Click checkout button...")

    checkout_page_one = CheckoutStepOnePage(page)
    page.wait_for_load_state("domcontentloaded")
    expect(checkout_page_one.continue_button).to_be_visible()
    logger.info("Verify: shopping cart page ---> checkout step one page - passed")

    # ------- from checkout step one page ---> checkout step two page -------
    # start - already on checkout step one page from previous steps
    logger.info(">>> Start:  checkout step one page...")

    # test error messages for missing required fields
    logger.info("Testing error messages for missing required fields on checkout step one page...")
    logger.info("Entering last name and zip code only...")

    # missing first name
    checkout_page_one.enter_info(last_name=checkout_data["last_name"], zip_code=checkout_data["zip_code"])

    checkout_page_one.click_continue_button()
    logger.info("Clicking continue button...")

    # verify clicking continue button has no effect
    assert page.url == checkout_step_one_url, f"Expected URL {checkout_step_one_url}, got {page.url}"
    logger.info("Verify: Clicking continue button with missing first name has no effect - passed")

    logger.info("Entering user information on checkout step one page...")
    checkout_page_one.enter_info(first_name=checkout_data["first_name"], last_name=checkout_data["last_name"], zip_code=checkout_data["zip_code"])

    checkout_page_one.click_continue_button()
    logger.info("Clicking continue button...")

    checkout_page_two = CheckoutStepTwoPage(page)
    page.wait_for_load_state("domcontentloaded")
    expect(checkout_page_two.finish_button).to_be_visible()
    logger.info("Verify: checkout step one page ---> checkout step two page - passed")

    # ------- from checkout step two page ---> checkout complete page -------
    # start - already on checkout step two page from previous steps
    logger.info(">>> Start:  checkout step two page...")

    checkout_page_two = CheckoutStepTwoPage(page)
    page.wait_for_load_state("domcontentloaded")
    expect(checkout_page_two.finish_button).to_be_visible()
    logger.info("%scheckout-step-two.html loaded successfully", base_url)

     # click finish button to complete purchase
    checkout_page_two.click_finish_button()
    logger.info("Clicking finish button...")

    checkout_complete_page = CheckoutCompletePage(page)
    page.wait_for_load_state("domcontentloaded")
    expect(checkout_complete_page.back_home_button).to_be_visible()
    logger.info("Verify: checkout step two page ---> checkout complete page - passed")

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< buttons to move backward <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    logger.info("<<<<<<<<<<<< Testing navigation buttons that move user back to previous pages... <<<<<<<<<<<<")

    # -------from checkout complete page <--- checkout step two page -------
    # start - already on checkout complete page from previous steps
    logger.info("<<< Start:  checkout complete page...")
    # click back home button
    checkout_complete_page.click_back_home_button()

    # verify inventory page is loaded
    page.wait_for_load_state("domcontentloaded")
    expect(inventory_page.shopping_cart).to_be_visible()
    logger.info("Verify: Checkout complete page <--- inventory page - passed.")

    # ------- from checkout step two <--- inventory page -------
    # start
    starting_page.goto_url(checkout_step_two_url)
    page.wait_for_load_state("domcontentloaded")
    expect(checkout_page_two.cancel_button).to_be_visible()
    logger.info("<<< Start:  checkout step two page...")

    # click cancel button
    checkout_page_two.click_step2_cancel_button()

    # verify inventory page is loaded
    page.wait_for_load_state("domcontentloaded")
    expect(inventory_page.shopping_cart).to_be_visible()
    logger.info("Verify: Checkout step two page <--- inventory page - passed.")

    # ------- from checkout step one page <--- cart page -------
    # start
    starting_page.goto_url(checkout_step_one_url)
    page.wait_for_load_state("domcontentloaded")
    expect(checkout_page_one.continue_button).to_be_visible()
    logger.info("<<< Start:  checkout step one page...")

    #click cancel button
    checkout_page_one.click_step1_cancel_button()

    # verify cart page is loaded
    page.wait_for_load_state("domcontentloaded")
    expect(shopping_cart.continue_shopping_button).to_be_visible()
    logger.info("Verify: Checkout step one page <--- cart page - passed.")

    # ------- from cart page <--- inventory page -------
    # start - already on cart page from previous steps
    page.wait_for_load_state("domcontentloaded")
    expect(shopping_cart.continue_shopping_button).to_be_visible()
    logger.info("<<< Start: Cart page")

    # click continue shopping button
    shopping_cart.click_continue_shopping_button()

    # verify inventory page is loaded
    page.wait_for_load_state("domcontentloaded")
    expect(inventory_page.shopping_cart).to_be_visible()
    logger.info("Verify: Cart page <--- inventory page - passed.")
