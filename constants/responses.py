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
