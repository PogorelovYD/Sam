# Лабораторная работа 2

## Тема

Объединение таблиц, подзапросы и функции преобразования данных в SQL.

## Цель работы

Освоить методы объединения таблиц (`JOIN`, `UNION`), работу с подзапросами и функции преобразования данных (`CASE`, `COALESCE`) в PostgreSQL.

## Основано на

Chapter 3. SQL for Data Preparation

---

# Часть 1. Общие задания

---

## Задание 2.1. Поиск покупателей авто

### Бизнес-задача

Получить контактные данные всех клиентов, купивших автомобиль, для обзвона.

### Требования

- Использовать таблицы `sales`, `customers`, `products`.
- Условие: `product_type = 'automobile'`.
- Условие: `phone IS NOT NULL`.
- Вывести: `customer_id`, `first_name`, `last_name`, `phone`.

### SQL-запрос

```sql
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    c.phone
FROM sales s
INNER JOIN customers c 
    ON s.customer_id = c.customer_id
INNER JOIN products p 
    ON s.product_id = p.product_id
WHERE p.product_type = 'automobile'
  AND c.phone IS NOT NULL;
```

### Скриншот результата

<img width="884" height="1235" alt="Image" src="https://github.com/user-attachments/assets/6814100c-b7fe-4401-bc08-1d5acc7cf3ba" />

### Краткое описание результата

В результате выполнения запроса были получены клиенты, которые покупали товары с типом `automobile`, а также имеют заполненный номер телефона. Для соединения данных использовался `INNER JOIN`, так как нужны только те записи, которые есть одновременно в таблицах продаж, клиентов и товаров.

---

## Задание 2.2. Вечеринка в Лос-Анджелесе

### Бизнес-задача

Составить список приглашенных на мероприятие. В список должны попасть клиенты и сотрудники из Лос-Анджелеса.

### Требования

- Запрос 1: клиенты из `city = 'Los Angeles'`.
- Запрос 2: продавцы из таблицы `salespeople`, работающие в дилерских центрах из таблицы `dealerships`, где `city = 'Los Angeles'`.
- Объединить результаты через `UNION`.
- Добавить поле `guest_type` со значениями `Customer` или `Employee`.

### SQL-запрос

```sql
SELECT 
    c.first_name,
    c.last_name,
    'Customer' AS guest_type
FROM customers c
WHERE c.city = 'Los Angeles'

UNION

SELECT 
    sp.first_name,
    sp.last_name,
    'Employee' AS guest_type
FROM salespeople sp
INNER JOIN dealerships d 
    ON sp.dealership_id = d.dealership_id
WHERE d.city = 'Los Angeles';
```

### Скриншот результата

<img width="876" height="990" alt="Image" src="https://github.com/user-attachments/assets/24102746-4b11-40ba-8206-f85f7e57b7ff" />

### Краткое описание результата

В результате был сформирован единый список приглашенных на мероприятие. В список вошли клиенты из города `Los Angeles` и сотрудники, работающие в дилерских центрах этого города. Для объединения двух выборок использовался оператор `UNION`.

---

## Задание 2.3. Создание витрины данных

### Бизнес-задача

Подготовить плоскую таблицу для аналитиков данных.

### Требования

- Основная таблица: `sales`.
- Соединить таблицы `sales`, `customers`, `products`, `dealerships`.
- Использовать `LEFT JOIN`.
- Если `dealership_id` в продажах равен `NULL`, заменить его на `-1` с помощью `COALESCE`.
- Создать столбец `high_savings`.
- `high_savings` равен `1`, если `(base_msrp - sales_amount) > 500`, иначе `0`.

### SQL-запрос

```sql
SELECT
    s.customer_id,
    c.first_name,
    c.last_name,
    s.product_id,
    p.product_type,
    p.base_msrp,
    s.sales_amount,
    COALESCE(s.dealership_id, -1) AS dealership_id,
    d.city AS dealership_city,
    CASE 
        WHEN (p.base_msrp - s.sales_amount) > 500 THEN 1
        ELSE 0
    END AS high_savings
FROM sales s
LEFT JOIN customers c 
    ON s.customer_id = c.customer_id
LEFT JOIN products p 
    ON s.product_id = p.product_id
LEFT JOIN dealerships d 
    ON s.dealership_id = d.dealership_id;
```

### Скриншот результата

<img width="871" height="1112" alt="Image" src="https://github.com/user-attachments/assets/02422422-65b7-489a-87bf-48afec99a4fd" />

### Краткое описание результата

В результате была создана плоская витрина данных на основе таблицы продаж. К продажам были добавлены данные о клиентах, товарах и дилерских центрах. С помощью функции `COALESCE` отсутствующие значения `dealership_id` были заменены на `-1`. С помощью конструкции `CASE` был создан новый признак `high_savings`, показывающий, была ли экономия больше 500.

---

# Часть 2. Индивидуальные задания

## Вариант 16

---

## Индивидуальное задание 1

### Условие

Показать сотрудников и их должность (`title`), работающих в `Houston`.

### SQL-запрос

```sql
SELECT
    sp.first_name,
    sp.last_name,
    sp.title,
    d.city
FROM salespeople sp
INNER JOIN dealerships d
    ON sp.dealership_id = d.dealership_id
WHERE d.city = 'Houston';
```

### Скриншот результата

<img width="858" height="766" alt="Image" src="https://github.com/user-attachments/assets/ee87ff73-2133-492c-829d-0660b9083bef" />

### Краткое описание результата

В результате выполнения запроса были выведены сотрудники, которые работают в дилерских центрах города `Houston`. Для получения города использовалось соединение таблиц `salespeople` и `dealerships` по полю `dealership_id`.

---

## Индивидуальное задание 2

### Условие

Найти товары, цена которых равна максимальной цене в таблице.

### SQL-запрос

```sql
SELECT
    product_id,
    product_type,
    base_msrp
FROM products
WHERE base_msrp = (
    SELECT MAX(base_msrp)
    FROM products
);
```

### Скриншот результата

<img width="860" height="556" alt="Image" src="https://github.com/user-attachments/assets/3653c04f-586d-400e-90c9-b6cbee08f47c" />

### Краткое описание результата

В результате был найден товар или товары, у которых значение `base_msrp` равно максимальной цене в таблице `products`. Для поиска максимального значения использовался подзапрос с функцией `MAX`.

---

## Индивидуальное задание 3

### Условие

В таблице `customers` вывести первую букву фамилии и полный email.

### SQL-запрос

```sql
SELECT
    LEFT(last_name, 1) AS first_letter_last_name,
    email
FROM customers;
```

### Скриншот результата

<img width="863" height="618" alt="Image" src="https://github.com/user-attachments/assets/24ea6ee2-fe84-4843-ae50-f85707f68028" />

### Краткое описание результата

В результате выполнения запроса для каждого клиента была выведена первая буква фамилии и полный адрес электронной почты. Для получения первой буквы фамилии использовалась функция `LEFT`.

---

# Вывод

В ходе выполнения лабораторной работы были изучены способы объединения таблиц с помощью `INNER JOIN` и `LEFT JOIN`, а также объединение результатов нескольких запросов через оператор `UNION`.

Также были использованы подзапросы для поиска товаров с максимальной ценой и функции преобразования данных. Функция `COALESCE` применялась для замены отсутствующих значений, а конструкция `CASE` использовалась для создания нового вычисляемого признака `high_savings`.

В индивидуальном задании варианта 16 были выполнены запросы для поиска сотрудников из города `Houston`, товаров с максимальной ценой и вывода первой буквы фамилии клиентов вместе с их email.

---

# Список файлов

```text
lab_02/
│
├── README.md
│
└── screenshots/
    ├── task_2_1.png
    ├── task_2_2.png
    ├── task_2_3.png
    ├── variant_16_1.png
    ├── variant_16_2.png
    └── variant_16_3.png
```
