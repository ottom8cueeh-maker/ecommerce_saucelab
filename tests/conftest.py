"""Shared pytest fixtures for the SauceDemo e2e test suite."""
import pytest
import yaml
from pathlib import Path
from playwright.sync_api import Playwright

@pytest.fixture(scope="session")
def playwright(playwright: Playwright):
    """Configure Playwright to use 'data-test' as the test ID attribute for all sessions."""
    playwright.selectors.set_test_id_attribute("data-test")
    yield playwright

@pytest.fixture(scope="session")
def test_data():
    """Load and return all test data from data/data.yaml as a dictionary."""
    data_file = Path(__file__).parent.parent / "data" / "data.yaml"
    with open(data_file) as f:
        return yaml.safe_load(f)

@pytest.fixture(scope="session")
def checkout_data(test_data):
    """Return the checkout step one form data (first name, last name, zip code)."""
    return test_data["checkout_step_1_data"]

@pytest.fixture(scope="session")
def checkout_complete_data(test_data):
    """Return the expected text values for the checkout complete confirmation page."""
    return test_data["checkout_complete"]

@pytest.fixture
def products_url():
    """Return the URL for the inventory/products page."""
    return "https://www.saucedemo.com/inventory.html"

@pytest.fixture
def cart_url():
    """Return the URL for the shopping cart page."""
    return "https://www.saucedemo.com/cart.html"

@pytest.fixture
def checkout_step_one_url():
    """Return the URL for the checkout step one (customer info) page."""
    return "https://www.saucedemo.com/checkout-step-one.html"

@pytest.fixture
def checkout_step_two_url():
    """Return the URL for the checkout step two (order summary) page."""
    return "https://www.saucedemo.com/checkout-step-two.html"
