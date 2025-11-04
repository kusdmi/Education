import requests

#Задание №1
# response = requests.get('https://jsonplaceholder.typicode.com/posts')
#
# if response.status_code == 200:
#     posts = response.json()
#
#     for i, post in enumerate(posts[:5], 1):
#         print(f"Пост #{i}")
#         print(f"Заголовок: {post['title']}")
#         print(f"Текст: {post['body']}")
#         print("-" * 50)
# else:
#     print(f"Ошибка при запросе: {response.status_code}")


#Задание №2

# API_KEY = "42fa4d6f05233061ca441d5575d2805a"
#
# city = input("Введите название города: ")
#
# url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru"
#
# response = requests.get(url)
#
# if response.status_code == 200:
#     data = response.json()
#     temp = data['main']['temp']
#     desc = data['weather'][0]['description']
#
#     print(f"\nПогода в {city}:")
#     print(f"Температура: {temp}°C")
#     print(f"Описание: {desc.capitalize()}")
# else:
#     print("Ошибка при получении данных о погоде")

#Задание 3 - 4
# def create_custom_post_with_validation():
#     print("=== Создание нового поста ===")
#
#     try:
#         title = input("Введите заголовок поста: ").strip()
#         body = input("Введите текст поста: ").strip()
#         user_id = input("Введите ID пользователя: ").strip()
#
#         if not title:
#             print("Ошибка: Заголовок не может быть пустым")
#             return
#
#         if not body:
#             print("Ошибка: Текст поста не может быть пустым")
#             return
#
#         try:
#             user_id = int(user_id)
#             if user_id <= 0:
#                 print("Ошибка: ID пользователя должен быть положительным числом")
#                 return
#         except ValueError:
#             print("Ошибка: ID пользователя должен быть числом")
#             return
#
#         url = "https://jsonplaceholder.typicode.com/posts"
#         new_post_data = {
#             "title": title,
#             "body": body,
#             "userId": user_id
#         }
#
#         headers = {
#             "Content-Type": "application/json; charset=UTF-8"
#         }
#
#         response = requests.post(url, json=new_post_data, headers=headers)
#
#         handle_response(response, new_post_data)
#
#     except KeyboardInterrupt:
#         print("\n\n Операция прервана пользователем")
#     except Exception as e:
#         print(f"Неожиданная ошибка: {e}")
#
#
# def handle_response(response, original_data):
#     status_code = response.status_code
#
#     print(f"\nСтатус код: {status_code}")
#
#     if status_code == 201:
#         created_post = response.json()
#         print("Пост успешно создан!")
#         print(f"ID: {created_post['id']}")
#         print(f"Заголовок: {created_post['title']}")
#         print(f"Текст: {created_post['body']}")
#         print(f"ID пользователя: {created_post['userId']}")
#
#     elif status_code == 400:
#         print("Ошибка 400: Неверный запрос")
#         try:
#             error_details = response.json()
#             print(f"Детали: {error_details}")
#         except:
#             print(f"Текст ответа: {response.text}")
#
#     elif status_code == 404:
#         print("Ошибка 404: Ресурс не найден")
#         print("Проверьте правильность URL API")
#
#     elif status_code == 422:
#         print("Ошибка 422: Необрабатываемая сущность")
#         try:
#             validation_errors = response.json()
#             print("Ошибки валидации:")
#             for field, errors in validation_errors.items():
#                 print(f"  {field}: {errors}")
#         except:
#             print(f"Текст ответа: {response.text}")
#
#     elif status_code == 429:
#         print("Ошибка 429: Слишком много запросов")
#         print("Подождите некоторое время перед повторной попыткой")
#
#     elif 500 <= status_code < 600:
#         print(f"Ошибка {status_code}: Проблема на стороне сервера")
#         print("Попробуйте позже или свяжитесь с поддержкой")
#
#     else:
#         print(f"Неизвестный статус код: {status_code}")
#         print(f"Ответ сервера: {response.text}")
#
#
# if __name__ == "__main__":
#     create_custom_post_with_validation()