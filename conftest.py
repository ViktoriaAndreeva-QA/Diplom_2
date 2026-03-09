import pytest
import requests
from constants import BASE_URL, REGISTER_ENDPOINT, USER_ENDPOINT
from helpers import generate_random_user_data


@pytest.fixture
def created_user():
    """
    Создает пользователя перед тестом и удаляет после.
    Возвращает данные пользователя и токен для авторизации.
    """
    # Используем функцию из helpers для генерации данных
    user_data = generate_random_user_data()

    # Создаем пользователя
    response = requests.post(f"{BASE_URL}{REGISTER_ENDPOINT}", json=user_data)
    response_data = response.json()
    access_token = response_data.get("accessToken")
    
    # Возвращаем данные и токен в тест
    yield {
        "data": user_data,
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
