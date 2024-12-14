import allure
from data.data import INGREDIENTS, EXISTING_USER
from data.errors import ERROR_MESSAGES
from helpers.api_requests import create_order

@allure.feature("Создание заказа")
@allure.story("Тестирование функционала создания заказа с различными условиями")
class TestOrder:

    @allure.title("Создание заказа с авторизацией")
    @allure.description("Проверяет, что пользователь может создать заказ после успешной авторизации.")
    def test_create_order_with_authorization(self, login_user):
        with allure.step("Авторизуемся в системе"):
            auth_response = login_user(EXISTING_USER)
            assert auth_response.status_code == 200, ERROR_MESSAGES["SUCCESSFUL_LOGIN_ERROR"].format(
                response_status_code=auth_response.status_code, response=auth_response.text
            )
            auth_token = auth_response.json().get("accessToken")
            token = auth_token.split(' ')[1] if ' ' in auth_token else auth_token
            assert token, ERROR_MESSAGES["TOKEN_FORMAT_ERROR"]

        with allure.step("Создаем заказ с авторизацией"):
            order_data = {"ingredients": INGREDIENTS[:2]}
            response = create_order(order_data, token)
            assert response.status_code == 200, ERROR_MESSAGES["ORDERS_FETCH_ERROR"].format(
                response=response.text
            )
            assert response.json().get("success") is True, ERROR_MESSAGES["SUCCESS_FLAG_ERROR"]

    @allure.title("Создание заказа без авторизации")
    @allure.description("Проверяет, что заказ можно создать без авторизации.")
    def test_create_order_without_authorization(self):
        with allure.step("Создаем заказ без авторизации"):
            order_data = {"ingredients": INGREDIENTS[:2]}
            response = create_order(order_data)
            assert response.status_code == 200, ERROR_MESSAGES["ORDERS_FETCH_ERROR"].format(
                response=response.text
            )

    @allure.title("Создание заказа с ингредиентами")
    @allure.description("Проверяет, что заказ можно создать с указанными ингредиентами.")
    def test_create_order_with_ingredients(self):
        with allure.step("Создаем заказ с ингредиентами"):
            order_data = {"ingredients": INGREDIENTS[:2]}
            response = create_order(order_data)
            assert response.status_code == 200, ERROR_MESSAGES["ORDERS_FETCH_ERROR"].format(
                response=response.text
            )
            assert response.json().get("success") is True, ERROR_MESSAGES["SUCCESS_FLAG_ERROR"]

    @allure.title("Ошибка при создании заказа без ингредиентов")
    @allure.description("Проверяет, что при отсутствии ингредиентов в заказе сервер возвращает ошибку.")
    def test_create_order_without_ingredients(self):
        with allure.step("Отправляем запрос на создание заказа без ингредиентов"):
            order_data = {}
            response = create_order(order_data)
            assert response.status_code == 400, ERROR_MESSAGES["ORDERS_BAD_REQUEST_ERROR"].format(
                response_status_code=response.status_code
            )
            assert response.json().get("success") is False, ERROR_MESSAGES["SUCCESS_FLAG_ERROR"]

    @allure.title("Ошибка при создании заказа с неверным хешем ингредиентов")
    @allure.description("Проверяет, что при передаче неверного хеша ингредиентов сервер возвращает ошибку.")
    def test_create_order_with_invalid_ingredient_hash(self):
        with allure.step("Отправляем запрос на создание заказа с неверным хешем ингредиентов"):
            order_data = {"ingredients": ["44445"]}
            response = create_order(order_data)
            assert response.status_code == 500, ERROR_MESSAGES["INVALID_INGREDIENT_ERROR"].format(
                response_status_code=response.status_code
            )
