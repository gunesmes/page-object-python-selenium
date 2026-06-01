# Selenium Page Transactions Boilerplate (with Guará)
This repository demonstrates an advanced automation architecture that evolves the traditional **Page Object Model (POM)** into **Page Transactions** using the [Guará](https://github.com) framework.

By adding a semantic transaction layer over standard Page Objects, tests become highly readable, decoupled from UI details, and focused entirely on the user's business journey.
## 🚀 Key Benefits
- **Fluent BDD Syntax:** Writes like Gherkin (`given`, `when`, `then`) but runs natively in pure Python code.
- **Better Separation of Concerns:** Page Objects handle HTML element selectors, while Transactions handle business behaviors and workflows.
- **High Maintainability:** Steps are encapsulated. Changes in a user workflow require updating only a single Transaction class rather than multiple test files.

## 💻 Code Examples
### 1. The Transaction Layer (`transactions/login_transaction.py`)
Transactions group atomic Page Object steps into comprehensive user behaviors.
```python
from guara.transaction import AbstractTransaction
from pages.login_page import LoginPage
from pages.main_page import MainPage

class UserInMainPage(AbstractTransaction):
    def do(self):
        main_page = MainPage(self._driver)
        main_page.click_sign_in_button()

class UserLogin(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)

    def do(self, with_username, with_secret):
        login_page = LoginPage(self._driver)
        login_page.enter_email(with_username)
        login_page.enter_password(with_secret)
        login_page.login()
        return self._driver.current_url
```

### 2. The Test Script (`tests/test_login_transaction.py`)
Tests are purely declarative, describing *what* happens rather than *how* it happens.
```python
import unittest
from guara import it
from guara.transaction import Application
from tests.base_test import BaseTest
from transactions.login_transaction import UserLogin, UserInMainPage

class TestLoginTransaction(BaseTest):

    def test_user_can_login_successfully(self):
        app = Application(self.driver)
        
        (
            app.given(UserInMainPage)
            .when(
                UserLogin,
                with_username="test_user",
                with_secret="secure_password"
            )
            .then(it.Contains, "dashboard")
        )

if __name__ == "__main__":
    unittest.main()
```
