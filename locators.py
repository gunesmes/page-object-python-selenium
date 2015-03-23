from selenium.webdriver.common.by import By

# for maintainability we can seperate web objects by page name

class MainPageLocatars(object):
  LOGO 					= (By.ID, 'nav-logo')
  ACCOUNT       = (By.ID, 'nav-link-yourAccount')
  SIGNUP 				= (By.CSS_SELECTOR, '#nav-flyout-ya-newCust > a')
  LOGIN 				= (By.CSS_SELECTOR, '#nav-flyout-ya-signin > a')
  SEARCH        = (By.ID, 'twotabsearchtextbox')
  SEARCH_LIST 	= (By.ID, 's-results-list-atf')

class LoginPageLocatars(object):
  EMAIL 				= (By.ID, 'ap_email')
  PASSWORD 			= (By.ID, 'ap_password')
  SUBMIT 				= (By.ID, 'signInSubmit-input')
  ERROR_MESSAGE = (By.ID, 'message_error')
