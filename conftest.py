import pytest
import requests
import random
import string
from constants import BASE_URL, REGISTER_ENDPOINT, USER_ENDPOINT


def generate_random_string(length=8):
    """Генерирует случайную строку"""
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))


@pytest.fixture
def random_user_data():
    """Фикстура с рандомными данными пользователя"""
    return {
        "email": f"{generate_random_string(8)}@email.com",
        "password": generate_random_string(10),
        "name": generate_random_string(8)
    }


@pytest.fixture
def created_user(random_user_data):
    """
    Создает пользователя перед тестом и удаляет после.
    Возвращает данные пользователя и токен для авторизации.
    """
    # Создаем пользователя
    response = requests.post(f"{BASE_URL}{REGISTER_ENDPOINT}", json=random_user_data)
    response_data = response.json()
    access_token = response_data.get("accessToken")
    
    # Возвращаем данные и токен в тест
    yield {
        "data": random_user_data,
        "token": access_token
    }
    
    # Удаляем после теста
    if access_token:
        headers = {"Authorization": access_token}
        requests.delete(f"{BASE_URL}{USER_ENDPOINT}", headers=headers)

@pytest.fixture
def delete_user_after_test():
    """Фикстура только для удаления пользователя после теста"""
    created_tokens = []
    
    def _track(token):
        """Сохраняет токен для последующего удаления"""
        if token:
            created_tokens.append(token)
        return token
    
    yield _track
    
    # Удаляем всех созданных пользователей
    for token in created_tokens:
        headers = {"Authorization": token}
        requests.delete(f"{BASE_URL}{USER_ENDPOINT}", headers=headers)


@pytest.fixture
def login_data():
    """Фикстура для создания данных входа"""
    def _create(user_data):
        return {
            "email": user_data["email"],
            "password": user_data["password"]
        }
    return _create
