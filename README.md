# Freim — Сервис учета ошибок программного продукта

Сервис учета и отслеживания ошибок программного продукта на Python с реляционной базой данных SQLite и веб-интерфейсом на Django.

## 1. Назначение проекта

Freim — учебное веб-приложение для управления дефектами (ошибками) программного обеспечения.
Проект позволяет регистрировать ошибки, связывать их с пользователями и ответственными разработчиками, отслеживать статусы и приоритеты, анализировать статистику по нагрузке и выполнять поиск через современный веб-интерфейс на Django.

Проект развивается поэтапно:
- **ПР1–ПР3**: Консольная версия приложения, ООП-модель и JSON-хранилище;
- **ПР5**: Переход к Django: HTTP, URL-маршрутизация и первые view-функции;
- **ПР6**: Шаблоны Django (DTL), наследование, включаемые компоненты и статические файлы (CSS, JS, логотип);
- **ПР7**: Реляционная база данных SQLite, DDL-схема, импорт данных из JSON, разработка SQL-запросов и получение данных в Django-представлениях с использованием `sqlite3.Row` и параметризованных запросов;
- **ПР9**: Полноценный переход на Django ORM: создание моделей (`User`, `Developer`, `Status`, `Error`), выполнение миграций, перенос данных в `db.sqlite3`, замена сырых SQL-запросов на QuerySet API (`select_related`, фильтрация, сортировка, пагинация `Paginator`, агрегация `annotate(Count(...))`);
- **ПР10**: Глубокая настройка административной панели Django (Django Admin), регистрация всех моделей с классами `ModelAdmin` (фильтрация, поиск, `list_editable`, `readonly_fields`, `autocomplete_fields`, inline-таблицы `TabularInline`, массовые действия `actions`), расширение ORM (`TextChoices`, менеджер `ErrorManager` и `ErrorQuerySet`, метод `close()`), создание суперпользователя и глобальный контекстный процессор `bugtracker_context`.

## 2. Используемые технологии

- Python 3;
- Django 5;
- SQLite 3;
- SQL (DDL, DML, агрегатные функции, GROUP BY, HAVING, подзапросы NOT IN);
- Django Template Language (DTL);
- HTML5;
- CSS3;
- JavaScript;
- Bootstrap 5;
- JSON для исходных данных;
- Git;
- pytest;
- flake8.

## 3. Реляционная база данных и структура таблиц (ПР7)

Для проекта спроектирована реляционная база данных в SQLite: `data/freim.sqlite`.

### 3.1. Таблицы и типы данных

1. **`users`** (пользователи, регистрирующие ошибки):
   - `id INTEGER PRIMARY KEY` — уникальный идентификатор пользователя;
   - `name TEXT NOT NULL` — имя пользователя;
   - `email TEXT NOT NULL` — адрес электронной почты.

2. **`developers`** (разработчики, ответственные за исправление):
   - `id INTEGER PRIMARY KEY` — уникальный идентификатор разработчика;
   - `name TEXT NOT NULL` — имя разработчика;
   - `specialization TEXT NOT NULL` — область специализации.

3. **`statuses`** (статусы жизненного цикла ошибки):
   - `id INTEGER PRIMARY KEY` — уникальный идентификатор статуса;
   - `name TEXT NOT NULL` — наименование статуса (`Новая`, `В работе`, `Исправлена`, `Закрыта`).

4. **`errors`** (ошибки программного продукта):
   - `id INTEGER PRIMARY KEY` — уникальный идентификатор ошибки;
   - `title TEXT NOT NULL` — заголовок ошибки;
   - `description TEXT NOT NULL` — подробное описание ошибки;
   - `severity TEXT NOT NULL` — уровень серьезности (`критическая`, `значительная`, `незначительная`);
   - `priority TEXT NOT NULL` — приоритет (`Высокий`, `Средний`, `Низкий`);
   - `status_id INTEGER NOT NULL` — внешний ключ к таблице `statuses(id)`;
   - `user_id INTEGER NOT NULL` — внешний ключ к таблице `users(id)`;
   - `developer_id INTEGER NOT NULL` — внешний ключ к таблице `developers(id)`.

Внешние ключи контролируются на уровне СУБД с помощью директивы `PRAGMA foreign_keys = ON`.

## 4. Схема и запросы SQL

- **`sql/schema.sql`** — файл DDL с командами `CREATE TABLE IF NOT EXISTS` для всех сущностей с внешними ключами;
- **`sql/queries.sql`** — набор из 13 проверенных SQL-запросов с подробными комментариями:
  - *Выборка списков объектов*: Запросы 1 и 2;
  - *Фильтрация WHERE*: Запрос 3 (критические ошибки), Запрос 4 (активные ошибки), Запрос 5 (поиск по LIKE);
  - *Соединение таблиц JOIN*: Запрос 6 (полная информация об ошибке с 4 таблицами), Запрос 7 (LEFT JOIN разработчиков и назначенных задач);
  - *Агрегатные функции COUNT*: Запрос 8 (число активных ошибок), Запрос 9 (число ошибок высокого приоритета);
  - *Группировка GROUP BY*: Запрос 10 (ошибки по разработчикам), Запрос 11 (ошибки по статусам);
  - *Фильтрация групп HAVING*: Запрос 12 (разработчики с количеством задач более 1);
  - *Подзапросы NOT IN*: Запрос 13 (свободные разработчики без активных назначений).

## 5. Модули базы данных

- **`db/database.py`**:
  Предоставляет функцию `get_connection(db_path=None)`, создающую соединение `sqlite3.connect()` и гарантированно активирующую проверку внешних ключей (`PRAGMA foreign_keys = ON`).
- **`db/import_json.py`**:
  Скрипт переноса данных из исходных JSON-файлов (`users.json`, `developers.json`, `statuses.json`, `errors.json`) в таблицы SQLite с использованием `executemany()`, транзакционного контроля (`commit`, `rollback`) и автоматическим вызовом схемы `sql/schema.sql`.

Запуск импорта:
```bash
python -m db.import_json
```

## 6. Модели Django ORM и интеграция с веб-интерфейсом (ПР9)

В приложении `bugtracker` реализованы модели Django ORM (`bugtracker/models.py`), полностью отражающие реляционную структуру:
- **`User`** (`verbose_name="Пользователь"`): поля `name`, `email`;
- **`Developer`** (`verbose_name="Разработчик"`): поля `name`, `specialization`;
- **`Status`** (`verbose_name="Статус"`): поле `name`;
- **`Error`** (`verbose_name="Ошибка"`): поля `title`, `description`, `severity`, `priority`, а также внешние ключи `status`, `user`, `developer` с `on_delete=models.PROTECT` и `related_name="errors"`.

Все модели содержат:
- понятные русскоязычные `verbose_name` и `verbose_name_plural`;
- информативные методы `__str__()`;
- сортировку по умолчанию в классе `Meta` (`ordering`);
- метод `get_absolute_url()` для сущности `Error`.

### 6.1. Миграции и перенос данных
- Начальная миграция схемы: `bugtracker/migrations/0001_initial.py`;
- Скрипт миграции данных из `data/freim.sqlite` в `db.sqlite3`: `db/import_sqlite_to_orm.py`.

Запуск миграций и импорта:
```bash
python manage.py migrate
python -m db.import_sqlite_to_orm
```

### 6.2. QuerySet API в представлениях
Все Django-представления переведены с прямого `sqlite3` на Django ORM:
- **Оптимизация запросов (`select_related`)**: предотвращение проблемы N+1 запросов при выборке связанных сущностей (`status`, `developer`, `user`);
- **Главная (`/`)**: сводные счетчики через ORM (`Error.objects.count()`, `Status.objects.count()`, `Developer.objects.count()`) и последние ошибки через `order_by('-id')[:5]`;
- **Список ошибок (`/errors/`)**: фильтрация по статусу, разработчику, серьезности и приоритету; динамическая сортировка; постраничный вывод (`Paginator`) с сохранением GET-параметров в ссылках пагинации через `{% querystring %}`;
- **Карточка ошибки (`/errors/<id>/`)**: безопасное получение объекта через `get_object_or_404(Error, pk=error_id)`;
- **Поиск ошибок (`/errors/search/`)**: фильтрация с использованием `Q`-объектов;
- **Статистика (`/errors/statistics/`)**: агрегация через `annotate(count=Count('errors'))` для статусов и разработчиков.

## 7. Административная панель Django и расширенные возможности ORM (ПР10)

В рамках ПР10 реализована полноценная настройка административного интерфейса (`bugtracker/admin.py`) и углубленная работа с Django ORM:

### 7.1. Настройка Django Admin
Все ключевые модели зарегистрированы с помощью декоратора `@admin.register`:
- **`ErrorAdmin` (`Error`)**:
  - `list_display`: идентификатор, заголовок, серьезность, приоритет, статус, назначенный разработчик, создавший пользователь;
  - `list_display_links`: переход в карточку ошибки по клику на `id` или `title`;
  - `search_fields`: полнотекстовый поиск по `title`, `description`, имени разработчика `developer__name` и пользователя `user__name`;
  - `list_filter`: быстрая фильтрация по уровню серьезности, приоритету, статусу и разработчику;
  - `list_editable`: прямое редактирование приоритета ошибки в списке объектов без перехода в детальную форму;
  - `readonly_fields`: защита системного первичного ключа `id` от случайного изменения;
  - `autocomplete_fields`: динамический поиск и подстановка связанных сущностей `developer`, `user`, `status`;
  - `save_on_top`: дублирование кнопок сохранения в верхней части формы;
  - **Массовые действия (`actions`)**:
    - `mark_closed`: пакетный перевод выделенных ошибок в статус «Закрыта»;
    - `make_high_priority`: пакетное повышение приоритета ошибок до «Высокий».
- **`DeveloperAdmin` (`Developer`)**:
  - Отображение ФИО, специализации и вычисляемого количества ошибок `errors_count` (с сортировкой по аннотации `Count('errors')`);
  - Встроенная таблица назначенных ошибок `ErrorInline` (`admin.TabularInline`) прямо в карточке разработчика;
  - Поиск по имени и специализации, фильтр по специализации.
- **`UserAdmin` (`User`)**:
  - Отображение имени, email и количества созданных ошибок;
  - Встроенная таблица `ErrorInline` в карточке пользователя;
  - Поиск по имени и адресу электронной почты.
- **`StatusAdmin` (`Status`)**:
  - Отображение наименования статуса и количества привязанных ошибок `errors_count`.
- **Брендирование панели**:
  - Заголовок `admin.site.site_header`: «Панель управления Freim»;
  - Заголовок страницы `admin.site.site_title`: «Freim Bugtracker Admin»;
  - Подзаголовок главной страницы `admin.site.index_title`: «Управление дефектами и справочниками».

### 7.2. Суперпользователь и скрипт инициализации
Для входа в административную панель подготовлен административный пользователь:
- **Логин**: `admin`
- **Пароль**: `admin`
- **Email**: `admin@example.com`

Скрипт проверки и автоматического создания администратора: `db/create_superuser.py`.
```bash
python -m db.create_superuser
```

### 7.3. Расширенные возможности моделей и ORM
- **`models.TextChoices`**:
  - `Severity`: `критическая`, `значительная`, `незначительная`;
  - `Priority`: `Высокий`, `Средний`, `Низкий`.
- **Подсказки `help_text`**: поясняющие подсказки для всех полей моделей в интерфейсе администратора;
- **Кастомный QuerySet и Manager (`ErrorQuerySet`, `ErrorManager`)**:
  - `Error.objects.active()` — исключает закрытые и исправленные ошибки;
  - `Error.objects.critical()` — фильтрует критические ошибки;
  - `Error.objects.high_priority()` — фильтрует задачи высокого приоритета;
  - `Error.objects.by_status(status_name)` — фильтрация по имени статуса;
- **Метод модели `error.close()`**: перевод ошибки в статус «Закрыта».

### 7.4. Пользовательский контекстный процессор
Создан модуль `bugtracker/context_processors.py`, зарегистрированный в `settings.py` (`TEMPLATES -> OPTIONS -> context_processors`).
Функция `bugtracker_context(request)` передает во все шаблоны:
- `site_name`: название сервиса (`Freim`);
- `total_errors_count`: общее количество ошибок в системе;
- `active_errors_count`: количество активных (не закрытых) ошибок;
- `critical_errors_count`: количество критических ошибок.

В навигационной панели (`templates/includes/navigation.html`) добавлен бейдж с количеством ошибок и быстрая ссылка на Django Admin (`/admin/`).

## 8. Структура проекта

```text
Freim-main/
├── db/
│   ├── __init__.py
│   ├── create_superuser.py
│   ├── database.py
│   ├── import_json.py
│   ├── import_sqlite_to_orm.py
│   └── inspect_source_db.py
│
├── sql/
│   ├── queries.sql
│   └── schema.sql
│
├── data/
│   ├── developers.json
│   ├── errors.json
│   ├── statuses.json
│   ├── users.json
│   └── freim.sqlite
│
├── db.sqlite3
│
├── bugtracker/
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   └── 0002_alter_developer_name_alter_developer_specialization_and_more.py
│   ├── templates/errors/
│   │   ├── includes/
│   │   │   ├── error_card.html
│   │   │   └── error_status.html
│   │   ├── error_detail.html
│   │   ├── error_list.html
│   │   ├── error_search.html
│   │   └── statistics.html
│   ├── admin.py
│   ├── apps.py
│   ├── context_processors.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── homepage/
│   ├── static/homepage/
│   │   ├── css/style.css
│   │   ├── img/logo.png
│   │   └── js/main.js
│   ├── templates/homepage/
│   │   └── index.html
│   ├── apps.py
│   ├── urls.py
│   └── views.py
│
├── templates/
│   ├── includes/navigation.html
│   ├── errors/
│   ├── homepage/
│   └── base.html
│
├── models/
├── tests/
│   ├── test_admin.py
│   ├── test_database.py
│   ├── test_errors.py
│   ├── test_models.py
│   ├── test_orm.py
│   └── test_views.py
│
├── freim_project/
├── manage.py
└── README.md
```

## 9. Проверка и тестирование

1. Системная проверка Django:
```bash
python manage.py check
```

2. Запуск тестов:
```bash
pytest -v
```
(Проходят все 33 автоматизированных теста, охватывающие ООП-модели, SQL, представления, Django ORM, контекстные процессоры и Django Admin).

3. Проверка качества кода по стандарту PEP 8:
```bash
flake8 . --extend-exclude=.venv
```

4. Запуск сервера разработки:
```bash
python manage.py runserver
```
После запуска сайт доступен по адресу: http://127.0.0.1:8000/
Панель администратора доступна по адресу: http://127.0.0.1:8000/admin/ (учётные данные: `admin` / `admin`).
