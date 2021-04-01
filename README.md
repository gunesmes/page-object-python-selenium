[page-object-python-selenium] is being sponsored by the following tool; please help to support us by taking a look and signing up to a free trial


# Selenium Page Object Model with Python 

Page-object-model (POM) is a pattern that you can apply it to develop efficient automation framework. With page-model, it is possible to minimise maintenance cost. Basically page-object means that your every page is inherited from a base class which includes basic functionalities for every pages. If you have some new functionality that every pages have, you can simple add it to the base class.

`BasePage` class include basic functionality and driver initialization
```python
base_page.py
class BasePage(object):
    def __init__(self, driver, base_url='http://www.amazon.com/'):
        self.base_url = base_url
        self.driver = driver
        self.timeout = 30

    def find_element(self, *locator):
        return self.driver.find_element(*locator)
```

`MainPage` is derived from the `BasePage class, it contains methods related to this page, which will be used to create test steps.
```python
# main_page.py
class MainPage(BasePage):
    def __init__(self, driver):
        self.locator = MainPageLocators
        super().__init__(driver)  # Python3 version

    def check_page_loaded(self):
        return True if self.find_element(*self.locator.LOGO) else False
```

When you want to write tests, you should derive your test class from `BaseTest` which holds basic functionality for your tests. Then you can call  page and related methods in accordance with the steps in the test cases
```python
class TestSignInPage(BaseTest):

    def test_sign_in_with_valid_user(self):
        print("\n" + str(test_cases(4)))
        main_page = MainPage(self.driver)
        login_page = main_page.click_sign_in_button()
        result = login_page.login_with_valid_user("valid_user")
        self.assertIn("yourstore/home", result.get_url())
```

#### If you want to run all tests, you should type: 
```sh
python -m unittest 
```


#### If you want to run just a class, you should type: 
```sh
python -m unittest tests.test_sign_in_page.TestSignInPage
```

#### If you want to run just a test method, you should type: 
```sh
python -m unittest tests.test_sign_in_page.TestSignInPage.test_page_load
```
