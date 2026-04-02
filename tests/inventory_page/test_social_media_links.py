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
    login_page.login(login_page.valid_username1, login_page.valid_password)
    # --------------------------- inventory page -----------------------------------
    # wait for inventory page to load
    page.wait_for_url(products_url)
    inventory_page = InventoryPage(page)
    page.wait_for_load_state("domcontentloaded")
    expect(inventory_page.shopping_cart).to_be_visible()
    assert page.url == products_url, f"Expected URL {products_url}, got {page.url}"
    logger.info("%s loaded successfully", products_url)

    # --------------------------- social media links -----------------------------------
    # Capture the new tab opened by clicking the Twitter footer link:  x.com (formerly Twitter) is loaded
    with page.context.expect_page() as new_page_info:
        inventory_page.twitter_link.click()
        logger.info("Clicking Twitter (X) footer link...")

    new_page = new_page_info.value
    new_page.wait_for_load_state()
    assert x_url in new_page.url, f"Expected URL containing {x_url}, got {new_page.url}"
    logger.info("Verified X (Twitter) link opens %s", new_page.url)
    new_page.close()

    # Capture the new tab opened by clicking the Facebook footer link
    with page.context.expect_page() as new_page_info:
        inventory_page.facebook_link.click()
        logger.info("Clicking Facebook footer link...")
    new_page = new_page_info.value
    new_page.wait_for_load_state()
    assert facebook_url in new_page.url, f"Expected URL containing {facebook_url}, got {new_page.url}"
    logger.info("Verified Facebook link opens %s", new_page.url)
    new_page.close()

    # # Capture the new tab opened by clicking the LinkedIn footer link
    with page.context.expect_page() as new_page_info:
        inventory_page.linkedin_link.click()
        logger.info("Clicking LinkedIn footer link...")

    new_page = new_page_info.value
    new_page.wait_for_load_state()

    assert linkedin_url in new_page.url, f"Expected URL containing {linkedin_url}, got {new_page.url}"
    logger.info("Verified LinkedIn link opens %s", new_page.url)
    new_page.close()
