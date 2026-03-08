import pytest
import requests
import allure
from constants import (
    BASE_URL, CREATE_ORDER_ENDPOINT,
    INGREDIENTS, INVALID_HASH_INGREDIENT,
    SUCCESS_CREATE_ORDER_CODE,
    ERROR_WITHOUT_INGREDIENTS_CODE, ERROR_WITHOUT_INGREDIENTS_RESPONSE,
    ERROR_INVALID_HASH_INGREDIENT_CODE
)

@allure.feature('Создание заказа')
class TestCreateOrder:
    """Тесты для создания заказа"""


    @allure.title('Успешное создание заказа с авторизацией')
    @allure.description('Проверка создания заказа авторизованным пользователем с корректными ингредиентами')
    def test_create_order_with_auth_and_ingredients_success(self, created_user):
        """Успешное создание заказа с ингредиентами для авторизованного пользователя"""
        with allure.step('Подготовка данных заказа и заголовков с токеном'):
            headers = {"Authorization": created_user["token"]}
            order_data = {'ingredients': [
                INGREDIENTS["bun_fluorescent"],
                INGREDIENTS["filling_mollusk"],
                INGREDIENTS["sauce_space"]
                ]}

        with allure.step('Отправка POST запроса на /api/orders с авторизацией'):
            response = requests.post(f"{BASE_URL}{CREATE_ORDER_ENDPOINT}", json=order_data, headers=headers)

        with allure.step('Проверка успешного создания заказа'):
            assert response.status_code == SUCCESS_CREATE_ORDER_CODE
            assert response.json()["success"] is True

    @allure.title('Успешное создание заказа с разными наборами ингредиентов')
    @allure.description('Параметризованная проверка создания заказа с различными комбинациями ингредиентов')
    @pytest.mark.parametrize("ingredients", [
        ["61c0c5a71d1f82001bdaaa70"],
        [INGREDIENTS["bun_fluorescent"]],
        [INGREDIENTS["sauce_spicy_x"]],
        [INGREDIENTS["bun_fluorescent"], INGREDIENTS["filling_mollusk"]],
        [INGREDIENTS["bun_crator"], INGREDIENTS["bun_fluorescent"]],
        [INGREDIENTS["bun_fluorescent"], INGREDIENTS["bun_fluorescent"]]
    ])
    def test_create_order_with_different_ingredient_sets_success(self, created_user, ingredients):
        """Параметризованный тест: успешное создание заказа с разными наборами ингредиентов"""
        with allure.step(f'Подготовка данных заказа'):
            headers = {"Authorization": created_user["token"]}
            order_data = {"ingredients": ingredients}
    
        with allure.step('Отправка POST запроса'):
            response = requests.post(f"{BASE_URL}{CREATE_ORDER_ENDPOINT}", json=order_data, headers=headers)
    
        with allure.step('Проверка успешного создания заказа'):
            assert response.status_code == SUCCESS_CREATE_ORDER_CODE
            assert response.json()["success"] is True

    @allure.title('Успешное создание заказа с двойными порциями')
    @allure.description('Проверка создания заказа с булочкой и двойными порциями начинки и соуса')
    def test_create_order_with_bun_double_filling_and_double_sauce_success(self, created_user):
        """Успешное создание заказа с булочкой и двойными порциями начинки и соуса"""
        with allure.step('Подготовка данных заказа с двойными порциями'):
            headers = {"Authorization": created_user["token"]}
            order_data = {'ingredients': [
                INGREDIENTS["bun_fluorescent"],
                INGREDIENTS["filling_fallenian"],
                INGREDIENTS["filling_fallenian"],
                INGREDIENTS["sauce_spicy_x"],
                INGREDIENTS["sauce_spicy_x"]
                ]}

        with allure.step('Отправка POST запроса'):
            response = requests.post(f"{BASE_URL}{CREATE_ORDER_ENDPOINT}", json=order_data, headers=headers)

        with allure.step('Проверка успешного создания заказа'):
            assert response.status_code == SUCCESS_CREATE_ORDER_CODE
            assert response.json()["success"] is True

    @allure.title('Ошибка при создании заказа без авторизации')
    @allure.description('Проверка, что нельзя создать заказа неавторизованному пользователю')
    @pytest.mark.xfail(
    reason="Баг API: возвращает 200 вместо 401",
    strict=True
    )
    def test_create_order_without_auth_raises_error(self):
        """Ошибка при создании заказа для НЕавторизованного пользователя"""
        with allure.step('Подготовка данных заказа'):
            order_data = {'ingredients': [
                INGREDIENTS["bun_crator"],
                INGREDIENTS["filling_meteorite"],
                INGREDIENTS["sauce_spicy_x"]
                ]}

        with allure.step('Отправка POST запроса на /api/orders без авторизации'):
            response = requests.post(f"{BASE_URL}{CREATE_ORDER_ENDPOINT}", json=order_data)

        with allure.step('Проверка, что API требует авторизацию'):
            assert response.status_code == 401
            assert response.json()["success"] is False

    @allure.title('Ошибка при создании заказа без ингредиентов')
    @allure.description('Проверка, что нельзя создать заказ с пустым списком ингредиентов')
    def test_create_order_without_ingredients_raises_error(self, created_user):
        """Ошибка при попытке создания заказа без ингредиентов"""
        with allure.step('Подготовка данных заказа с пустым списком ингредиентов'):
            headers = {"Authorization": created_user["token"]}
            order_data = {'ingredients': []}

        with allure.step('Отправка POST запроса'):
            response = requests.post(f"{BASE_URL}{CREATE_ORDER_ENDPOINT}", json=order_data, headers=headers)

        with allure.step('Проверка ошибки 400 Bad Request'):
            assert response.status_code == ERROR_WITHOUT_INGREDIENTS_CODE
            assert response.json()["success"] is False
            assert response.json()["message"] == ERROR_WITHOUT_INGREDIENTS_RESPONSE["message"]

    @allure.title('Ошибка при создании заказа с невалидным хешем')
    @allure.description('Проверка, что сервер возвращает 500 при передаче неверного ID ингредиента')
    @pytest.mark.parametrize("invalid_ingredients", [
        [INVALID_HASH_INGREDIENT],
        [INGREDIENTS["bun_fluorescent"], INVALID_HASH_INGREDIENT]
    ])
    def test_create_order_with_invalid_ingredient_hash_raises_error(self, created_user, invalid_ingredients):
        """Ошибка 500 при попытке создания заказа с невалидным хешем ингредиента"""
        with allure.step(f'Подготовка данных с невалидным хешем'):
            headers = {"Authorization": created_user["token"]}
            order_data = {'ingredients': invalid_ingredients}

        with allure.step('Отправка POST запроса'):
            response = requests.post(f"{BASE_URL}{CREATE_ORDER_ENDPOINT}", json=order_data, headers=headers)

        with allure.step('Проверка ошибки 500 Internal Server Error'):
            assert response.status_code == ERROR_INVALID_HASH_INGREDIENT_CODE
            assert "text/html" in response.headers["Content-Type"]
            assert "Internal Server Error" in response.text
