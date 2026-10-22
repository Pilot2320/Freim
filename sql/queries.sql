-- ====================================================================
-- SQL-запросы для сервиса учета ошибок Freim (ПР7)
-- ====================================================================

-- 1. Выборка списков объектов
-- --------------------------------------------------------------------
-- Запрос 1. Список всех ошибок с сортировкой по ID
SELECT id, title, severity, priority
FROM errors
ORDER BY id;

-- Запрос 2. Список всех разработчиков с сортировкой по имени
SELECT id, name, specialization
FROM developers
ORDER BY name;

-- 2. Фильтрация данных (WHERE)
-- --------------------------------------------------------------------
-- Запрос 3. Поиск ошибок с критической серьезностью
SELECT id, title, severity, priority
FROM errors
WHERE severity = 'критическая'
ORDER BY id;

-- Запрос 4. Выборка активных (не закрытых) ошибок
SELECT id, title, severity, priority, status_id
FROM errors
WHERE status_id != 4
ORDER BY id;

-- Запрос 5. Поиск ошибок по ключевому слову в заголовке
SELECT id, title, severity, priority
FROM errors
WHERE title LIKE '%парол%'
ORDER BY id;

-- 3. Соединение связанных таблиц (JOIN)
-- --------------------------------------------------------------------
-- Запрос 6. Полная информация об ошибках со связями (JOIN 4 таблиц)
SELECT
    errors.id,
    errors.title,
    errors.description,
    errors.severity,
    errors.priority,
    statuses.name AS status_name,
    users.name AS user_name,
    users.email AS user_email,
    developers.name AS developer_name,
    developers.specialization AS developer_specialization
FROM errors
JOIN statuses ON errors.status_id = statuses.id
JOIN users ON errors.user_id = users.id
JOIN developers ON errors.developer_id = developers.id
ORDER BY errors.id;

-- Запрос 7. Разработчики и закрепленные за ними активные ошибки (LEFT JOIN)
SELECT
    developers.name AS developer_name,
    developers.specialization,
    errors.id AS error_id,
    errors.title AS error_title
FROM developers
LEFT JOIN errors ON developers.id = errors.developer_id
    AND errors.status_id != 4
ORDER BY developers.name;

-- 4. Агрегирующие функции (COUNT)
-- --------------------------------------------------------------------
-- Запрос 8. Подсчет общего количества активных ошибок
SELECT COUNT(*) AS active_errors_count
FROM errors
WHERE status_id != 4;

-- Запрос 9. Подсчет количества ошибок с высоким приоритетом
SELECT COUNT(*) AS high_priority_count
FROM errors
WHERE priority = 'Высокий';

-- 5. Группировка записей (GROUP BY)
-- --------------------------------------------------------------------
-- Запрос 10. Количество ошибок по каждому разработчику
SELECT
    developers.id,
    developers.name AS developer_name,
    COUNT(errors.id) AS errors_count
FROM developers
LEFT JOIN errors ON developers.id = errors.developer_id
GROUP BY developers.id, developers.name
ORDER BY errors_count DESC;

-- Запрос 11. Количество ошибок по каждому статусу
SELECT
    statuses.id,
    statuses.name AS status_name,
    COUNT(errors.id) AS errors_count
FROM statuses
LEFT JOIN errors ON statuses.id = errors.status_id
GROUP BY statuses.id, statuses.name
ORDER BY statuses.id;

-- 6. Фильтрация групп после группировки (HAVING)
-- --------------------------------------------------------------------
-- Запрос 12. Разработчики с более чем одной назначенной ошибкой
SELECT
    developers.name AS developer_name,
    COUNT(errors.id) AS errors_count
FROM developers
JOIN errors ON developers.id = errors.developer_id
GROUP BY developers.id, developers.name
HAVING COUNT(errors.id) > 1
ORDER BY errors_count DESC;

-- 7. Подзапросы (NOT IN)
-- --------------------------------------------------------------------
-- Запрос 13. Разработчики, не имеющие активных назначенных ошибок
SELECT
    developers.id,
    developers.name,
    developers.specialization
FROM developers
WHERE developers.id NOT IN (
    SELECT errors.developer_id
    FROM errors
    WHERE errors.status_id != 4
)
ORDER BY developers.name;

