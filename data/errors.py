ERROR_MESSAGES = {
    'AUTHORIZATION_ERROR': "Ошибка при авторизации",
    'SUCCESSFUL_LOGIN_ERROR': "Ожидался HTTP-код 200, но сервер вернул {response.status_code}. Ответ: {response.text}",
    'INVALID_LOGIN_ERROR': "Ожидался HTTP-код 401, но сервер вернул {response.status_code}. Ответ: {response.text}",
    'INVALID_LOGIN_SUCCESS_FLAG_ERROR': "Параметр 'success' должен быть False, но получено: {response_json.get('success')}",
    'INVALID_LOGIN_MESSAGE_ERROR': "Ожидалось сообщение 'email or password are incorrect', но получено: {response_json.get('message')}",
    'TOKEN_MISSING_ERROR': "Токен отсутствует",
    'TOKEN_FORMAT_ERROR': "Токен имеет неверный формат или отсутствует",
    'ORDERS_FETCH_ERROR': "Ошибка при получении заказов",
    'ORDERS_DATA_FORMAT_ERROR': "Данные о заказах не являются списком",
    'ORDERS_COUNT_ERROR': "Возвращено больше 50 заказов",
    'TOTAL_ORDERS_ERROR': "Общее количество заказов не возвращено",
    'TOTAL_TODAY_ORDERS_ERROR': "Общее количество заказов за сегодня не возвращено",
    'SUCCESS_FLAG_ERROR': "Флаг успеха равен False",
    'MISSING_ORDER_FIELDS_ERROR': "Отсутствуют поля заказа",
    'UNAUTHORIZED_ERROR_MESSAGE': "You should be authorised",
    'UNAUTHORIZED_STATUS_ERROR': "Ожидался статус 401 (неавторизован), получен {response.status_code}",
    'MISSING_ACCESS_TOKEN_ERROR': "Ответ должен содержать 'accessToken', но он отсутствует.",
    'MISSING_REFRESH_TOKEN_ERROR': "Ответ должен содержать 'refreshToken', но он отсутствует.",
    'MISSING_USER_DATA_ERROR': "Данные пользователя ('user') отсутствуют в ответе.",
    'DUPLICATE_LOGIN_ERROR': "Пользователь уже существует",
    'MISSING_FIELD_ERROR': "Email, password and name are required fields"
}
