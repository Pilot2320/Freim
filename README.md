# Сервис учета ошибок программного продукта

Консольное приложение для регистрации, поиска и обработки ошибок программного продукта было переведено в веб-приложение на Django в рамках практической работы ПР5. Сохраняется предметная область, созданная в ПР3: ошибки, пользователи, разработчики и статусы.

## Что реализовано в ПР5

- создан Django-проект `freim_project`;
- создано Django-приложение `homepage` для стартовой страницы;
- создано Django-приложение `errors` для списка ошибок и карточки ошибки;
- настроена маршрутизация URL между проектом и приложениями;
- используются view-функции и HTML-шаблоны;
- подключён Bootstrap 5.3 через CDN и собственный CSS;
- данные загружаются из JSON-файлов и отображаются в веб-интерфейсе;
- проект готов к дальнейшему развитию с Django ORM и шаблонами.

## Возможности

- регистрация ошибки с заголовком, описанием и серьезностью;
- связь ошибки с пользователем и ответственным разработчиком;
- автоматическое определение приоритета;
- просмотр, поиск и сортировка ошибок;
- фильтрация по статусу и серьезности;
- изменение статуса и удаление ошибки;
- загрузка объектов из JSON при запуске;
- сохранение объектов в JSON между запусками;
- отображение ошибок через веб-страницы Django.

## Объектная модель

- `Error` - ошибка с атрибутами `id`, `title`, `description`, `severity`, `priority`, `status`, `user`, `developer`. Методы `__str__()`, `from_data()` и `to_data()`.
- `User` - пользователь, зарегистрировавший ошибку. Атрибуты `id`, `name`, `email`.
- `Developer` - разработчик, ответственный за исправление. Атрибуты `id`, `name`, `specialization`.
- `Status` - объект статуса обработки ошибки с атрибутами `id` и `name`.

Класс `Error` хранит ссылки на объекты `User`, `Developer` и `Status`. В JSON сохраняются только идентификаторы связанных объектов. При загрузке `storage.py` восстанавливает связи между объектами.

## Структура проекта

```text
freim_project/
├── __init__.py
├── asgi.py
├── settings.py
├── urls.py
├── wsgi.py

homepage/
├── __init__.py
├── apps.py
├── urls.py
├── views.py
└── templates/homepage/index.html

errors/
├── __init__.py
├── apps.py
├── urls.py
├── views.py
├── templates/errors/error_list.html
└── templates/errors/error_detail.html

templates/
├── base.html

static/
└── css/styles.css

models/
├── __init__.py
├── errors.py
├── users.py
├── developers.py
└── statuses.py

data/
├── errors.json
├── users.json
├── developers.json
└── statuses.json

tests/
├── test_errors.py
└── test_models.py

manage.py
README.md
requirements.txt
```

## Запуск

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

После запуска откройте:

- http://127.0.0.1:8000/ - главная страница;
- http://127.0.0.1:8000/errors/ - список ошибок;
- http://127.0.0.1:8000/errors/1/ - карточка конкретной ошибки.

## Тестирование

```bash
pytest -v
```

Тесты проверяют создание объектов, строковое представление, функции работы с ошибками, связи между объектами и JSON round trip.

## Проверка качества кода

```bash
flake8 .
```
