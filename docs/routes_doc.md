## Более детально про маршруты:

### **POST** - `{domain_name}/api/users/register/`

Регистрация пользователя. Необходим json объект формата:

```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

#### По полям:

- `username` - Обязательно к заполнению. Поле должно быть уникальное
- `email` - Обязательно к заполнению. Поле должно быть уникальное
- `password` - Обязательно к заполнению. Поле проходит стандартную django password валидацию

#### Формат ответа:

```json
{
  "pk": "integer",
  "username": "string",
  "email": "string",
  "orders": "{domain}/api/users/profile/orders/"
}
```

Поле `orders` - содержит ссылку на страницу заказов пользователя

#### Доступные фильтры:

- `id` - exact по полю id
- `status` - icontains по полю status
- `created_at` - (lte, gte, lt, gt) по полю created_at

#### Дополнительно:

- Поле `username` должно быть уникально в бд
- Поле `email` должно быть уникально в бд
- На поле `password` стоит стандартный django password validator

### **POST** - `{domain_name}/api/users/token/`

Получение токена пользователя. Необходим json объект формата:

```json
{
  "username": "string",
  "password": "string"
}
```

**Важно!**: Для успешного получения токена запись с такими значениями должна существовать в бд

#### Формат ответа:

```json
{
  "refresh": "token",
  "access": "token"
}
```

### **POST** - `{domain_name}/api/users/refresh/`

Обновление токена пользователя. Необходим json объект формата:

```json
{
  "refresh": "token"
}
```

#### По полям

- `refresh` - refresh токен, для получения access токена

#### Формат ответа:

```json
{
  "access": "token"
}
```

### POST `{domain_name}/api/users/password/reset/`

Отправка email для сброса пароля. Необходим json объект формата:

```json
{
  "email": "string"
}
```

##### Информация по полям:

- `email` - email адрес пользователя. На этот email будет сгенерировано письмо с url ссылкой для сброса пароля

#### Формат ответа:

```json
{
  "detail": "Email со ссылкой для сброса пароля было отправлено на указанный email адрес. Ссылка будет активна до: {expire_date}"
}
```

### **POST** - `{domain_name}/api/users/password/update/{username}/{token}`

Сброс пароля пользователя. Необходим json объект формата:

```json
{
  "password": "string"
}
```

##### Информация по полям:

- `password` - Строковое поле. Для поля используется стандартное django password validation

#### Формат ответа:

```json
{
  "id": "integer",
  "username": "string",
  "email": "string"
}
```

##### Информация по полям:

- `id` - Числовое поле. Идентификатор пользователя у которого поменяли пароль
- `username` - Строковое поле. Имя пользователя у которого поменяли пароль
- `email` - Строковое поле. Email пользователя у которого поменяли пароль

### **GET** - `{domain_name}/api/users/profile/`

Информация о пользователе. Для получения информации в `headers` должно быть передано поле `Authorization`. Пример:

```http request
HEAD Authorization: Bearer "Token"
```

#### Формат ответа:

```json
{
  "pk": "integer",
  "username": "string",
  "email": "string",
  "orders": "{domain}/api/users/profile/orders/"
}
```

Поле `orders` - ссылка на страницу с заказами пользователя

### **GET**, **POST** - `{domain_name}/api/users/profile/orders/`

Заказы пользователя. Создание заказа. В Headers необходимо передать токен:

```http request
HEAD Authorization: Bearer "Token"
```

#### Для создания заказа необходим json объект формата:

```json
{
  "address": {
    "postal_code": "integer",
    "country": "string",
    "region": "string",
    "city": "string"
  },
  "order_items": [
    {
      "product": "integer",
      "shop": "integer",
      "quantity": "integer"
    }
  ],
  "additional": ""
}
```

##### Информация по полям:

- `postal_code` - Обязательное числовое поле. Содержит почтовый индекс
- `country` - Обязательное строковое поле. Содержит название страны
- `region` - Обязательное строковое поле. Содержит название региона
- `city` - Обязательное строковое поле. Содержит название города
- `product` - Обязательное числовое поле. Содержит id товара. По полю ведется валидация на существования такого товара в
  бд
- `shop` - Обязательное числовое поле. Содержит id магазина. По полю ведется валидация на существования такого магазина
- `quantity` - Обязательное числовое поле. Количество товара. По полю ведется валидация на количество товара в магазине
- `additional` - Необязательное строковое поле. Дополнительная информация по заказу

Дополнительно по полям `product` и `shop` вместе ведется валидация на существования такой позиции в таком магазине

#### Формат ответа:

```json
{
  "id": "integer",
  "created_at": "string",
  "status": "string",
  "details": "{domain}/api/users/profile/orders/{order_id}/"
}
```

##### Информация по полям:

- `id` - Числовое поле. Содержит id заказа
- `created_at` - Строковое поле. Содержит дату создания заказа
- `status` - Строковое поле. Статус заказа. По умолчанию только созданные заказы имеют статус `Новый`
- `details` - Строковое поле. Содержит ссылку на детальную информацию по заказу

**Важно**: После создания заказа отправляется email на `ADMIN_EMAIL` с уведомлением о новом созданном заказе

#### Формат ответа по GET запросу списка заказов:

```json
 {
  "results": [
    {
      "id": "integer",
      "created_at": "string",
      "status": "string",
      "details": "{domain}/api/users/profile/orders/{order_id}/"
    }
  ]
}
```

##### Информация по полям описана выше

### **GET** - `{domain_name}/api/users/profile/orders/{order_id}/`

Детальная информация по заказу. В Headers необходимо передать токен:

```http request
HEAD Authorization: Bearer "Token"
```

#### Формат ответа:

```json
{
  "id": "integer",
  "created_at": "string",
  "status": "string",
  "address": {
    "postal_code": "integer",
    "country": "string",
    "region": "string",
    "city": "string"
  },
  "additional": "string",
  "items": "{domain}/api/users/profile/orders/{order_id}/items/",
  "total_price": "integer"
}
```

#### Информация по полям:

- `id` - Числовое поле. Содержит id заказа
- `created_at` - Строковое поле. Содержит дату создания заказа
- `status` - Строковое поле. Содержит статус заказа
- `postal_code` - Обязательное числовое поле. Содержит почтовый индекс
- `country` - Строковое поле. Содержит название страны
- `region` - Строковое поле. Содержит название региона
- `city` - Строковое поле. Содержит название города
- `additional` - Строковое поле. Дополнительная информация по заказу
- `items` - Строковое поле. Содержит ссылку на список товаров в заказе
- `total_price` - Итоговая сумма по заказу

### **GET** - `{domain_name}/api/users/profile/orders/{order_id}/items/`

Список товаров в заказе. В Headers необходимо передать токен:

```http request
HEAD Authorization: Bearer "Token"
```

#### Формат ответа:

```json
{
  "results": [
    {
      "position": {
        "product_id": "integer",
        "product_name": "string",
        "shop_id": "integer",
        "shop_name": "string",
        "description": "string",
        "params": [
          {
            "name": "string",
            "value": "string"
          }
        ]
      },
      "quantity": "integer",
      "price": "integer",
      "price_rrc": "integer",
      "sum": "integer"
    }
  ]
}
```

#### Информация по полям:

- `product_id` - Числовое поле. Содержит id товара
- `product_name` - Строковое поле. Содержит имя товара
- `shop_id` - Числовое поле. Содержит id магазина
- `shop_name` - Строковое поле. Содержит имя магазина
- `description` - Строковое поле. Содержит описание товара
- `name` - Строковое поле. Содержит название параметра
- `value` - Строковое поле. Содержит значение параметра
- `quantity` - Числовое поле. Содержит количество товара
- `price` - Числовое поле. Содержит цену товара
- `price_rrc` - Числовое поле. Содержит РРЦ
- `sum` - Числовое поле. Содержит итоговую сумму (quantity * price)

### **GET** - `{domain_name}/api/shops/`

Список магазинов

### Формат ответа

```json
{
  "results": [
    {
      "id": "integer",
      "name": "string",
      "status": "string",
      "detail": "{domain}/api/shops/{shop_slug}/"
    }
  ]
}
```

#### Информация по полям:

- `id` - Числовое поле. Содержит id магазина
- `name` - Строковое поле. Содержит имя магазина
- `status` - Строковое поле. Содержит статус магазина
- `detail` - Строковое поле. Содержит url для детальной информации по магазину

#### Доступные фильтры:

- `name` - icontains по полю name
- `status` - icontains по полю status

### **GET** `{domain_name}/api/shops/{shop_slug}/`

Детальная информация по магазину.

#### Формат ответа:

```json
{
  "id": "integer",
  "name": "string",
  "email": "string",
  "phone": "string",
  "status": "string",
  "price_list": "{domain}/api/shops/{shop_slug}/products/",
  "price_file": "{domain}/media/prices/DNS-25-08-2023_18-21-49-140927.yml",
  "orders": "{domain}/api/shops/{shop_slug}/orders/"
}
```

#### Информация по полям:

- `id` - Числовое поле. Содержит id магазина
- `name` - Строковое поле. Содержит имя магазина
- `email` - Строковое поле. Содержит email адрес магазина
- `phone` - Строковое поле. Содержит телефон магазина
- `status` - Строковое поле. Содержит статус магазина
- `price_list` - Строковое поле. Содержит url адрес с товарами этого магазина
- `price_file` - Строковое поле. Содержит ссылку на последний загруженный прайс файл магазина. **Важно**: Данная поле
  доступно только администратору или менеджеру данного магазина
- `orders` - Строковое поле. Содержит url адрес для просмотра списка заказов данного магазина. **Важно**: Данная поле
  доступно только администратору или менеджеру данного магазина

### **GET** `{domain_name}/api/shops/{shop_slug}/orders/`

Список заказов магазина. В Headers необходимо передать токен:

```http request
HEAD Authorization: Bearer "Token"
```

**Важно**: Пользователь должен быть менеджером магазина или админом

#### Формат ответа:

```json
{
  "results": [
    {
      "id": "integer",
      "created_at": "string",
      "status": "string",
      "details": "{domain}/api/shops/{shop_slug}/orders/{order_id}/"
    }
  ]
}
```

#### Информация по полям:

- `id` - Числовое поле. Содержит id заказа
- `created_at` - Строковое поле. Содержит дату создания заказа
- `status` - Строковое поле. Статус заказа.
- `details` - Строковое поле. Содержит ссылку на детальную информацию по заказу

#### Доступные фильтры:

- `id` - exact по полю id
- `status` - icontains по полю status
- `created_at` - (lte, gte, lt, gt) по полю created_at

### **GET** `{domain_name}/api/shops/{shop_slug}/orders/{order_id}/`

Детальная информация по заказу в магазине. В Headers необходимо передать токен:

```http request
HEAD Authorization: Bearer "Token" 
```

**Важно**: Пользователь должен быть менеджером магазина или админом

#### Формат ответа:

```json
{
  "id": "integer",
  "created_at": "string",
  "status": "string",
  "address": {
    "postal_code": "integer",
    "country": "string",
    "region": "string",
    "city": "string"
  },
  "items": "{domain}/api/shops/{shop_slug}/orders/{order_id}/items/"
}
```

#### Информация по полям:

- `id` - Числовое поле. Содержит id заказа
- `created_at` - Строковое поле. Содержит дату создания заказа
- `status` - Строковое поле. Содержит статус заказа
- `postal_code` - Обязательное числовое поле. Содержит почтовый индекс
- `country` - Строковое поле. Содержит название страны
- `region` - Строковое поле. Содержит название региона
- `city` - Строковое поле. Содержит название города
- `items` - Строковое поле. Содержит ссылку на список товаров в заказе конкретного магазина

### **GET** `{domain_name}/api/shops/{shop_slug}/orders/{order_id}/items/`

Список товаров в заказе из этого магазина. В Headers необходимо передать токен:

```http request
HEAD Authorization: Bearer "Token" 
```

**Важно**: Пользователь должен быть менеджером магазина или админом

#### Формат ответа:

```json
{
  "results": [
    {
      "position": {
        "product_id": "integer",
        "product_name": "string",
        "description": "string",
        "params": [
          {
            "name": "string",
            "value": "string"
          }
        ]
      },
      "quantity": "integer",
      "price": "integer",
      "price_rrc": "integer"
    }
  ]
}
```

#### Информация по полям:

- `product_id` - Числовое поле. Содержит id товара
- `product_name` - Строковое поле. Содержит имя товара
- `description` - Строковое поле. Содержит описание товара
- `name` - Строковое поле. Содержит название параметра
- `value` - Строковое поле. Содержит значение параметра
- `quantity` - Числовое поле. Содержит количество товара
- `price` - Числовое поле. Содержит цену товара
- `price_rrc` - Числовое поле. Содержит РРЦ

### **GET** `{domain_name}/api/shops/{shop_slug}/products/`

Список товаров в магазине

#### Формат ответа

```json
{
  "results": [
    {
      "product_id": "integer",
      "product_name": "string",
      "categories": [
        "string"
      ],
      "shop_id": "integer",
      "shop_name": "string",
      "description": "string",
      "params": [
        {
          "name": "string",
          "value": "string"
        }
      ],
      "quantity": "integer",
      "price": "integer",
      "price_rrc": "integer"
    }
  ]
}
```

#### Информация по полям:

- `product_id` - Числовое поле. Содержит id товара
- `product_name` - Строковое поле. Содержит имя товара
- `categories` - Список строк. Содержит категории товара
- `shop_id` - Числовое поле. Содержит id магазина
- `shop_name` - Строковое поле. Содержит имя магазина
- `description` - Строковое поле. Содержит описание товара
- `name` - Строковое поле. Содержит название параметра
- `value` - Строковое поле. Содержит значение параметра
- `quantity` - Числовое поле. Содержит количество товара в магазине
- `price` - Числовое поле. Содержит цену товара
- `price_rrc` - Числовое поле. Содержит РРЦ

#### Доступные фильтры:

- `product_id` - exact по полю product__pk
- `product_name` - icontains по полю product__name
- `category` - icontains по полю product__categories__name
- `price` - (lte, gte, lt, gt) по полю price
- `price_rrc` - (lte, gte, lt, gt) по полю price_rrc
- `quantity` - (lte, gte, lt, gt) по полю quantity

### **GET** `{domain_name}/media/prices/{price_file_name}/`

Получить последний загруженный price файл с товарами

#### Формат ответа:

- yml файл с товарами из магазина

### **PUT**, **PATCH** `{domain_name}/api/shops/{shop_slug}/status/`

Смена статуса у магазина. В Headers необходимо передать токен:

```http request
HEAD Authorization: Bearer "Token" 
```

**Важно**: Пользователь должен быть менеджером магазина или админом

#### Необходим json объект:

```json
{
  "status": "boolean"
}
```

##### Информация по полям:

- `status` - boolean поле. true - магазин готов принимать заказы, false - не готов принимать заказы

#### Формат ответа:

```json
{
  "status": "boolean"
}
```

#### Дополнительно:

- Валидация поля status. Если у магазина пустое поле price_file, то статус невозможно установить в true

### **PUT**, **PATCH** `{domain_name}/api/shops/{shop_slug}/update/`

Загрузка актуального прайс файла. В Headers необходимо передать токен:

```http request
HEAD Authorization: Bearer "Token" 
```

**Важно**: Пользователь должен быть менеджером магазина или админом

#### Необходим json объект:

```json
{
  "price_file": "file object"
}
```

##### Информация по полям:

- `price_file` - Файловый объект с актуальным прайсом. В случае успешного парсинга файла идет обновление всех товаров
  конкретного магазина. Если же парсинг файла был с ошибками, то загружается backup данных

### **GET** - `{domain_name}/api/products/`

Список доступных для заказа товаров

#### Формат ответа:

```json
{
  "results": [
    {
      "id": "integer",
      "name": "string",
      "categories": [
        "string"
      ],
      "details": "{domain}/api/products/{product_slug}/"
    }
  ]
}
```

##### Информация по полям:

- `id` - Числовое поле. Содержит id товара
- `name` - Строковое поле. Содержит название товара
- `categories` - Список со строками. Содержит категории товара
- `details` - Строковое поле. Содержит url с детальной информацией о товаре

#### Доступные фильтры:

- `cat` - icontains по полю categories__name
- `name` - icontains по полю name

### **GET** - `{domain_name}/api/products/{product_slug}/`

Детальная информация по товару

#### Формат ответа

```json
{
  "results": [
    {
      "product_id": "integer",
      "product_name": "string",
      "categories": [
        "string"
      ],
      "shop_id": "integer",
      "shop_name": "string",
      "description": "string",
      "params": [
        {
          "name": "string",
          "value": "string"
        }
      ],
      "quantity": "integer",
      "price": "integer",
      "price_rrc": "integer"
    }
  ]
}
```

#### Информация по полям:

- `product_id` - Числовое поле. Содержит id товара
- `product_name` - Строковое поле. Содержит имя товара
- `categories` - Список строк. Содержит категории товара
- `shop_id` - Числовое поле. Содержит id магазина
- `shop_name` - Строковое поле. Содержит имя магазина
- `description` - Строковое поле. Содержит описание товара
- `name` - Строковое поле. Содержит название параметра
- `value` - Строковое поле. Содержит значение параметра
- `quantity` - Числовое поле. Содержит количество товара в магазине
- `price` - Числовое поле. Содержит цену товара
- `price_rrc` - Числовое поле. Содержит РРЦ

#### Доступные фильтры:

- `product_id` - exact по полю product__pk
- `product_name` - icontains по полю product__name
- `shop_id` - exact по полю shop__pk
- `shop_name` - icontains по полю shop__name
- `category` - icontains по полю product__categories__name
- `price` - (lte, gte, lt, gt) по полю price
- `price_rrc` - (lte, gte, lt, gt) по полю price_rrc
- `quantity` - (lte, gte, lt, gt) по полю quantity

### **GET** - `{domain_name}/api/schema/`

Получить OpenAPI схему. Количество запросов не ограничено

#### Доступные параметры:

- `format` - `string` - json или yaml
- `lang`  - `string` - язык схемы

#### Формат ответа

- Файл со схемой

### **GET** - `{domain_name}/api/docs/`

Swagger документация по проекту. Количество запросов не ограничено

### **GET** - `{domain_name}/api/oauth/login/{backend}`

Авторизация в проекте через сторонний backend

**ВАЖНО!** Для работы с данными backend, у вас должны быть настроены приложения в этих
провайдерах.
Документация по настройке - [Как настроить oauth](oauth_doc.md)

#### Список доступных backend:

- `github` - Авторизация через github
- `vk` - Авторизация через vk

#### Доступные параметры:

- `next` - Url страницы, на которую произойдет redirect после успешной авторизации

#### Формат ответа:

- Если у запроса не был заполен параметр `next` - то будет осуществлен redirect на
  страницу `{domain_name}/api/users/profile`
- Если у запроса был заполнен параметр `next`, то происходит проверка:
    - Если `next` ведет на сторонний url и включен `SOCIAL_AUTH_SANITIZE_REDIRECTS` и `next` есть
      в `SOCIAL_AUTH_ALLOWED_REDIRECT_HOSTS` - то произойдет
      redirect на этот url + дополнительно в качестве параметров будет сгенерирован `refresh` и `access` токены, т.е.
      redirect - `next?refresh=token&access=token`
    - Если `next` ведет на сторонний url и параметры `SOCIAL_AUTH_SANITIZE_REDIRECTS`
      и `SOCIAL_AUTH_ALLOWED_REDIRECT_HOSTS` не заполнены, то redirect будет осуществлен
      на `{domain_name}/api/users/profile`
    - Если `next` не ведет на сторонний url, то redirect - `next?refresh=token&access=token`














