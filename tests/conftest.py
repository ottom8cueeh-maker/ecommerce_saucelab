import pytest
import yaml
from pathlib import Path
from playwright.sync_api import Playwright

@pytest.fixture(scope="session")
def playwright(playwright: Playwright):
    playwright.selectors.set_test_id_attribute("data-test")
    yield playwright

@pytest.fixture(scope="session")
def test_data():
    data_file = Path(__file__).parent.parent / "data" / "data.yaml"
    with open(data_file) as f:
        return yaml.safe_load(f)

@pytest.fixture(scope="session")
def checkout_data(test_data):
    return test_data["checkout_step_1_data"]

@pytest.fixture(scope="session")
def checkout_complete_data(test_data):
    return test_data["checkout_complete"]

@pytest.fixture
def products_url():
    return "https://www.saucedemo.com/inventory.html"

@pytest.fixture
def cart_url():
    return "https://www.saucedemo.com/cart.html"

@pytest.fixture
def checkout_step_one_url():
    return "https://www.saucedemo.com/checkout-step-one.html"

@pytest.fixture
def checkout_step_two_url():
    return "https://www.saucedemo.com/checkout-step-two.html"
