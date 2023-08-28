# Детальная информация по проекту

## Архитектура проекта:

### Приложение `backend`

- `admin` - Пакет с классами для админ панели. Дополнительно в каждом классе заполнен docstring
    - `product_admin` - Основные классы для админ панели связанные с представлением product
    - `shop_admin` - Основные классы для админ панели связанные с представлением shop
    - `user_admin` - Основные классы для админ панели связанные с представлением user
- `filters` - Пакет с фильтрами для `django-filter`
    - `product_filters` - Фильтры для product views
    - `shop_filters` - Фильтры для shop views
- `models` - Пакет с основными моделями приложения
    - `product_models` - Модели связанные с product
    - `shop_models` - Модели связанные с shop
    - `user_models` - Модели связанные с user
- `permissions` - Пакет с permissions
    - `shop_permissions` - Permissions для view связанных с shop
- `serializers` - Пакет с основными serializers
    - `product_serializers` - serializers связанные с моделями product
    - `shop_serializers` - serializers связанные с моделями shop
    - `user_serializers`  - serializers связанные с моделями user
- `tasks` - Пакет содержащий основные tasks для celery
    - `email_tasks` - Tasks для отправки писем
    - `price_file_tasks` - Tasks для обновления price_file
- `templates` - Основные шаблоны приложения
    - `email_templates` - Html шаблоны для отправки писем
- `utils` - Основные утилиты для приложения
    - `constants` - Константы для приложения
    - `exceptions` - Кастомные exceptions для приложения
    - `managment_utils` - Функции для вызова manage.py команд
    - `price_file_utils` - Утилиты для работы с price_file tasks
    - `product_utils` - Утилиты для product моделей
    - `types` - Кастомные типы
    - `validation` - Валидация
- `views` - Пакет с классами представления
    - `product_views` - Классы представления связанные с моделями product
    - `shop_views` - Классы представления связанные с моделями shop
    - `user_views` - Классы представления связанные с моделями user
- `urls` - Основные routes приложения
- `backup_fixtures` - Папка для хранения временных fixtures при обновлении price_file
- `database` - Папка для хранения базы данных
- `docs` - Документация по проекту
- `main` - Пакет с настройками проекта
- `media` - Папка для хранения всего загруженного содержимого. Именно в ней хранятся загруженные price_file

## Обновление прайс файла

### Необходимый формат прайс файла, для успешного обновления

```yaml
- name: Имя продукта (Обязательное поле)
  description: Описание продукта. (Не обязательное поле)
  categories:
    - Категории продукта (Обязательное поле)
  quantity: Количество продукта (Число, Обязательное поле)
  price: Цена закупа продукта (Число, Обязательное поле)
  price_rrc: РРС продукта (Число, Обязательное поле)
  params: # Не обязательное поле
    - Имя параметра: Значение параметра
```

### Процесс обновления прайс файла

- Происходит загрузка прайс файла
- View проверяет если был до этого прайс файл он его удаляет, если нет то переходит к следующему шагу
- Загружает файл и добавляет его url в модель ShopModel
- Инициирует `update_price_file_task`. *Дальше пойдут действия в `update_price_file_task`*
- В `backup_fixtures` выгружаются fixtures моделей `ProductShopModel` и `ProductParameterModel` конкретного магазина
- Устанавливаются все позиции данного магазина в 0
- Парсится price_file находящийся по пути url в ShopModel
- Валидируются поля price_file. В случае возникновения ошибки будет инициирована задача `send_price_error_update_email`,
  которая отправит email пользователю загрузившему файл
- Дальше по порядку проверяется:
    - Существуют ли категории в price_file, если нет создаем, если да получаем список из объектов модели CategoryModel
    - Получаем объект ProductModel по name. Если такого объекта нет создаем
    - Добавляем в объект ProductModel список из объектов модели CategoryModel
    - Обновляем или создаем объект модели ProductShopModel (через объект модели ShopModel.positions)
    - Удаляем у данного объекта все параметры (модель ProductShopModel)
    - Добавляем к этому объекту параметры из params price_file (Так же проверяется если таких параметров нет, то создаем
      запись)
- В случае успешного обновления файла инициируется задача `send_price_success_updated_email`. Задача отправляет email
  пользователю, с уведомлением об успешном обновлении прайса 