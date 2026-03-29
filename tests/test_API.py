import pytest
import requests
import uuid
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

BASE_URL = os.getenv('BASE_URL')
API_LOGIN = os.getenv('API_LOGIN')
API_PASSWORD = os.getenv('API_PASSWORD')


@pytest.fixture(scope='session')
def get_token():
    """Фикстура для получения токена один раз за сессию."""
    # Получаем ID компании
    creds = {
        'login': API_LOGIN,
        'password': API_PASSWORD,
    }
    resp = requests.post(f"{BASE_URL}/api-v2/auth/companies", json=creds)
    assert resp.status_code == 200, "Ошибка при получении компании"
    company_id = resp.json()['content'][0]['id']

    check_creds = {
        'login': API_LOGIN,
        'password': API_PASSWORD,
        'companyId': company_id,
    }
    check_resp = requests.post(
        f"{BASE_URL}/api-v2/auth/keys/get", json=check_creds)

    if check_resp.status_code == 200:
        keys = check_resp.json()
        if keys and len(keys) > 0:
            return keys[0]['key']

    create_resp = requests.post(
        f"{BASE_URL}/api-v2/auth/keys", json=check_creds)
    assert create_resp.status_code == 201, "Не удалось создать API ключ"
    return create_resp.json()['key']


@pytest.fixture
def headers(get_token):
    """Обновляем HEADERS с актуальным токеном."""
    return {
        'Authorization': f'Bearer {get_token}',
        'Content-Type': 'application/json',
    }


def generate_unique_title():
    """Генерирует уникальное название проекта."""
    return f"Test Project {uuid.uuid4()}"


@pytest.fixture
def created_project(headers):
    """Создаёт проект, удаляет после теста."""
    title = generate_unique_title()

    response = requests.post(
        f"{BASE_URL}/api-v2/projects",
        headers=headers,
        json={"title": title}
    )
    assert response.status_code == 201, f"Проект не создан:{response.text}"

    project_id = response.json()['id']

    yield project_id

    requests.put(
        f"{BASE_URL}/api-v2/projects/{project_id}",
        headers=headers,
        json={"deleted": True}
    )


@pytest.mark.api
def test_create_project_positive(created_project, headers):
    """Позитивный тест: создание проекта и проверка его существования."""
    project_id = created_project
    get_response = requests.get(
        f"{BASE_URL}/api-v2/projects/{project_id}",
        headers=headers
    )
    assert get_response.status_code == 200, "Созданный проект не найден"
    data = get_response.json()
    assert 'id' in data, "Ответ не содержит id проекта"


@pytest.mark.api
def test_create_project_negative_empty_body(headers):
    response = requests.post(
        f"{BASE_URL}/api-v2/projects",
        headers=headers,
        json={}  # пустое тело
    )
    assert response.status_code == 400, (
        f"Ожидался код 400, получен {response.status_code}"
    )


@pytest.mark.api
def test_update_project_positive(created_project, headers):
    """Позитивный тест: изменение названия существующего проекта."""
    project_id = created_project
    new_title = f"Updated {generate_unique_title()}"
    response = requests.put(
        f"{BASE_URL}/api-v2/projects/{project_id}",
        headers=headers,
        json={'title': new_title}
    )
    assert response.status_code == 200, (
        f"Ожидался код 200, получен {response.status_code}"
    )

    # Проверим, что изменения применились, выполнив GET
    get_response = requests.get(
        f"{BASE_URL}/api-v2/projects/{project_id}",
        headers=headers
    )
    assert get_response.status_code == 200
    assert get_response.json().get('title') == new_title, "Не обновлено"


@pytest.mark.api
def test_update_project_negative_no_id(headers):
    """Негативный тест: PUT запрос без указания ID (ожидается 404 или 405)."""
    new_title = generate_unique_title()
    response = requests.put(
        f"{BASE_URL}/api-v2/projects/",
        headers=headers,
        json={'title': new_title}
    )
    assert response.status_code in (404, 405), (
        f"Ожидался 404 или 405, получен {response.status_code}"
    )


@pytest.mark.api
def test_get_project_by_id_positive(created_project, headers):
    """Позитивный тест: получение проекта по ID с авторизацией."""
    project_id = created_project
    response = requests.get(
        f"{BASE_URL}/api-v2/projects/{project_id}",
        headers=headers
    )
    assert response.status_code == 200, (
        f"Ожидался код 200, получен {response.status_code}"
    )
    data = response.json()
    assert data['id'] == project_id, "ID проекта не совпадает"
    assert 'title' in data, "Ответ не содержит названия"


@pytest.mark.api
def test_get_project_by_id_negative_no_auth(created_project):
    """Негативный тест: получение проекта без авторизации (ожидается 401)."""
    project_id = created_project
    response = requests.get(
        f"{BASE_URL}/api-v2/projects/{project_id}",
        headers={}  # без токена
    )
    assert response.status_code == 401, (
        f"Ожидался код 401, получен {response.status_code}"
    )
