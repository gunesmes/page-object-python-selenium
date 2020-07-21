import unittest
from tests.base_test import BaseTest
from pages.main_page import *
from utils.test_cases import test_cases


# I am using python unittest for asserting cases.
# In this module, there should be test cases.
# If you want to run it, you should type: python <module-name.py>

class TestSignInPage(BaseTest):

    def test_page_load(self):
        print("\n" + str(test_cases(0)))
        page = MainPage(self.driver)
        self.assertTrue(page.check_page_loaded())

    def test_search_item(self):
        print("\n" + str(test_cases(1)))
        page = MainPage(self.driver)
        search_result = page.search_item("iPhone")
        self.assertIn("iPhone", search_result)

    def test_sign_up_button(self):
        print("\n" + str(test_cases(2)))
        page = MainPage(self.driver)
        sign_up_page = page.click_sign_up_button()
        self.assertIn("ap/register", sign_up_page.get_url())

    def test_sign_in_button(self):
        print("\n" + str(test_cases(3)))
        page = MainPage(self.driver)
        login_page = page.click_sign_in_button()
        self.assertIn("ap/signin", login_page.get_url())

    def test_sign_in_with_valid_user(self):
        print("\n" + str(test_cases(4)))
        main_page = MainPage(self.driver)
        login_page = main_page.click_sign_in_button()
        result = login_page.login_with_valid_user("valid_user")
        self.assertIn("yourstore/home", result.get_url())

    def test_sign_in_with_in_valid_user(self):
        print("\n" + str(test_cases(5)))
        main_page = MainPage(self.driver)
        login_page = main_page.click_sign_in_button()
        result = login_page.login_with_in_valid_user("invalid_user")
        self.assertIn("There was a problem with your request", result)
