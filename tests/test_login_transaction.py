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
