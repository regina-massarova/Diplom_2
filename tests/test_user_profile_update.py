import allure
from helpers.api_requests import login_user, update_user_data, restore_user_data
from data.data import EXISTING_USER
from data.errors import ERROR_MESSAGES

@allure.feature("Обновление профиля пользователя")
@allure.story("Проверка сценариев изменения данных пользователя")
class TestUserProfileUpdate:

    @allure.title("Успешное обновление профиля при авторизации")
    @allure.description("Проверяет, что пользователь может обновить свои данные после успешной авторизации.")
    def test_authorized_user_can_update_profile(self):
        with allure.step("Авторизация пользователя с корректными данными"):
            response = login_user(EXISTING_USER)
            assert response.status_code == 200, ERROR_MESSAGES["SUCCESSFUL_LOGIN_ERROR"].format(
                response_status_code=response.status_code, response=response.text
            )

            access_token = response.json().get("accessToken")
            assert access_token, ERROR_MESSAGES["MISSING_ACCESS_TOKEN_ERROR"]

            token = access_token.split(' ')[1] if ' ' in access_token else access_token

        updated_user_data = {
            "email": EXISTING_USER["email"],
            "name": "Updated Name"
        }

        with allure.step("Запрос на обновление профиля пользователя"):
            response = update_user_data(updated_user_data, token)
            assert response.status_code == 200, ERROR_MESSAGES["USER_PROFILE_UPDATE_ERROR"].format(
                response_status_code=response.status_code, response=response.text
            )
            assert response.json().get("success") is True, ERROR_MESSAGES["SUCCESS_FLAG_ERROR"].format(
                response_json=response.json()
            )
            assert response.json().get("user", {}).get("email") == updated_user_data["email"], \
                ERROR_MESSAGES["EMAIL_UPDATE_ERROR"].format(
                    expected=updated_user_data["email"],
                    actual=response.json().get("user", {}).get("email")
                )
            assert response.json().get("user", {}).get("name") == updated_user_data["name"], \
                ERROR_MESSAGES["NAME_UPDATE_ERROR"].format(
                    expected=updated_user_data["name"],
                    actual=response.json().get("user", {}).get("name")
                )

        with allure.step("Восстановление исходных данных пользователя"):
            restore_user_data(EXISTING_USER["email"], EXISTING_USER)

    @allure.title("Ошибка обновления профиля без авторизации")
    @allure.description("Проверяет, что обновление данных пользователя невозможно без авторизации.")
    def test_update_profile_without_authorization_fails(self):
        updated_user_data = {
            "email": EXISTING_USER["email"],
            "name": "Updated Name"
        }

        with allure.step("Запрос на обновление профиля без предоставления токена авторизации"):
            response = update_user_data(updated_user_data)
            assert response.status_code == 401, ERROR_MESSAGES["UNAUTHORIZED_STATUS_ERROR"].format(
                response_status_code=response.status_code
            )
            assert response.json().get("success") is False, ERROR_MESSAGES["SUCCESS_FLAG_ERROR"].format(
                response_json=response.json()
            )
            assert response.json().get("message") == "You should be authorised", \
                ERROR_MESSAGES["UNAUTHORIZED_ERROR_MESSAGE"].format(response_json=response.json())
