from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
from pages.login_page import LoginPage
from pages.signup_page import SignUpBasePage
from utils.locators import *
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException


# Page objects are written in this module.
# Depends on the page functionality we can have more functions for new classes

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

    def search_item(self, item):
        search_box = self.wait_and_find(*self.locator.SEARCH)
        search_box.clear()
        search_box.send_keys(item)
        search_box.send_keys(Keys.ENTER)
        return self.wait_and_find(*self.locator.SEARCH_LIST).text

    def click_sign_up_button(self):
        # Try opening the tooltip; fallback to direct URL if not interactable
        try:
            try:
                self.hover(*self.locator.ACCOUNT)
            except Exception:
                pass
            el = self.wait_and_find(*self.locator.SIGNUP)
            el.click()
        except (NoSuchElementException, ElementNotInteractableException, TimeoutException):
            # Direct navigation fallback (more stable for Amazon dynamic header changes)
            self.driver.get("https://www.amazon.com/ap/register")
        return SignUpBasePage(self.driver)

    def click_sign_in_button(self):
        try:
            try:
                self.hover(*self.locator.ACCOUNT)
            except Exception:
                pass
            el = self.wait_and_find(*self.locator.LOGIN)
            el.click()
        except (NoSuchElementException, ElementNotInteractableException, TimeoutException):
            self.driver.get("https://www.amazon.com/ap/signin")
        return LoginPage(self.driver)
