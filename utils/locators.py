from selenium.webdriver.common.by import By


# for maintainability we can seperate web objects by page name

class MainPageLocators(object):
    # Amazon has used both #nav-logo and #nav-logo-sprites historically; use a CSS grouping selector.
    LOGO = (By.CSS_SELECTOR, '#nav-logo, #nav-logo-sprites')
    ACCOUNT = (By.ID, 'nav-link-accountList')
    # These tooltip links often require hover to display; selectors may change. Consider refining later.
    SIGNUP = (By.CSS_SELECTOR, '#nav-signin-tooltip a[href*="register"]')
    LOGIN = (By.CSS_SELECTOR, '#nav-signin-tooltip a[href*="signin"]')
    SEARCH = (By.ID, 'twotabsearchtextbox')
    SEARCH_LIST = (By.CSS_SELECTOR, 'div[data-component-type="s-search-result"]')


class LoginPageLocators(object):
    EMAIL = (By.ID, 'ap_email')
    PASSWORD = (By.ID, 'ap_password')
    SUBMIT = (By.ID, 'signInSubmit')
    ERROR_MESSAGE = (By.ID, 'auth-error-message-box')
    COOKIE_ACCEPT = (By.ID, 'sp-cc-accept')
