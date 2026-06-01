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
