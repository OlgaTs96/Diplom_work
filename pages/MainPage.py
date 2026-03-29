from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver


class MainPage:
    """
    Класс, представляющий главную страницу сайта.
    """

    def __init__(self, driver: WebDriver):
        """
        Инициализация страницы и открытие сайта.
        :param driver: WebDriver - экземпляр Selenium WebDriver.
        """
        self._driver: WebDriver = driver
        self._driver.get('https://ru.yougile.com/')
        self._wait: WebDriverWait = WebDriverWait(driver, 10)

    def click_login_button(self) -> None:
        """
        Нажимает на кнопку входа.
        Ожидает, что кнопка станет кликабельной, и кликает по ней.

        :return: None
        """
        login_btn = self._wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '.btn-outline-primary')))
        login_btn.click()

    def go_to_login_page(self) -> None:
        """
        Переходит на страницу входа, вызывая кнопку входа.

        :return: None
        """
        self.click_login_button()

    def authorization_username(self, email: str) -> None:
        """
        Вводит email в поле для ввода email.

        :param email: str - адрес электронной почты для авторизации.
        :return: None
        """
        email_input = self._wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//input[@type='email']")))
        email_input.clear()
        email_input.send_keys(email)

    def authorization_password(self, password: str) -> None:
        """
        Вводит пароль и отправляет форму.

        :param password: str - пароль для авторизации.
        :return: None
        """
        password_input = self._wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//input[@type='password']")))
        password_input.clear()
        password_input.send_keys(password)
        submit_btn = self._wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".hint__cnt")))
        submit_btn.click()

    def login_as(self, email: str, password: str) -> None:
        """
        Выполняет полный вход под указанным пользователем (авторизация).

        :param email: str - адрес электронной почты.
        :param password: str - пароль.
        :return: None
        """
        self.go_to_login_page()
        self.authorization_username(email)
        self.authorization_password(password)

    def go_to_home(self):
        self._driver.get('https://ru.yougile.com/')
