import pytest
import requests
import allure
from constants import (
    BASE_URL, REGISTER_ENDPOINT, 
    SUCCESS_CREATED_CODE,
    ERROR_MISSING_FIELDS_CODE, ERROR_MISSING_FIELDS_RESPONSE,
    ERROR_CONFLICT_CODE, ERROR_CONFLICT_RESPONSE
    )
from helpers import generate_random_string, generate_random_user_data


@allure.feature('Создание пользователя')
class TestCreateUser:
    """Тесты для создания пользователя"""


    @allure.title('Успешное создание пользователя')
    @allure.description('Проверка создания пользователя со всеми обязательными полями')
    def test_create_user_with_all_fields_success(self, delete_user_after_test):
        """Успешное создание пользователя с заполнением всех полей"""
        user_data = generate_random_user_data()

        with allure.step('Отправка POST запроса на регистрацию пользователя'):
            response = requests.post(f"{BASE_URL}{REGISTER_ENDPOINT}", json=user_data)

        with allure.step('Получение токена и сохранение для удаления'):
            token = response.json().get("accessToken")
            delete_user_after_test(token)

        with allure.step('Проверка статус кода и ответа'):
            assert response.status_code == SUCCESS_CREATED_CODE
            assert response.json()["success"] is True
            assert token is not None

    @allure.title('Ошибка при создании существующего пользователя')
    @allure.description('Проверка, что нельзя создать пользователя с уже зарегистрированными данными')
    def test_create_user_already_exists_user_raises_error(self, created_user):
        """Ошибка при попытке создать уже существующего пользователя"""
        with allure.step('Отправка POST запроса на регистрацию существующего пользователя'):
            response = requests.post(f"{BASE_URL}{REGISTER_ENDPOINT}", json=created_user["data"])
    
        with allure.step('Проверка ошибки 403 Conflict'):
            assert response.status_code == ERROR_CONFLICT_CODE
            assert response.json()["success"] is False
            assert response.json()["message"] == ERROR_CONFLICT_RESPONSE["message"]

    @allure.title('Ошибка при отсутствии обязательного поля')
    @allure.description('Проверка, что нельзя создать пользователя без email, password или name')
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_with_missing_required_field_raises_error(self, missing_field):
        """Ошибка при попытке создания пользователя без заполнения обязательного поля"""
        with allure.step(f'Генерация данных без поля {missing_field}'):
            user_data = {
                "email": f"{generate_random_string(8)}@email.com",
                "password": generate_random_string(10),
                "name": generate_random_string(8)
            }

        del user_data[missing_field]

        with allure.step(f'Отправка POST запроса на регистрацию без поля {missing_field}'):
            response = requests.post(f"{BASE_URL}{REGISTER_ENDPOINT}", json=user_data)

        with allure.step('Проверка ошибки 400 Bad Request'):
            assert response.status_code == ERROR_MISSING_FIELDS_CODE
            assert response.json()["success"] is False
            assert response.json()["message"] == ERROR_MISSING_FIELDS_RESPONSE["message"]
