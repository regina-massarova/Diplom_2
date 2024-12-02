import allure
from helpers.api_requests import login_user, get_user_data, register_user
from data.data import EXISTING_USER, MISSING_FIELDS_USER
from data.errors import ERROR_MESSAGES

@allure.feature("Управление учетными записями пользователей")
@allure.story("Проверка сценариев создания и авторизации пользователей")
class TestUserManagement:

    @allure.title("Проверка регистрации нового уникального пользователя")
    @allure.description("Регистрация нового пользователя, авторизация и проверка его данных в системе")
    def test_register_unique_user(self, setup_unique_user):
        user_data = setup_unique_user
        auth_response = login_user(user_data)

        assert auth_response.status_code == 200, ERROR_MESSAGES["SUCCESSFUL_LOGIN_ERROR"].format(
            response=auth_response
        )

        auth_token = auth_response.json().get("accessToken")
        token = auth_token.split(' ')[1] if ' ' in auth_token else auth_token
        assert token, ERROR_MESSAGES["TOKEN_MISSING_ERROR"]

        response = get_user_data(token)

        assert response.status_code == 200, ERROR_MESSAGES["SUCCESSFUL_LOGIN_ERROR"].format(
            response=response
        )

        assert response.json().get("user", {}).get("email") == user_data["email"], \
            f"Электронная почта не совпадает: ожидалось {user_data['email']}, получено {response.json().get('user', {}).get('email')}"

    @allure.title("Проверка повторной регистрации существующего пользователя")
    @allure.description("Попытка зарегистрировать уже существующего пользователя должна возвращать ошибку")
    def test_register_existing_user(self):
        response = register_user(EXISTING_USER)

        assert response.status_code == 403, ERROR_MESSAGES["SUCCESSFUL_LOGIN_ERROR"].format(
            response=response
        )

        response_json = response.json()
        assert response_json["success"] is False, "Флаг 'success' должен быть False"
        assert response_json["message"] == "User already exists", \
            f"Неверное сообщение об ошибке. Ожидалось: 'User already exists', получено: {response_json.get('message')}"

    @allure.title("Проверка регистрации пользователя с пропущенными обязательными полями")
    @allure.description("Регистрация пользователя без обязательных данных должна завершаться ошибкой")
    def test_register_user_missing_fields(self):
        incomplete_user = MISSING_FIELDS_USER.copy()
        incomplete_user["password"] = ""  # Убираем обязательное поле
        response = register_user(incomplete_user)

        assert response.status_code == 403, ERROR_MESSAGES["SUCCESSFUL_LOGIN_ERROR"].format(
            response=response
        )
        expected_response = {
            "success": False,
            "message": ERROR_MESSAGES["MISSING_FIELD_ERROR"]
        }
        assert response.json() == expected_response, \
            f"Ответ API не соответствует ожиданиям. Ожидалось: {expected_response}, получено: {response.json()}"
