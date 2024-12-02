import requests
import allure
from data.data import ENDPOINTS

@allure.step("Отправка запроса на регистрацию нового пользователя с данными {user_data}")
def register_user(user_data):
    response = requests.post(ENDPOINTS["register_user"], json=user_data)
    return response

@allure.step("Запрос на получение access токена для пользователя с email {email} и паролем {password}")
def get_access_token(email, password):
    response = requests.post(ENDPOINTS["login_user"], json={
        "email": email,
        "password": password,
    })
    return response.json().get("accessToken")

@allure.step("Авторизация пользователя с данными {user_data}")
def login_user(user_data):
    response = requests.post(ENDPOINTS["login_user"], json=user_data)
    return response

@allure.step("Восстановление данных пользователя {email} до исходного состояния")
def restore_user_data(email, original_data):
    response = requests.patch(ENDPOINTS["user_data"], json=original_data)
    if response.status_code == 200:
        print(f"User {email} data restored successfully.")
    else:
        print(f"Failed to restore user data for {email}. Response: {response.text}")

@allure.step("Удаление пользователя {email} с паролем {password}")
def delete_user(email, password):
    access_token = get_access_token(email, password)
    response = requests.delete(ENDPOINTS["user_data"], headers={"Authorization": f"Bearer {access_token}"})
    if response.status_code == 200:
        print(f"User {email} deleted successfully.")
    else:
        print(f"Failed to delete user {email}. Response: {response.text}")

@allure.step("Запрос на получение заказов пользователя с токеном {token}")
def get_user_orders(token=None):
    headers = {}
    if token:
        headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(ENDPOINTS["get_orders"], headers=headers)
    return response

@allure.step("Создание заказа с данными {order_data} для пользователя с токеном {token}")
def create_order(order_data, token=None):
    headers = {}
    if token:
        headers = {"Authorization": f"Bearer {token}"}

    response = requests.post(ENDPOINTS["get_orders"], json=order_data, headers=headers)
    return response

@allure.step("Запрос на получение данных пользователя с токеном {token}")
def get_user_data(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(ENDPOINTS["user_data"], headers=headers)
    return response

@allure.step("Запрос на обновление данных пользователя с новыми данными {user_data} и токеном {token}")
def update_user_data(user_data, token=None):
    headers = {}
    if token:
        headers = {"Authorization": f"Bearer {token}"}
    response = requests.patch(ENDPOINTS["user_data"], json=user_data, headers=headers)
    return response
