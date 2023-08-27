## Доступные маршруты:

- **USER:**
    - **POST** - `{domain_name}/api/users/register/` - Регистрация пользователя
    - **POST** - `{domain_name}/api/users/token/` - Получение токена пользователя.
    - **POST** - `{domain_name}/api/users/refresh/` - Обновление токена пользователя.
    - **GET** - `{domain_name}/api/users/profile/` - Информация о пользователе. **Требуется**: Аутентификация
    - **GET**, **POST** - `{domain_name}/api/users/profile/orders/` - Заказы пользователя. Создание заказа. **Требуется
      **:
      Аутентификация
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

## Дополнительная информация:

- ### [Детальная информация по маршрутам](docs/additional_routes_doc.md)
- ### [Детальная информация по env файлу](docs/env_file_doc.md)
- ### [Детальная информация по проекту и файлам](docs/project_doc.md)







