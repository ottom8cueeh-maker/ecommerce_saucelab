"""Shared pytest fixtures for the SauceDemo e2e test suite."""
from pathlib import Path
import pytest
import yaml
from playwright.sync_api import Playwright

@pytest.fixture(scope="session", autouse=True)
def configure_playwright(playwright: Playwright):
    """Auto-use session fixture that configures Playwright to use 'data-test' as the test ID attribute."""
    playwright.selectors.set_test_id_attribute("data-test")

@pytest.fixture(scope="session")
def captured_data():
    """Load and return all test data from data/captured_data.yaml as a dictionary."""
    data_file = Path(__file__).parent.parent / "data" / "captured_data.yaml"
    with open(data_file, encoding="utf-8") as f:
        return yaml.safe_load(f)

@pytest.fixture(scope="session")
def input_data():
    """Load and return all test data from data/input_data.yaml as a dictionary."""
    data_file = Path(__file__).parent.parent / "data" / "input_data.yaml"
    with open(data_file, encoding="utf-8") as f:
        return yaml.safe_load(f)

@pytest.fixture(scope="session")
def checkout_data(input_data):
    """Return the checkout step one form data (first name, last name, zip code)."""
    return input_data["checkout_step_1_data"]

@pytest.fixture(scope="session")
def checkout_step_1_errors(captured_data):  # noqa: F811
    """Return the expected error messages for the checkout step one form validation."""
    return captured_data["checkout_step_1_errors"]

@pytest.fixture(scope="session")
def checkout_complete_data(captured_data):  # noqa: F811
    """Return the expected text values for the checkout complete confirmation page."""
    return captured_data["checkout_complete"]

# URL fixtures for all pages in the user flow, for easy maintenance and readability in tests
@pytest.fixture
def products_url(base_url):
    """Return the URL for the inventory/products page."""
    return f"{base_url}inventory.html"

@pytest.fixture
def cart_url(base_url):
    """Return the URL for the shopping cart page."""
    return f"{base_url}cart.html"

@pytest.fixture
def checkout_step_one_url(base_url):
    """Return the URL for the checkout step one (customer info) page."""
    return f"{base_url}checkout-step-one.html"

@pytest.fixture
def checkout_step_two_url(base_url):
    """Return the URL for the checkout step two (order summary) page."""
    return f"{base_url}checkout-step-two.html"

@pytest.fixture
def checkout_complete_url(base_url):
    """Return the URL for the checkout complete confirmation page."""
    return f"{base_url}checkout-complete.html"

# social media URLs for inventory page footer links
@pytest.fixture
def x_url():
    """Return the URL for the Sauce Labs X (Twitter) page."""
    return "https://x.com/saucelabs"

@pytest.fixture
def facebook_url():
    """Return the URL for the Sauce Labs Facebook page."""
    return "https://www.facebook.com/saucelabs"

@pytest.fixture
def linkedin_url():
    """Return the URL for the Sauce Labs LinkedIn page."""
    return "https://www.linkedin.com/company/sauce-labs/"
