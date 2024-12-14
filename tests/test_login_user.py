import allure
from helpers.api_requests import login_user
from data.data import EXISTING_USER, INVALID_USER
from data.errors import ERROR_MESSAGES

@allure.feature("Авторизация пользователя")
@allure.story("Проверка успешного и неуспешного входа в систему")
class TestUserAuthentication:

    @allure.title("Успешная авторизация с корректными учетными данными")
    @allure.description("Проверяет возможность входа пользователя с валидными данными и корректный ответ сервера.")
    def test_valid_user_login(self, login_user):
        with allure.step("Отправляем запрос с данными зарегистрированного пользователя"):
            response = login_user(EXISTING_USER)

        with allure.step("Проверяем, что вход выполнен успешно"):
            assert response.status_code == 200, ERROR_MESSAGES["SUCCESSFUL_LOGIN_ERROR"].format(
                response_status_code=response.status_code, response=response.text
            )
            response_json = response.json()
            assert response_json.get("success") is True, ERROR_MESSAGES["SUCCESS_FLAG_ERROR"].format(
                response_json=response_json
            )
            assert "accessToken" in response_json, ERROR_MESSAGES["MISSING_ACCESS_TOKEN_ERROR"]
            assert "refreshToken" in response_json, ERROR_MESSAGES["MISSING_REFRESH_TOKEN_ERROR"]
            assert "user" in response_json, ERROR_MESSAGES["MISSING_USER_DATA_ERROR"]

    @allure.title("Ошибка авторизации при неверных учетных данных")
    @allure.description("Проверяет, что сервер возвращает ошибку при попытке входа с некорректными данными.")
    def test_invalid_user_login(self, login_user):
        with allure.step("Отправляем запрос с неверным email и паролем"):
            response = login_user(INVALID_USER)

        with allure.step("Проверяем, что сервер возвращает ошибку авторизации"):
            assert response.status_code == 401, ERROR_MESSAGES["UNAUTHORIZED_STATUS_ERROR"].format(
                response_status_code=response.status_code
            )
            response_json = response.json()
            assert response_json.get("success") is False, ERROR_MESSAGES["INVALID_LOGIN_SUCCESS_FLAG_ERROR"].format(
                response_json=response_json
            )
            assert response_json.get("message") == "email or password are incorrect", ERROR_MESSAGES["INVALID_LOGIN_MESSAGE_ERROR"].format(
                response_json=response_json
            )
