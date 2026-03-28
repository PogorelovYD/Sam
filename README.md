# Самостоятельная работа 1
## Выполнил: Погорелов Ярослав, группа [ЦИБ-241]

---

## Цель работы
Научиться подключаться к базе данных PostgreSQL, создавать структуру данных, наполнять её тестовыми данными и выполнять аналитические запросы. Построить визуализацию данных интернет-магазина в сервисе DataLens.

---

## Ход работы

### 1. Подключение к базе данных

Работа была выполнена на локальном сервере PostgreSQL с использованием DBeaver для выполнения SQL-запросов и просмотра структуры базы данных.

### 2. Создание структуры базы данных

Создана схема базы данных `ecommerce_st16` со следующими таблицами:
- `customers` — клиенты интернет-магазина
- `products` — товары
- `orders` — заказы
- `order_items` — состав заказов

```sql
CREATE SCHEMA IF NOT EXISTS ecommerce_st16;
SET search_path TO ecommerce_st16;

DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS customers CASCADE;

CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    city VARCHAR(50) DEFAULT 'Москва'
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price DECIMAL(12, 2) NOT NULL
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id) ON DELETE CASCADE,
    order_date DATE DEFAULT CURRENT_DATE,
    status VARCHAR(20) CHECK (status IN ('Новый', 'Оплачен', 'Доставлен', 'Отменен'))
);

CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(order_id) ON DELETE CASCADE,
    product_id INT REFERENCES products(product_id),
    quantity INT NOT NULL,
    price_per_unit DECIMAL(12, 2) NOT NULL
);
```

### 3. Наполнение данными

Таблицы были заполнены тестовыми данными, включающими:
- 6 клиентов
- 10 товаров
- 12 заказов
- позиции товаров в заказах

В базе представлены товары трёх категорий: электроника, книги, аксессуары.
Также были заданы разные статусы заказов: Новый, Оплачен, Доставлен, Отменен.

```sql
INSERT INTO customers (name, email, city) VALUES
('Елена Васильева', 'e.vas@mail.ru', 'Москва'),
('Сергей Новиков', 's.novikov@gmail.com', 'Санкт-Петербург'),
('Анна Смирнова', 'anna.s@yandex.ru', 'Казань'),
('Игорь Петров', 'igor.p@mail.ru', 'Екатеринбург'),
('Ольга Иванова', 'olga.iv@gmail.com', 'Новосибирск'),
('Артем Сидоров', 'artem66@bk.ru', 'Москва');

INSERT INTO products (name, category, price) VALUES
('Ноутбук "Мощь"', 'Электроника', 75000.00),
('Смартфон X', 'Электроника', 45000.00),
('Наушники Pro', 'Электроника', 12000.00),
('Планшет Air', 'Электроника', 35000.00),
('Книга "SQL для начинающих"', 'Книги', 1200.00),
('Книга "Python с нуля"', 'Книги', 1500.00),
('Книга "Data Science"', 'Книги', 2200.00),
('Мышь беспроводная', 'Аксессуары', 1500.00),
('Коврик для мыши', 'Аксессуары', 500.00),
('Рюкзак для ноутбука', 'Аксессуары', 4500.00);

INSERT INTO orders (customer_id, status, order_date) VALUES
(1, 'Доставлен', '2024-03-01'),
(2, 'Новый', '2024-03-10'),
(3, 'Оплачен', '2024-03-12'),
(4, 'Доставлен', '2024-03-15'),
(5, 'Оплачен', '2024-03-20'),
(6, 'Новый', '2024-03-22'),
(1, 'Оплачен', '2024-03-25'),
(2, 'Доставлен', '2024-03-26'),
(3, 'Доставлен', '2024-03-27'),
(4, 'Отменен', '2024-03-28'),
(5, 'Новый', '2024-03-29'),
(6, 'Доставлен', '2024-03-30');

INSERT INTO order_items (order_id, product_id, quantity, price_per_unit) VALUES
(1, 1, 1, 75000.00), (1, 8, 1, 1500.00), (1, 9, 1, 500.00),
(2, 5, 2, 1200.00), (2, 6, 1, 1500.00),
(3, 2, 1, 45000.00), (3, 3, 1, 12000.00),
(4, 10, 2, 4500.00), (4, 9, 1, 500.00),
(5, 7, 3, 2200.00), (5, 8, 1, 1500.00),
(6, 1, 1, 75000.00),
(7, 4, 1, 35000.00), (7, 6, 2, 1500.00),
(8, 2, 1, 45000.00),
(9, 3, 2, 12000.00), (9, 7, 1, 2200.00),
(10, 1, 1, 75000.00),
(11, 8, 3, 1500.00),
(12, 4, 1, 35000.00);
```

[Полный sql_dump](Script-2.sql)

### 4. Аналитические запросы
Для анализа данных были выполнены SQL-запросы, позволяющие получить основные показатели интернет-магазина.

#### 4.1. Выручка по категориям товаров
```sql
SELECT 
    p.category,
    SUM(oi.quantity * oi.price_per_unit) AS total_revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status <> 'Отменен'
GROUP BY p.category
ORDER BY total_revenue DESC;
```

#### 4.2. Топ-5 самых прибыльных товаров
```sql
SELECT 
    p.name,
    SUM(oi.quantity * oi.price_per_unit) AS product_revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status <> 'Отменен'
GROUP BY p.name
ORDER BY product_revenue DESC
LIMIT 5;
```

#### 4.3. Средний чек по городам
```sql
SELECT 
    c.city,
    ROUND(AVG(sub.order_total), 2) AS avg_order_value
FROM (
    SELECT 
        o.order_id,
        o.customer_id,
        SUM(oi.quantity * oi.price_per_unit) AS order_total
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.status <> 'Отменен'
    GROUP BY o.order_id, o.customer_id
) sub
JOIN customers c ON sub.customer_id = c.customer_id
GROUP BY c.city
ORDER BY avg_order_value DESC;
```

#### 4.4. Подготовка итоговой таблицы для DataLens
Для визуализации была сформирована итоговая таблица продаж, содержащая: номер заказа, дату заказа, город клиента, категорию товара, название товара, количество, цену за единицу и итоговую сумму по позиции.

```sql
SELECT
    o.order_id,
    o.order_date,
    c.city,
    p.category,
    p.name AS product_name,
    oi.quantity,
    oi.price_per_unit,
    (oi.quantity * oi.price_per_unit) AS total_sum
FROM ecommerce_st16.orders o
JOIN ecommerce_st16.customers c ON o.customer_id = c.customer_id
JOIN ecommerce_st16.order_items oi ON o.order_id = oi.order_id
JOIN ecommerce_st16.products p ON oi.product_id = p.product_id
WHERE o.status <> 'Отменен'
ORDER BY o.order_date, o.order_id;
```
Результат запроса был экспортирован в файл формата `.xlsx` и загружен в Yandex DataLens.

### 5. Визуализация в DataLens
Создано соединение по файлу: [файлик](data-1774614076535.csv)

Разработаны чарты и дашборд с визуализацией данных интернет-магазина.
В дашборде (Название: **Анализ интернет-магазина: продажи, категории и товары**) были размещены следующие элементы:
- Выручка по категориям — столбчатая диаграмма
- Доля категорий в общей выручке — круговая диаграмма
- Топ-5 товаров по выручке — столбчатая диаграмма
- Средний чек по городам — столбчатая диаграмма
- Детализация продаж — таблица

<img width="1231" height="624" alt="image" src="СЮДА_ССЫЛКУ_НА_СКРИНШОТ" />

[открыть дашборд](https://datalens.ru/ae7llcygk6v4u)

---

## Результаты

**Аналитические выводы:**

1. **Наибольшую выручку приносит категория «Электроника».** По рассчитанным данным её суммарная выручка составляет 346 000 руб., что значительно выше остальных категорий. Категории «Книги» и «Аксессуары» приносят существенно меньшую выручку (15 700 руб. и 17 500 руб. соответственно).
2. **Самым прибыльным товаром оказался ноутбук «Мощь».** Его суммарная выручка составила 150 000 руб. 
   В топ-5 товаров по выручке вошли:
   - ноутбук «Мощь»
   - смартфон X
   - планшет Air
   - наушники Pro
   - рюкзак для ноутбука
3. **Самый высокий средний чек наблюдается в Москве** — 56 250 руб. Это связано с покупками дорогостоящей электроники. Наименьший средний чек зафиксирован в Новосибирске — 6 300 руб.

---

## Заключение

В ходе работы были получены навыки:
- подключения и работы с PostgreSQL через DBeaver
- проектирования структуры базы данных
- создания связанных таблиц с внешними ключами
- наполнения базы тестовыми данными
- написания аналитических SQL-запросов с использованием JOIN, GROUP BY, SUM, AVG
- визуализации данных в BI-системе Yandex DataLens

Созданный дашборд позволяет быстро оценить структуру ассортимента интернет-магазина, распределение выручки по категориям, наиболее прибыльные товары и различия среднего чека по городам.
