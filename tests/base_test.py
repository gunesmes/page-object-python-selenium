import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# I am using python unittest for asserting cases.
# In this module, there should be test cases.
# If you want to run it, you should type: python <module-name.py>

class BaseTest(unittest.TestCase):

    def setUp(self):
        options = Options()
        options.add_argument("--headless=new")  # Uncomment for headless runs
        options.add_argument('--no-sandbox')  # Bypass OS security model
        options.add_argument('disable-infobars')
        options.add_argument('--disable-extensions')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-gpu')

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.get("https://www.amazon.com")

    # Additional driver initializations (e.g., Firefox) can be added here if needed.

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(BaseTest)
    unittest.TextTestRunner(verbosity=1).run(suite)
