import allure
from data.data import EXISTING_USER
from data.errors import ERROR_MESSAGES
from helpers.api_requests import get_user_orders

@allure.feature("Заказы пользователя")
@allure.story("Получение заказов пользователя через авторизацию")
class TestUserOrders:

    @allure.title("Получение заказов с авторизацией")
    @allure.description("Проверяет, что авторизованный пользователь может получить список своих заказов.")
    def test_get_orders_with_authorization(self, login_user):
        with allure.step("Авторизуем пользователя"):
            auth_response = login_user(EXISTING_USER)
            assert auth_response.status_code == 200, ERROR_MESSAGES["AUTHORIZATION_ERROR"]
            auth_token = auth_response.json().get("accessToken")
            assert auth_token, ERROR_MESSAGES["MISSING_ACCESS_TOKEN_ERROR"]

            # Проверяем формат токена
            token = auth_token.split(' ')[1] if ' ' in auth_token else auth_token
            assert token, ERROR_MESSAGES["TOKEN_FORMAT_ERROR"]

        with allure.step("Отправляем запрос на получение заказов"):
            response = get_user_orders(token)

        with allure.step("Проверяем успешность получения заказов"):
            assert response.status_code == 200, ERROR_MESSAGES["ORDERS_FETCH_ERROR"].format(
                response_status_code=response.status_code, response=response.text
            )

        with allure.step("Проверяем формат данных о заказах"):
            orders = response.json().get("orders")
            assert isinstance(orders, list), ERROR_MESSAGES["ORDERS_DATA_FORMAT_ERROR"]
            assert len(orders) <= 50, ERROR_MESSAGES["ORDERS_COUNT_ERROR"]
            assert "total" in response.json(), ERROR_MESSAGES["TOTAL_ORDERS_ERROR"]
            assert "totalToday" in response.json(), ERROR_MESSAGES["TOTAL_TODAY_ORDERS_ERROR"]
            assert response.json().get("success") is True, ERROR_MESSAGES["SUCCESS_FLAG_ERROR"]

        with allure.step("Проверяем наличие обязательных полей в каждом заказе"):
            for order in orders:
                assert all(key in order for key in
                           ["ingredients", "status", "number", "createdAt", "updatedAt"]), ERROR_MESSAGES["MISSING_ORDER_FIELDS_ERROR"]

    @allure.title("Ошибка при получении заказов без авторизации")
    @allure.description("Проверяет, что получение заказов без авторизации приводит к ошибке.")
    def test_get_orders_without_authorization(self):
        with allure.step("Отправляем запрос на получение заказов без авторизации"):
            response = get_user_orders()

        with allure.step("Проверяем, что сервер возвращает ошибку авторизации"):
            assert response.status_code == 401, ERROR_MESSAGES["UNAUTHORIZED_STATUS_ERROR"].format(
                response_status_code=response.status_code
            )
            assert response.json().get("message") == ERROR_MESSAGES["UNAUTHORIZED_ERROR_MESSAGE"], \
                f"Неожиданное сообщение: {response.json().get('message')}"
