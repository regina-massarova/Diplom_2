import random
import string

def generate_random_string(length):
    """Генерация случайной строки заданной длины."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def generate_user_data(email_suffix="@usertest.com"):
    """
    Генерация данных пользователя.

    :param email_suffix: Суффикс для электронной почты.
    :return: Словарь с email, password и name.
    """
    email = f"{generate_random_string(10)}{email_suffix}"
    password = generate_random_string(12)
    name = generate_random_string(8)
    return {"email": email, "password": password, "name": name}
