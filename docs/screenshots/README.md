# Скріншоти до Лабораторної роботи 9

Ця папка призначена для збереження 10 скріншотів HTTP-запитів із Postman / Thunder Client / Insomnia для підтвердження виконання Лабораторної роботи №9.

## Список файлів скріншотів:

1. `01_login_admin.png` — Отримання токена для користувача `admin` (`200 OK`).
2. `02_login_user.png` — Отримання токена для користувача `user` (`200 OK`).
3. `03_hello_admin_with_admin_200.png` — `GET /hello/admin` з токеном `admin` (`200 OK`).
4. `04_hello_admin_with_user_403.png` — `GET /hello/admin` з токеном `user` (`403 Forbidden`).
5. `05_hello_user_with_user_200.png` — `GET /hello/user` з токеном `user` (`200 OK`).
6. `06_hello_user_with_admin_403.png` — `GET /hello/user` з токеном `admin` (`403 Forbidden`).
7. `07_hello_man_with_user_200.png` — `GET /hello/man` з токеном `user` (`200 OK`).
8. `08_hello_man_with_admin_200.png` — `GET /hello/man` з токеном `admin` (`200 OK`).
9. `09_hello_unknown_with_user_200.png` — `GET /hello/unknown` з токеном `user` (`200 OK`).
10. `10_hello_admin_without_token_401.png` — `GET /hello/admin` без Bearer токена (`401 Unauthorized`).
