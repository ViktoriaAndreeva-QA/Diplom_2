import random
import string


def generate_random_string(length=8):
    """Генерирует случайную строку"""
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def generate_random_user_data():
    """Генерирует рандомные данные пользователя"""
    return {
        "email": f"{generate_random_string(8)}@email.com",
        "password": generate_random_string(10),
        "name": generate_random_string(8)
    }

def get_login_data(user_data):
    """Возвращает данные для входа из данных пользователя"""
    return {
        "email": user_data["email"],
        "password": user_data["password"]
    }
