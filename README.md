# О проекте

Проект для автоматизации закупок у поставщиков.
Доступные функции:

- Функции работы с пользователем:
    - Регистрация пользователя
    - Получение токена пользователем
    - Обновление токена пользователя
    - Сброс пароля пользователя
    - Назначение пользователя в качестве менеджера магазина (Через админ панель)
    - Просмотр профиль авторизованного пользователя
    - Просмотр заказов авторизованного пользователя
    - Создание заказа из разных магазинов
- Функции работы с товарами:
    - Просмотр списка товаров
    - Просмотр детальной информации по товару (наличие в магазине, описание, параметры...)
- Функции работы с магазинами:
    - Просмотр списка магазинов
    - Просмотр детальной информации по магазину
    - Просмотр списка товаров в конкретном магазине
- Функции доступные менеджеру магазина или админу:
    - Просмотр списка заказов магазина
    - Просмотр детальной информации о заказе в магазине
    - Просмотр списка товаров в заказе магазина (Отображает только товары заказанные в этом магазине)
    - Просмотр последнего загруженного прайс файла магазина
    - Изменение статуса магазина (Готов принимать заказ или нет)
    - Загрузка и обновление прайс файла магазина
- Дополнительные функции
    - При изменении статуса заказа, отправляется email пользователю сделавший заказ
    - При загрузке прайс файла, отправляется email менеджеру загрузивший прайс файл (2 вида уведомления - Успешное
      обновление и произошла ошибка при обновлении)
    - При создании нового заказа, отправляется email администратору с уведомлением о новом заказе
    - Отправка email пользователю с уникальным токеном для сброса пароля
    - Функциональная админ панель

## Доступные маршруты:

- **USER:**
    - **POST** - `{domain_name}/api/users/register/` - Регистрация пользователя
    - **POST** - `{domain_name}/api/users/token/` - Получение токена пользователя.
    - **POST** - `{domain_name}/api/users/refresh/` - Обновление токена пользователя.
    - **POST** - `{domain_name}/api/users/password/reset/` - Отправка email для сброса пароля.
    - **PATCH** - `{domain_name}/api/users/password/update/{username}/{token}` - Сброс пароля пользователя.
    - **GET** - `{domain_name}/api/users/profile/` - Информация о пользователе. **Требуется**: Аутентификация
    - **GET**, **POST** - `{domain_name}/api/users/profile/orders/` - Заказы пользователя. Создание заказа.
      **Требуется**: Аутентификация
    - **GET** - `{domain_name}/api/users/profile/orders/{order_id}/` - Детальная информация по заказу. **Требуется**:
      Аутентификация
    - **GET** - `{domain_name}/api/users/profile/orders/{order_id}/items/` - Список товаров в заказе. **Требуется**:
      Аутентификация
- **SHOP:**
    - **GET** - `{domain_name}/api/shops/` - Список магазинов
    - **GET** `{domain_name}/api/shops/{shop_slug}/` - Детальная информация по магазину
    - **GET** `{domain_name}/api/shops/{shop_slug}/orders/` - Список заказов магазина. **Требуется**: Аутентификация
    - **GET** `{domain_name}/api/shops/{shop_slug}/orders/{order_id}/` - Детальная информация по заказу в магазине. *
      *Требуется**: Аутентификация
    - **GET** `{domain_name}/api/shops/{shop_slug}/orders/{order_id}/items/` - Список товаров в заказе из этого
      магазина. **Требуется**: Аутентификация
    - **GET** `{domain_name}/api/shops/{shop_slug}/products/` - Список товаров в магазине
    - **GET** `{domain_name}/media/prices/{price_file_name}/` - Получить последний загруженный price файл с товарами
    - **PUT**, **PATCH** `{domain_name}/api/shops/{shop_slug}/status/` - Смена статуса у магазина. **Требуется**:
      Аутентификация
    - **PUT**, **PATCH** `{domain_name}/api/shops/{shop_slug}/update/` - Загрузка актуального прайс файла.
      **Требуется**:Аутентификация
- **PRODUCTS:**
    - **GET** - `{domain_name}/api/products/` - Список доступных для заказа товаров
    - **GET** - `{domain_name}/api/products/{product_slug}/` - Детальная информация по товару
- **OAUTH:**
    - **GET** - `{domain_name}/api/oauth/login/{backend}` - Авторизация через backend. Доступные backend - github,
      vk-oauth2
- **DOCS:**
    - **GET** - `{domain_name}/api/schema` - Получить OpenAPI схему
    - **GET** - `{domain_name}/api/docs` - Swagger документация на основе OpenAPI схемы

## Запуск проекта

- ### Через `docker-compose.yml`.
    - Запускаем все сервисы командой `docker-compose up`
- ### Через `docker-compose-only-bd.yml`
    - Запускаем базы данных (postgres, redis) через docker-compose
    - Делаем миграции **Django** - `python manage.py migrate`
    - Запускаем **Django** - `python manage.py runserver`
    - Запускаем **Celery** - `celery -A main worker -l info`
    - Обратите внимание! Доступ к базам данных осуществляется через `localhost`, а не через наименование сервиса

## Запуск тестов

**Важно!** Для запуска тестов необходим запуск `celery`, его можно запустить посредством `docker-compose.yml`, либо
вручную `celery -A main worker -l info`

- Для запуска тестов используется
  команда `pytest` [Документация по pytest](https://docs.pytest.org/en/latest/contents.html)

## Дополнительная информация:

- ### [Детальная информация по маршрутам](docs/routes_doc.md)
- ### [Детальная информация по env файлу](docs/env_file_doc.md)
- ### [Детальная информация по проекту](docs/project_doc.md)







