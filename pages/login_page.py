from utils.locators import *
from pages.base_page import BasePage
from pages.home_page import HomePage
from utils import users


class LoginPage(BasePage):
    def __init__(self, driver):
        self.locator = LoginPageLocators
        super(LoginPage, self).__init__(driver)  # Python2 version

    def enter_email(self, email):
        field = self.wait_and_find(*self.locator.EMAIL)
        try:
            field.clear()
        except Exception:
            pass
        field.send_keys(email)

    def enter_password(self, password):
        field = self.wait_and_find(*self.locator.PASSWORD)
        try:
            field.clear()
        except Exception:
            pass
        field.send_keys(password)

    def click_login_button(self):
        self.wait_and_find(*self.locator.SUBMIT).click()

    def login(self, user):
        user = users.get_user(user)
        print(user)
        if not user:
            return
        # Ensure we're on the sign in page
        if 'ap/signin' not in self.get_url():
            self.driver.get('https://www.amazon.com/ap/signin')
        # Accept cookies if banner appears
        try:
            btn = self.find_element(*self.locator.COOKIE_ACCEPT)
            btn.click()
        except Exception:
            pass
        self.enter_email(user["email"])
        self.enter_password(user["password"])
        self.click_login_button()

    def login_with_valid_user(self, user):
        self.login(user)
        return HomePage(self.driver)

    def login_with_in_valid_user(self, user):
        self.login(user)
        return self.find_element(*self.locator.ERROR_MESSAGE).text
