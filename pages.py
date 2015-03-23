from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from base import Page
from locators import *
import users, functions
from selenium.webdriver.support.ui import WebDriverWait


# Page opjects are written in this module.
# Depends on the page functionality we can have more functions for new classes

class MainPage(Page):
    def check_page_loaded(self):
        return True if self.find_element(*MainPageLocatars.LOGO) else False

    def search_item(self, item):
        self.find_element(*MainPageLocatars.SEARCH).send_keys(item)
        self.find_element(*MainPageLocatars.SEARCH).send_keys(Keys.ENTER)
        return self.find_element(*MainPageLocatars.SEARCH_LIST).text
        
    def click_sign_up_button(self):
        self.hover(*MainPageLocatars.ACCOUNT)
        self.driver.find_element(*MainPageLocatars.SIGNUP).click()
        return SignUpPage(self.driver)

    def click_sign_in_button(self):
        self.hover(*MainPageLocatars.ACCOUNT)
        self.driver.find_element(*MainPageLocatars.LOGIN).click()
        return LoginPage(self.driver)

class LoginPage(Page):
    def enter_email(self, user):
        self.driver.find_element(*LoginPageLocatars.EMAIL).send_keys(users.get_user(user)["email"])

    def enter_password(self, user):
        self.driver.find_element(*LoginPageLocatars.PASSWORD).send_keys(users.get_user(user)["password"])

    def click_login_button(self):
        self.driver.find_element(*LoginPageLocatars.SUBMIT).click()

    def login(self, user):
        self.enter_email(user)
        self.enter_password(user)
        self.click_login_button()

    def login_with_valid_user(self, user):
        self.login(user)
        return HomePage(self.driver)

    def login_with_in_valid_user(self, user):
        self.login(user)
        return self.find_element(*LoginPageLocatars.ERROR_MESSAGE).text    

class HomePage(Page):
    pass
    
class SignUpPage(Page):
    pass