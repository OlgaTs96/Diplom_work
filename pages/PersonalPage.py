from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class PersonalPage:
    """
    Класс, представляющий страницу личного кабинета
    или личной страницы пользователя.
    """

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация объекта страницы.

        :param driver: WebDriver - экземпляр Selenium WebDriver.
        """
        self.driver: WebDriver = driver
        self._wait: WebDriverWait = WebDriverWait(self.driver, 30)

    def click_button(self) -> None:
        """
        Нажимает на кнопку "Добавить проект с задачами".
        Ожидает, что кнопка станет кликабельной, и кликает по ней.

        :return: None
        """
        button = self._wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//span[text()="Добавить проект с задачами"]')
            )
        )
        button.click()

    def create_new_prod(self, value: str) -> None:
        """
        Создает новый проект, вводя название и подтверждая.

        :param value: str - название проекта, которое нужно ввести.
        :return: None
        """
        name_prod = self._wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR,
                 "input[placeholder='Введите название проекта…']")
            )
        )
        name_prod.clear()
        name_prod.send_keys(value)

        add_prod = self._wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[text()='Добавить проект с задачами']")
            )
        )
        add_prod.click()

    def open_prod(self) -> None:
        """
        Открывает существующий проект с названием "Diplom".

        :return: None
        """
        xpath_expr = (
            "//div[@data-testid='project-title' "
            "and normalize-space(text())='Diplom']"
        )
        open_btn = self._wait.until(
            EC.element_to_be_clickable((By.XPATH, xpath_expr))
        )
        open_btn.click()

    def create_task(self) -> None:
        """
        Создает новую задачу: кликает кнопку "Добавить задачу",
        вводит название задачи и подтверждает.

        :return: None
        """
        create_task_btn = self._wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[text()='Добавить задачу']")
            )
        )
        create_task_btn.click()

        task_input = self._wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//textarea[@data-testid='board-task-input-name']")
            )
        )
        task_input.send_keys("Задача 1")
        task_input.send_keys(Keys.ENTER)

    def delete_task(self) -> None:
        """
        Удаляет первую задачу. Открывает меню задачи,
        нажимает "Удалить" и подтверждает удаление.

        :return: None
        """
        menu_btn = self._wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@data-testid='board-task-menu']")
            )
        )
        menu_btn.click()

        delete_btn = self._wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[text()='Удалить']")
            )
        )
        delete_btn.click()

        confirm_delete_btn = self._wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[text()='Удалить']")
            )
        )
        confirm_delete_btn.click()
