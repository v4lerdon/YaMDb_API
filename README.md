# Проект api_yamdb

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Title). Произведения делятся на категории: "Книги", "Фильмы", "Музыка". Список категорий (Category) может быть расширен.
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

## Разработчики
1 Разработчик - Басков Михаил (baem-festa@yandex.ru)

2 Разработчик - Юрченко Валерий (valerayurchenko14@yandex.ru) - Тимлид

3 Разработчик - Grigory Plakhotnikov (ru-grigoriy@yandex.ru)

### Примеры эндпоинтов:

Регистрация нового пользователя
Получить код подтверждения на переданный email.
Права доступа: Доступно без токена.

```
http://127.0.0.1:8000/api/v1/auth/signup/
```

Получение JWT-токена
Получение JWT-токена в обмен на username и confirmation code.
Права доступа: Доступно без токена.

```
http://127.0.0.1:8000/api/v1/auth/signup/
```

Получение списка всех категорий
Получить список всех категорий
Права доступа: Доступно без токена

```
http://127.0.0.1:8000/api/v1/categories/
```

Добавление новой категории
Создать категорию.
Права доступа: Администратор.

```
http://127.0.0.1:8000/api/v1/categories/
```

Удаление категории
Удалить категорию.
Права доступа: Администратор.

```
http://127.0.0.1:8000/api/v1/categories/{slug}/
```

Подробнее можно посмотреть в документации Redoc после старта сервера по адресу:

```
http://127.0.0.1:8000/redoc/
```

### Как запустить проект:

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
