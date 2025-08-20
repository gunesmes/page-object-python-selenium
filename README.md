
# Selenium Page Object Model with Python

Page-object-model (POM) is a pattern that you can apply it to develop efficient automation framework. With page-model, it is possible to minimise maintenance cost. Basically page-object means that your every page is inherited from a base class which includes basic functionalities for every pages. If you have some new functionality that every pages have, you can simple add it to the base class.

## Overview

This project demonstrates a minimal Page Object Model (POM) test framework using Python's built‑in `unittest` and Selenium. It now uses `webdriver-manager` to automatically download a compatible ChromeDriver, reducing friction from local browser / driver version mismatches, and a Python virtual environment for isolated dependencies.

## Base Page

`BasePage` class includes basic functionality and shared driver helpers (plus explicit waiting utilities now):
```python
# base_page.py
class BasePage(object):
    def __init__(self, driver, base_url='http://www.amazon.com/'):
        self.base_url = base_url
        self.driver = driver
        self.timeout = 30

    def find_element(self, *locator):
        return self.driver.find_element(*locator)
```

## Main Page

`MainPage` is derived from `BasePage`; it contains methods related to the Amazon home page (logo presence, search, sign in / sign up navigation with resilient fallbacks and waits).
```python
# main_page.py
class MainPage(BasePage):
    def __init__(self, driver):
        self.locator = MainPageLocators
        super().__init__(driver)  # Python3 version

    def check_page_loaded(self):
        try:
            self.wait_element(*self.locator.LOGO)
            return True
        except Exception:
            return False
```

## Tests

When you write tests, derive from `BaseTest` which sets up / tears down the WebDriver. The test classes use page objects for readable steps.
```python
# test_sign_in_page.py
class TestSignInPage(BaseTest):
    def test_sign_in_with_valid_user(self):
        print("\n" + str(test_cases(4)))
        main_page = MainPage(self.driver)
        login_page = main_page.click_sign_in_button()
        result = login_page.login_with_valid_user("valid_user")
        self.assertIn("yourstore/home", result.get_url())
```

## Project Structure

```
pages/          # Page Objects (Base, Main, Login, Signup, Home)
tests/          # unittest test modules
utils/          # Locators, users (test data), test case descriptions
requirements.txt
```

## Setup (Virtual Environment)

Create and activate a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS / Linux
# On Windows: .venv\\Scripts\\activate
pip install --upgrade pip
pip install -r requirements.txt
```

Deactivate with:

```bash
deactivate
```

## WebDriver Management

ChromeDriver version drift is a common source of failures. We use `webdriver-manager` so the correct driver binary is auto-downloaded at runtime:

```python
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
```

You no longer need to manually place `chromedriver` on your PATH. For CI, caching the `.wdm/` directory (added to `.gitignore`) can speed up runs.

## Running Tests

Run all tests:
```bash
python -m unittest
```

Run a single test class:
```bash
python -m unittest tests.test_sign_in_page.TestSignInPage
```

Run a single test method:
```bash
python -m unittest tests.test_sign_in_page.TestSignInPage.test_page_load
```

## Headless Mode

Uncomment the `--headless=new` argument in `tests/base_test.py` to run without opening a browser window (useful for CI pipelines).

## Notes / Future Improvements

- Amazon DOM changes frequently; for reliability consider switching to a stable demo site (e.g. saucedemo.com) or introducing a layer of resilient locator strategies.
- Add reporting (HTML) or coverage if needed (not included currently to keep dependencies minimal).
- Implement retries or smarter waits for dynamic content.

## License

See `LICENSE`.
