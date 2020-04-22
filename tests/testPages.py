import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.main_page import *
from utils.testCases import test_cases


# I am using python unittest for asserting cases.
# In this module, there should be test cases.
# If you want to run it, you should type: python <module-name.py>

class TestPages(unittest.TestCase):

    def setUp(self):
        options = Options()
        # options.add_argument("--headless") # Runs Chrome in headless mode.
        options.add_argument('--no-sandbox')  # # Bypass OS security model
        options.add_argument('disable-infobars')
        options.add_argument("--disable-extensions")
        options.add_argument("--start-fullscreen")
        options.add_argument('--disable-gpu')

        self.driver = webdriver.Chrome(options=options)
        # self.driver = webdriver.Firefox()
        self.driver.get("http://www.amazon.com")

    def test_page_load(self):
        print("\n" + str(test_cases(0)))
        page = MainPage(self.driver)
        self.assertTrue(page.check_page_loaded())

    def test_search_item(self):
        print("\n" + str(test_cases(1)))
        page = MainPage(self.driver)
        search_result = page.search_item("iPhone 8")
        self.assertIn("iPhone 8", search_result)

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
        result = login_page.login_with_valid_user("valid_usrer")
        self.assertIn("yourstore/home", result.get_url())

    def test_sign_in_with_in_valid_user(self):
        print("\n" + str(test_cases(5)))
        main_page = MainPage(self.driver)
        login_page = main_page.click_sign_in_button()
        result = login_page.login_with_in_valid_user("invalid_user")
        self.assertIn("There was a problem with your request", result)

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPages)
    unittest.TextTestRunner(verbosity=2).run(suite)
