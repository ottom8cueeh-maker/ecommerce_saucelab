# Ecommerce SauceLab UI Tests

UI test automation project for [SauceDemo](https://www.saucedemo.com) using Python, Pytest, Playwright, and a Page Object Model (POM) structure.

## Stack

| Package | Version |
|---|---|
| playwright | 1.58.0 |
| pytest | 9.0.2 |
| pytest-playwright | 0.7.2 |
| pytest-base-url | 2.1.0 |
| PyYAML | 6.0.3 |
| python-dotenv | 1.2.2 |

## Project Structure

```text
ecommerce_saucelab/
├── config/
│   └── config.yaml
├── data/
│   ├── captured_data.yaml    # expected values (error messages, confirmation text)
│   └── input_data.yaml       # form input data (checkout fields)
├── pom/                      # Page Object Model classes
│   ├── checkout_complete.py
│   ├── checkout_step_one.py
│   ├── checkout_step_two.py
│   ├── inventory.py
│   ├── items.py
│   ├── login.py
│   ├── menu.py
│   ├── shopping_cart.py
│   └── startingpage.py
├── reports/
├── src/
├── tests/
│   ├── conftest.py
│   ├── buttons/
│   │   ├── test_add_remove_inventory_and_cart.py
│   │   ├── test_add_remove_inventoryitem.py
│   │   └── test_page_navigation_buttons.py
│   ├── e2e/
│   │   └── test_purchase_happy_path.py
│   ├── error_messages/
│   │   └── test_checkout_step1_errors.py
│   ├── login/
│   │   ├── test_invalid_credentials.py
│   │   └── test_valid_credentials.py
│   ├── menu/
│   │   └── menu_functionalities.py
│   └── product_sort/
│       ├── test_product_sorter.py
│       └── test_social_media_links.py
├── pytest.ini
└── requirements.txt
```

## Test Coverage

| Module | Test File | Description |
|---|---|---|
| Login | `tests/login/test_valid_credentials.py` | Valid login redirects to inventory page |
| Login | `tests/login/test_invalid_credentials.py` | Invalid credentials are rejected with an error message |
| Buttons | `tests/buttons/test_add_remove_inventory_and_cart.py` | Add/remove items from the inventory and cart pages |
| Buttons | `tests/buttons/test_add_remove_inventoryitem.py` | Add/remove an item from the item details page |
| Buttons | `tests/buttons/test_page_navigation_buttons.py` | Page navigation buttons move the user through checkout |
| Error Messages | `tests/error_messages/test_checkout_step1_errors.py` | Checkout step one form validation error messages |
| Menu | `tests/menu/menu_functionalities.py` | Sidebar menu items are visible and functional |
| Social Media | `tests/product_sort/test_social_media_links.py` | Footer social media links open the correct URLs in a new tab |
| Product Sort | `tests/product_sort/test_product_sorter.py` | Inventory sort by price (low/high) and name (A-Z/Z-A) |
| E2E | `tests/e2e/test_purchase_happy_path.py` | Full purchase flow from login to order confirmation |

### Markers

- `SMOKE` — core smoke tests
- `REGRESSION` — regression tests

## Prerequisites

- Python 3.13 (or compatible Python 3 version)
- A virtual environment
- Playwright browser binaries

## Setup

1. Create and activate a virtual environment.

```bash
python -m venv .venv
source .venv/Scripts/activate   # Windows (Git Bash)
# or
.venv\Scripts\activate          # Windows (cmd / PowerShell)
```

2. Install project dependencies.

```bash
pip install -r requirements.txt
```

3. Install Playwright browsers.

```bash
playwright install
```

4. Create a `.env` file in the project root with credentials for the SauceDemo site.

```env
TEST_VALID_USERNAME1=standard_user
TEST_VALID_PASSWORD=secret_sauce
TEST_BAD_USERNAME=locked_out_user
TEST_BAD_PASSWORD=wrong_password
```

## Test Data

Test data is split across two YAML files in `data/` and loaded via session-scoped fixtures in `tests/conftest.py`.

| File | Fixture | Contents |
|---|---|---|
| `data/input_data.yaml` | `input_data`, `checkout_data` | Checkout form inputs (first name, last name, zip code) |
| `data/captured_data.yaml` | `captured_data`, `checkout_step_1_errors`, `checkout_complete_data` | Expected error messages and order confirmation text |

### URL Fixtures

URL fixtures are defined directly in `tests/conftest.py` (no YAML file).

| Fixture | Value |
|---|---|
| `products_url` | `https://www.saucedemo.com/inventory.html` |
| `cart_url` | `https://www.saucedemo.com/cart.html` |
| `checkout_step_one_url` | `https://www.saucedemo.com/checkout-step-one.html` |
| `checkout_step_two_url` | `https://www.saucedemo.com/checkout-step-two.html` |
| `x_url` | `https://x.com/saucelabs` |
| `facebook_url` | `https://www.facebook.com/saucelabs` |
| `linkedin_url` | `https://www.linkedin.com/company/sauce-labs` |

## Running Tests

Run the full suite:

```bash
pytest
```

Run only SMOKE tests:

```bash
pytest -m SMOKE
```

Run a specific module:

```bash
pytest tests/e2e/test_purchase_happy_path.py
pytest tests/login/
pytest tests/buttons/
pytest tests/error_messages/
pytest tests/menu/
pytest tests/product_sort/
```

Run smoke tests only:

```bash
pytest -m SMOKE
```

## Pytest Configuration

The project uses `pytest.ini` for:

- project root on `PYTHONPATH`
- headed browser execution
- slow motion for browser actions
- base URL configuration
- CLI logging

## Notes

- The framework uses Playwright's `data-test` selector strategy where appropriate.
- Page objects are located under `pom`.
- Fixtures and shared test data loaders are located in `tests/conftest.py`.