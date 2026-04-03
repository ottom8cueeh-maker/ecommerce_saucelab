"""End-to-end test for the purchase happy path on the SauceDemo website."""

import logging
import pytest
from playwright.sync_api import expect
from pom.checkout_step_one import CheckoutStepOnePage
from pom.checkout_step_two import CheckoutStepTwoPage
from pom.checkout_complete import CheckoutCompletePage
from pom.inventory import InventoryPage
from pom.login import LoginPage
from pom.shopping_cart import ShoppingCart
from pom.startingpage import StartingPage
from pom.items import add_to_cart, extract_items, ProductName

logger = logging.getLogger(__name__)

@pytest.mark.SMOKE
@pytest.mark.REGRESSION
def test_purchase_happy_path(page, base_url, checkout_data, checkout_complete_data):
    """
    Verify that a user can complete a purchase from login to checkout.

     Steps:
        1. Log in with valid credentials.
        2. Add item(s) to the shopping cart.
        3. Proceed to checkout
        4. Verify checkout information
        5. Complete the purchase.
"""
    # Initialize page objects
    login_page = LoginPage(page)
    starting_page = StartingPage(page)
    inventory_page = InventoryPage(page)
    shopping_cart = ShoppingCart(page)
    checkout_page_one = CheckoutStepOnePage(page)
    checkout_page_two = CheckoutStepTwoPage(page)
    checkout_complete_page = CheckoutCompletePage(page)
    starting_page.goto_url(base_url)

    products_url = f"{base_url}inventory.html"
    checkout_step_one_url = f"{base_url}checkout-step-one.html"
    checkout_step_two_url = f"{base_url}checkout-step-two.html"
    cart_url = f"{base_url}cart.html"

    # ------------------------------- Login page -----------------------------------
    expect(page).to_have_url(base_url)
    expect(login_page.login_button, message="Login button is not visible on the login page").to_be_visible()
    logger.info("Login page: Logging in with valid credentials...")

    # TEST happy path login using credentials from environment variables
    login_page.login(login_page.valid_username1, login_page.valid_password)

    # --------------------------- inventory page -----------------------------------
    expect(page).to_have_url(products_url)
    expect(inventory_page.shopping_cart).to_be_visible()
    logger.info("%s loaded successfully", products_url)

    # Add  item(s) to shopping cart
    items = inventory_page.get_all_inventory_items()
    add_to_cart(items[ProductName.BACKPACK.value])
    add_to_cart(items[ProductName.BIKE_LIGHT.value])
    add_to_cart(items[ProductName.FLEECE_JACKET.value])

    #verify cart icon item count is updated
    expect(shopping_cart.shopping_cart_badge, message="Expected 3 items in cart badge").to_have_text("3")
    logger.info("Verify: 3 item(s) successfully added to shopping cart")

    shopping_cart.click_shopping_cart_icon()

    # -------------------------------------- shopping cart page -----------------------------------
    expect(page).to_have_url(cart_url)
    expect(shopping_cart.continue_shopping_button).to_be_visible()
    logger.info("%scart.html loaded successfully", base_url)

    # grab cart items for comparison later
    cart_items = extract_items(shopping_cart.items)

    shopping_cart.click_checkout_button()
    logger.info("Navigate: Clicking checkout button on shopping cart page ---> checkout step one page...")

    # ------------------------------ checkout step one page -----------------------------------
    expect(page).to_have_url(checkout_step_one_url)
    logger.info("%scheckout-step-one.html loaded successfully", base_url)

    # checkout step one page: enter user information and continue to checkout step two page
    logger.info("Entering user information on checkout step one page...")
    checkout_page_one.enter_info(checkout_data["first_name"], checkout_data["last_name"], checkout_data["zip_code"])

    checkout_page_one.click_continue_button()
    logger.info("Navigate: Clicking continue button on checkout step one page ---> checkout step two page...")

    # ------------------------------ checkout step two page -----------------------------------
    expect(page).to_have_url(checkout_step_two_url)
    expect(checkout_page_two.finish_button).to_be_visible()
    logger.info("%scheckout-step-two.html loaded successfully", base_url)

    # verify payment and shipping information are not empty
    payment_info = checkout_page_two.get_payment_info()
    assert payment_info, "Expected payment information to be displayed, but it is empty"
    logger.info("Verify:  Payment information displayed on checkout step two page: %s", payment_info)

    shipping_info = checkout_page_two.get_shipping_info()
    assert shipping_info, "Expected shipping information to be displayed, but it is empty"
    logger.info("Verify:  Shipping information displayed on checkout step two page: %s", shipping_info)

    # compare selected items on cart page vs check out step two page to ensure they are the same
    checkout_step_two_items = checkout_page_two.get_items()
    assert cart_items == checkout_step_two_items, f"Expected items on checkout step two page to match items on cart page, but they do not match. Cart page items: {cart_items}, checkout step two items: {checkout_step_two_items}"
    logger.info("Verify:  Items on checkout step two page match items on cart page")

    # sum all item prices on checkout step two page and compare against displayed subtotal at the bottom of page
    checkout_step_two_prices_sum = sum(item.price for item in checkout_step_two_items)
    checkout_step_two_item_total = checkout_page_two.get_summary_item_total_price()
    assert checkout_step_two_prices_sum == checkout_step_two_item_total, f"Expected item total ${checkout_step_two_prices_sum:.2f} to match page subtotal ${checkout_step_two_item_total:.2f}"
    logger.info("Verify:  Summing up prices of items matches displayed 'Item total': $%.2f", checkout_step_two_prices_sum)

    checkout_step_two_items_tax = checkout_page_two.get_summary_tax_price()
    logger.info("Verify:  Displayed tax on checkout step two page: $%.2f", checkout_step_two_items_tax)

    # verify price total numbers:  item total + tax = Total
    assert round(checkout_step_two_item_total + checkout_step_two_items_tax, 2) == checkout_page_two.get_summary_total_price(), f"Expected total price to equal item total plus tax, but it does not. Item total: ${checkout_step_two_item_total:.2f}, tax: ${checkout_step_two_items_tax:.2f}, expected total: ${checkout_step_two_item_total + checkout_step_two_items_tax:.2f}, displayed total: ${checkout_page_two.get_summary_total_price():.2f}"

    logger.info("Expected total price (item total + tax): $%.2f", checkout_step_two_item_total + checkout_step_two_items_tax)
    logger.info("Verify:  Displayed total price (bottom of the page): $%.2f", checkout_page_two.get_summary_total_price())

    # click finish button to complete purchase
    checkout_page_two.click_finish_button()
    logger.info("Navigate: Clicking finish button ---> checkout complete page")

    # --------------------------- checkout complete page -----------------------------------
    expect(page).to_have_url(f"{base_url}checkout-complete.html")
    expect(checkout_complete_page.back_home_button).to_be_visible()
    logger.info("%scheckout-complete.html loaded successfully", base_url)

    # verify checkout complete!
    checkout_status = checkout_complete_page.get_checkout_status()
    assert checkout_status == checkout_complete_data["complete_status"], f"Expected: '{checkout_complete_data['complete_status']}', but it is not"
    logger.info("Verify:  Checkout status displayed on checkout complete page: %s", checkout_complete_data['complete_status'])

    # verify complete header and text are displayed
    complete_header = checkout_complete_page.get_complete_header()
    assert complete_header == checkout_complete_data["complete_header"], f"Expected complete header to be {checkout_complete_data['complete_header']}, but it is not"
    logger.info("Verify:  Complete header displayed on checkout complete page: %s", checkout_complete_data['complete_header'])

    complete_text = checkout_complete_page.get_complete_text()
    assert complete_text == checkout_complete_data["complete_message"], f"Expected complete text to be {checkout_complete_data['complete_message']}, but it is not"
    logger.info("Verify:  Complete text displayed on checkout complete page: %s", checkout_complete_data['complete_message'])

    cart_count = shopping_cart.get_cart_items_count()
    assert cart_count == 0, f"Expected no items in cart, but found {cart_count}"
    logger.info("Verify: Total of %d item(s) in the cart after checkout completes", cart_count)

    #click back home button to return to inventory page
    checkout_complete_page.click_back_home_button()

    expect(page).to_have_url(products_url)
    expect(inventory_page.shopping_cart).to_be_visible()
    logger.info("Verify:  Successfully returned to inventory page at URL: %s", products_url)
