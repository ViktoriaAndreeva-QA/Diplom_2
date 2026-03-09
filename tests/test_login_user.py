import pytest
import requests
import allure
from constants import (
    BASE_URL, LOGIN_ENDPOINT,
    SUCCESS_LOGIN_CODE,
    ERROR_AUTHORIZATION_CODE, ERROR_AUTHORIZATION_RESPONSE
    )
from helpers import generate_random_user_data, get_login_data

@allure.feature('Авторизация пользователя')
class TestLoginUser:
    """Тесты для входа пользователя"""


    @allure.title('Успешный вход под существующим пользователем')
    @allure.description('Проверка, что зарегистрированный пользователь может войти в систему')
    def test_login_user_an_existing_user_success(self, created_user):
        """Успешный вход под существующим пользователем"""
        with allure.step('Подготовка данных для входа'):
            data = get_login_data(created_user["data"])
            allure.attach(f"Email: {data['email']}", name="Данные для входа", attachment_type=allure.attachment_type.TEXT)

        with allure.step('Отправка POST запроса на /api/auth/login'):
            response = requests.post(f"{BASE_URL}{LOGIN_ENDPOINT}", json=data)

        with allure.step('Проверка успешного входа'):
            assert response.status_code == SUCCESS_LOGIN_CODE
            assert response.json()["success"] is True

    @allure.title('Ошибка при входе с неверными данными')
    @allure.description('Проверка, что нельзя войти с неправильным email или паролем')
    @pytest.mark.parametrize("field", ["email", "password"])
    def test_login_user_with_wrong_credentials_raises_error(self, created_user, field):
        """Возникает ошибка при попытке входа с неверными данными пользователя"""
        with allure.step(f'Подготовка данных с неверным полем: {field}'):
            data = get_login_data(created_user["data"])
            data[field] = data[field][:-1]

        with allure.step('Отправка POST запроса с неверными данными'):
            response = requests.post(f"{BASE_URL}{LOGIN_ENDPOINT}", json=data)

        with allure.step('Проверка ошибки авторизации'):
            assert response.status_code == ERROR_AUTHORIZATION_CODE
            assert response.json()["success"] is False
            assert response.json()["message"] == ERROR_AUTHORIZATION_RESPONSE["message"]

    @allure.title('Ошибка при входе под несуществующим пользователем')
    @allure.description('Проверка, что нельзя войти с данными незарегистрированного пользователя')
    def test_login_user_nonexistent_user_raises_error(self):
        """Возникает ошибка при попытке входа под несуществующим пользователем"""
        with allure.step('Подготовка данных несуществующего пользователя'):
            user_data = generate_random_user_data()
            data = get_login_data(user_data)

        with allure.step('Отправка POST запроса с данными несуществующего пользователя'):
            response = requests.post(f"{BASE_URL}{LOGIN_ENDPOINT}", json=data)

        with allure.step('Проверка ошибки авторизации'):
            assert response.status_code == ERROR_AUTHORIZATION_CODE
            assert response.json()["success"] is False
            assert response.json()["message"] == ERROR_AUTHORIZATION_RESPONSE["message"]

    @allure.title('Ошибка при входе с пустым полем')
    @allure.description('Проверка, что нельзя войти, если email или password пустые')
    @pytest.mark.parametrize("field", ["email", "password"])
    def test_login_user_with_empty_field_raises_error(self, field):
        """Возникает ошибка при попытке входа с пустым полем"""
        with allure.step(f'Подготовка данных с пустым полем: {field}'):
            user_data = generate_random_user_data()
            data = get_login_data(user_data)
            data[field] = ""

        with allure.step('Отправка POST запроса с пустым полем'):
            response = requests.post(f"{BASE_URL}{LOGIN_ENDPOINT}", json=data)

        with allure.step('Проверка ошибки авторизации'):
            assert response.status_code == ERROR_AUTHORIZATION_CODE
            assert response.json()["success"] is False
            assert response.json()["message"] == ERROR_AUTHORIZATION_RESPONSE["message"]
