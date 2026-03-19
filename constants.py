# Базовый URL
BASE_URL = "https://stellarburgers.education-services.ru"

# Эндпоинты
REGISTER_ENDPOINT = "/api/auth/register"
LOGIN_ENDPOINT = "/api/auth/login"
USER_ENDPOINT = "/api/auth/user"
CREATE_ORDER_ENDPOINT = "/api/orders"


# ========== УСПЕШНЫЕ ОТВЕТЫ ==========

## Успешное создание пользователя
SUCCESS_CREATED_CODE = 200
SUCCESS_CREATED_RESPONSE = {
    "success": True,
    "user": {
        "email": "",
        "name": ""
    },
    "accessToken": "",
    "refreshToken": ""
}

## Успешная авторизация пользователя
SUCCESS_LOGIN_CODE = 200
SUCCESS_LOGIN_RESPONSE = {
    "success": True,
    "accessToken": "",
    "refreshToken": "",
    "user": {
        "email": "",
        "name": ""
    }
}

## Успешное удаление пользователя
SUCCESS_DELETE_USER_CODE = 202
SUCCESS_DELETE_USER_RESPONSE = {
    "success": True,
    "message": "User successfully removed"
}

## Успешное создание заказа
SUCCESS_CREATE_ORDER_CODE = 200
SUCCESS_CREATE_ORDER_RESPONSE = {
    "success": True,
    "name": "",
    "order": {
        "number": ""
    }
}


# ========== ОШИБКИ ==========

## Ошибка при попытке создания уже существующего пользователя
ERROR_CONFLICT_CODE = 403
ERROR_CONFLICT_RESPONSE = {
    "success": False,
    "message": "User already exists"
}

## Ошибка при попытке создания пользователя без заполнения обязательных полей
ERROR_MISSING_FIELDS_CODE = 403
ERROR_MISSING_FIELDS_RESPONSE = {
    "success": False,
    "message": "Email, password and name are required fields"
}

## Ошибка при попытке авторизоваться под несуществующим (удалённым) пользователем
ERROR_AUTHORIZATION_CODE = 401
ERROR_AUTHORIZATION_RESPONSE = {
    "success": False,
    "message": "email or password are incorrect"
}

## Ошибка при создании заказа с невалидным хешем ингредиента
ERROR_INVALID_HASH_INGREDIENT_CODE = 500
ERROR_INVALID_HASH_RESPONSE_HTML = "Internal Server Error"

## Ошибка при попытке создания заказа без ингредиентов
ERROR_WITHOUT_INGREDIENTS_CODE = 400
ERROR_WITHOUT_INGREDIENTS_RESPONSE = {
    "success": False,
    "message": "Ingredient ids must be provided"
}






# ========== ИНГРЕДИЕНТЫ (ID из API) ==========
INGREDIENTS = {
    # Булки
    "bun_fluorescent": "61c0c5a71d1f82001bdaaa6d",          # Флюоресцентная булка R2-D3
    "bun_crator": "61c0c5a71d1f82001bdaaa6c",               # Краторная булка N-200i
    
    # Начинки
    "filling_mollusk": "61c0c5a71d1f82001bdaaa6f",          # Мясо бессмертных моллюсков
    "filling_meteorite": "61c0c5a71d1f82001bdaaa70",        # Говяжий метеорит
    "filling_fallenian": "61c0c5a71d1f82001bdaaa77",        # Плоды Фалленианского дерева
    
    # Соусы
    "sauce_spicy_x": "61c0c5a71d1f82001bdaaa72",            # Соус Spicy-X
    "sauce_space": "61c0c5a71d1f82001bdaaa73"               # Соус фирменный Space Sauce
}

INVALID_HASH_INGREDIENT = "invalid_hash_12345"
