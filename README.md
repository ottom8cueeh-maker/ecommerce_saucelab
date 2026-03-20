# Ecommerce SauceLab UI Tests

UI test automation project for SauceDemo using Python, Pytest, Playwright, and a Page Object Model structure.

## Stack

- Python
- Pytest
- Playwright
- PyYAML
- python-dotenv

## Project Structure

```text
config/
data/
fixtures/
reports/
src/
tests/
  e2e/
  login/
ui/
  pom/
pytest.ini
requirements.txt
```

## Test Coverage

- Valid login flow
- Invalid login flow
- End-to-end purchase happy path

## Prerequisites

- Python 3.13 or compatible Python 3 version available locally
- A virtual environment
- Playwright browser binaries installed

## Setup

1. Create and activate a virtual environment.

```bash
python -m venv .venv
source .venv/Scripts/activate
```

2. Install project dependencies.

```bash
pip install -r requirements.txt
```

3. Install Playwright browsers.

```bash
playwright install
```

4. Create a `.env` file in the project root.

```env
TEST_VALID_USERNAME1=standard_user
TEST_VALID_PASSWORD=secret_sauce
TEST_BAD_USERNAME=locked_out_user
TEST_BAD_PASSWORD=wrong_password
```

## Test Data

Static checkout data is stored in `data/data.yaml` and loaded through fixtures in `tests/conftest.py`.

Current test data includes:

- Checkout first name, last name, and zip code
- Checkout completion page expected title and message

## Running Tests

Run the full suite:

```bash
pytest
```

Run the end-to-end happy path:

```bash
pytest tests/e2e/test_purchase_happy_path.py
```

Run the login tests:

```bash
pytest tests/login
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
- Page objects are located under `ui/pom`.
- Fixtures and shared test data loaders are located in `tests/conftest.py`.