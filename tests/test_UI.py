import pytest
import os
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from dotenv import load_dotenv
from pages.MainPage import MainPage
from pages.PersonalPage import PersonalPage

load_dotenv()


@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


@pytest.mark.ui
def test_authentication_positive(driver):
    """Тест: Успешная авторизация"""
    with allure.step("Открываем страницу и авторизуемся "
                     "(позитивный сценарий)"):
        page = MainPage(driver)

        with allure.step("Кликаем кнопку входа"):
            page.click_login_button()

        email = os.getenv("login")
        password = os.getenv("password")

        with allure.step("Вводим email и пароль, подтверждаем"):
            page.authorization_username(email)
            page.authorization_password(password)

        with allure.step("Ожидаем перенаправления на страницу команды"):
            WebDriverWait(driver, 30).until(
                EC.url_to_be("https://ru.yougile.com/team/")
            )

        with allure.step("Проверка текущего URL"):
            assert driver.current_url == "https://ru.yougile.com/team/", (
                f"URL: {driver.current_url} != ожидаемый."
            )


@pytest.mark.ui
def test_authentication_negative(driver):
    """Тест: Неуспешная авторизация с неправильными данными"""
    with allure.step("Открываем страницу и пытаемся авторизоваться "
                     "с неправильными данными"):
        page = MainPage(driver)

        with allure.step("Кликаем кнопку входа"):
            page.click_login_button()

        invalid_email = "incorrect_email@example.com"
        invalid_password = "wrongpassword"

        with allure.step("Вводим неправильный email и пароль"):
            page.authorization_username(invalid_email)
            page.authorization_password(invalid_password)

        with allure.step("Ожидаем сообщение об ошибке"):
            wait = WebDriverWait(driver, 10)
            error_locator = (By.CSS_SELECTOR, '.login-error')
            error_element = wait.until(
                EC.presence_of_element_located(error_locator))
            assert error_element.is_displayed(), "Сообщение об ошибке "
            "не отображается"


@pytest.mark.ui
def test_create_prod(driver):
    """Тест: Создание нового проекта 'Diplom'"""
    with allure.step("Авторизация и создание нового проекта 'Diplom'"):
        page = MainPage(driver)

        with allure.step("Кликаем кнопку входа и вводим данные"):
            page.go_to_home
            page.click_login_button()
            email = os.getenv("login")
            password = os.getenv("password")
            page.authorization_username(email)
            page.authorization_password(password)

        with allure.step("Переходим на личную страницу и "
                         "создаем проект 'Diplom'"):
            personal_page = PersonalPage(driver)
            personal_page.click_button()
            personal_page.create_new_prod('Diplom')

        with allure.step("Проверяем наличие проекта 'Diplom' на странице"):
            wait = WebDriverWait(driver, 30)
            diplom_element = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[contains(text(), 'Diplom')]")
                )
            )

            assert diplom_element is not None, "Не найден элемент "
            "с текстом 'Diplom'"


@pytest.mark.ui
def test_create_task(driver):
    """Тест: Создание новой задачи 'Задача 1'"""
    with allure.step("Авторизация и открытие проекта для создания задачи"):
        page = MainPage(driver)

        with allure.step("Кликаем кнопку входа и вводим данные"):
            page.go_to_home
            page.click_login_button()
            email = os.getenv("login")
            password = os.getenv("password")
            page.authorization_username(email)
            page.authorization_password(password)

        with allure.step("Переходим на личную страницу и открываем проект"):
            personal_page = PersonalPage(driver)
            personal_page.open_prod()

        with allure.step("Создаем новую задачу 'Задача 1'"):
            personal_page.create_task()

        with allure.step("Проверяем появление новой задачи на странице"):
            wait = WebDriverWait(driver, 30)
            task_element = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//span[text()='Задача 1']")
                )
            )
            assert task_element is not None, "Не найдена новая доска"


@pytest.mark.ui
def test_del_task(driver):
    """Тест: Удаление задачи 'Задача 1'"""
    with allure.step("Авторизация и удаление задачи 'Задача 1'"):
        page = MainPage(driver)

        with allure.step("Кликаем кнопку входа и вводим данные"):
            page.click_login_button()
            email = os.getenv("login")
            password = os.getenv("password")
            page.authorization_username(email)
            page.authorization_password(password)

        with allure.step("Удаляем задачу 'Задача 1'"):
            personal_page = PersonalPage(driver)
            personal_page.delete_task()

        with allure.step("Проверяем, что задача удалена "
                         "(она исчезла со страницы)"):
            wait = WebDriverWait(driver, 10)
            wait.until(EC.invisibility_of_element_located(
                (By.XPATH, "//span[text()='Задача 1']")
            ))
            assert True, "Задача успешно удалена"
