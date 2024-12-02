BASE_URL = "https://stellarburgers.nomoreparties.site/api"

ENDPOINTS = {
    "register_user": f"{BASE_URL}/auth/register",
    "login_user": f"{BASE_URL}/auth/login",
    "logout_user": f"{BASE_URL}/auth/logout",
    "token": f"{BASE_URL}/auth/token",
    "user_data": f"{BASE_URL}/auth/user",
    "get_orders": f"{BASE_URL}/orders"
}

EXISTING_USER = {
    "email": "rmassarova@mail.ru",
    "password": "EaHbyZmUF2g5S",
    "name": "Регина_Массарова"
}

MISSING_FIELDS_USER = {
    "email": "no_fields_user@burger.com",
    "password": "",
    "name": "Без_Данных"
}

INVALID_USER = {
    "email": "unknown_user@burger.com",
    "password": "wrong_secret"
}

INGREDIENTS = [
    "61c0c5a71d1f82001bdaaa6d",  # Флюоресцентная булка R2-D3
    "61c0c5a71d1f82001bdaaa70",  # Говяжий метеорит (отбивная)
    "61c0c5a71d1f82001bdaaa71",  # Биокотлета из марсианской Магнолии
    "61c0c5a71d1f82001bdaaa6f",  # Мясо бессмертных моллюсков Protostomia
]

