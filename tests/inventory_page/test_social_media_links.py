"""Tests for the social media footer links on the SauceDemo inventory page."""
import logging
from playwright.sync_api import expect
import pytest
from pom.inventory import InventoryPage
from pom.startingpage import StartingPage
from pom.login import LoginPage

logger = logging.getLogger(__name__)

@pytest.mark.FUNCTIONAL
def test_social_media_links(page, base_url, x_url, facebook_url, linkedin_url):
    """
    Verify that the social media links in the footer of the inventory page navigate to the correct URLs.

    Steps:
        1. Log in with valid credentials.
        2. Click on each social media link (Twitter, Facebook, LinkedIn) in the footer.
        3. Verify that each link opens the correct URL in a new tab.
    """
    # Initialize page objects
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    starting_page = StartingPage(page)

    # Define URLs for verification
    products_url = f"{base_url}inventory.html"

    starting_page.goto_url(base_url)

    # ------------------------------- Login page -----------------------------------
    expect(page).to_have_url(base_url)
    expect(login_page.login_button, message="Login button is not visible on the login page").to_be_visible()

    # TEST happy path login using credentials from environment variables
    logger.info("Login page: Logging in with valid credentials...")
    login_page.login(login_page.valid_username1, login_page.valid_password)

    # --------------------------- inventory page -----------------------------------
    # wait for inventory page to load
    expect(page).to_have_url(products_url)
    expect(inventory_page.shopping_cart).to_be_visible()
    logger.info("%s loaded successfully", products_url)

    # --------------------------- social media links -----------------------------------
    # Capture the new tab opened by clicking the Twitter footer link:  x.com (formerly Twitter) is loaded
    with page.context.expect_page() as new_page_info:
        inventory_page.twitter_link.click()
        logger.info("Clicking Twitter (X) footer link...")

    new_page = new_page_info.value
    new_page.wait_for_load_state()
    expect(new_page).to_have_url(x_url)
    logger.info("Verified X (Twitter) link opens %s", new_page.url)
    new_page.close()

    # Capture the new tab opened by clicking the Facebook footer link
    with page.context.expect_page() as new_page_info:
        inventory_page.facebook_link.click()
        logger.info("Clicking Facebook footer link...")

    new_page = new_page_info.value
    new_page.wait_for_load_state()
    expect(new_page).to_have_url(facebook_url)
    logger.info("Verified Facebook link opens %s", new_page.url)
    new_page.close()

    # # Capture the new tab opened by clicking the LinkedIn footer link
    with page.context.expect_page() as new_page_info:
        inventory_page.linkedin_link.click()
        logger.info("Clicking LinkedIn footer link...")

    new_page = new_page_info.value
    new_page.wait_for_load_state()
    expect(new_page).to_have_url(linkedin_url)
    logger.info("Verified LinkedIn link opens %s", new_page.url)
    new_page.close()
