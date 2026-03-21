
"""Tests for form validation error messages on the SauceDemo checkout step one page."""
import logging
from dotenv.main import logger
from playwright.sync_api import expect
from pom.login import LoginPage
from pom.checkout_step_one import CheckoutStepOnePage
from pom.startingpage import StartingPage

logger = logging.getLogger(__name__)

def test_checkout_step_one_errors(page, base_url, checkout_step_one_url, checkout_data, checkout_step_1_errors):
    """
    Verify that the correct error messages are displayed when required fields are
    omitted on the checkout step one form.

    Steps:
        1. Navigate to the checkout step one page.
        2. Submit the form with each required field missing in turn.
        3. Verify the appropriate error message is shown for each missing field.
    """
    starting_page = StartingPage(page)
    starting_page.goto_url(base_url)

     # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> buttons to move forward >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    logger.info(">>>>>>>>>>>> Testing navigation buttons that move user forward to next pages... >>>>>>>>>>>>")

    # ------------------------------- Login page -----------------------------------
    page.wait_for_url(base_url)
    assert page.url == base_url, f"Expected URL {base_url}, got {page.url}"
    logger.info("%s loaded successfully", base_url)

    # TEST happy path login using credentials from environment variables
    logger.info("Logging in with valid credentials...")
    login_page = LoginPage(page)
    login_page.enter_username(login_page.valid_username1)
    login_page.enter_password(login_page.valid_password)
    login_page.click_login()
    logger.info("Login is successful --> waiting for products page to load")
    starting_page.goto_url(checkout_step_one_url)

    checkout_page_one = CheckoutStepOnePage(page)
    page.wait_for_load_state("domcontentloaded")
    expect(checkout_page_one.continue_button).to_be_visible()
    logger.info("Verify: shopping cart page ---> checkout step one page - passed")

    # test starts
    # ---------------- missing first name ----------------
    checkout_page_one.enter_info(last_name=checkout_data["last_name"], zip_code=checkout_data["zip_code"])
    logger.info("Entering last name and postal code, leaving first name blank...")

    checkout_page_one.click_continue_button()
    logger.info("Clicking continue button...")

    # verify error message for missing first name
    expect(checkout_page_one.error_message).to_have_text(checkout_step_1_errors["first_name"])
    logger.info("Verify: Error message for missing first name - passed")

    # ---------------- missing last name ----------------
    checkout_page_one.enter_info(first_name=checkout_data["first_name"], zip_code=checkout_data["zip_code"])
    logger.info("Entering first name and postal code, leaving last name blank...")

    checkout_page_one.click_continue_button()
    logger.info("Clicking continue button...")

    # verify error message for missing last name
    expect(checkout_page_one.error_message).to_have_text(checkout_step_1_errors["last_name"])
    logger.info("Verify: Error message for missing last name - passed")

    # ---------------- missing postal code ----------------
    checkout_page_one.enter_info(first_name=checkout_data["first_name"], last_name=checkout_data["last_name"])
    logger.info("Entering first name and last name, leaving postal code blank...")

    checkout_page_one.click_continue_button()
    logger.info("Clicking continue button...")

    # verify error message for missing postal code
    expect(checkout_page_one.error_message).to_have_text(checkout_step_1_errors["zip_code"])
    logger.info("Verify: Error message for missing postal code - passed")
