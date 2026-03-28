DROP SCHEMA IF EXISTS ecommerce_st16 CASCADE;
CREATE SCHEMA ecommerce_st16;

CREATE TABLE ecommerce_st16.customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    city VARCHAR(50) DEFAULT 'Москва'
);

CREATE TABLE ecommerce_st16.products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price DECIMAL(12,2) NOT NULL CHECK (price > 0)
);

CREATE TABLE ecommerce_st16.orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES ecommerce_st16.customers(customer_id) ON DELETE CASCADE,
    order_date DATE DEFAULT CURRENT_DATE,
    status VARCHAR(20) CHECK (status IN ('Новый', 'Оплачен', 'Доставлен', 'Отменен'))
);

CREATE TABLE ecommerce_st16.order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES ecommerce_st16.orders(order_id) ON DELETE CASCADE,
    product_id INT REFERENCES ecommerce_st16.products(product_id),
    quantity INT NOT NULL CHECK (quantity > 0),
    price_per_unit DECIMAL(12,2) NOT NULL CHECK (price_per_unit > 0)
);

INSERT INTO ecommerce_st16.customers (name, email, city) VALUES
('Елена Васильева', 'e.vas@mail.ru', 'Москва'),
('Сергей Новиков', 's.novikov@gmail.com', 'Санкт-Петербург'),
('Анна Смирнова', 'anna.s@yandex.ru', 'Казань'),
('Игорь Петров', 'igor.p@mail.ru', 'Екатеринбург'),
('Ольга Иванова', 'olga.iv@gmail.com', 'Новосибирск'),
('Артем Сидоров', 'artem66@bk.ru', 'Москва');

INSERT INTO ecommerce_st16.products (name, category, price) VALUES
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

INSERT INTO ecommerce_st16.orders (customer_id, status, order_date) VALUES
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

INSERT INTO ecommerce_st16.order_items (order_id, product_id, quantity, price_per_unit) VALUES
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

SELECT * FROM ecommerce_st16.customers;
SELECT * FROM ecommerce_st16.products;
SELECT * FROM ecommerce_st16.orders;
SELECT * FROM ecommerce_st16.order_items;

SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_schema = 'ecommerce_st16'
ORDER BY table_name;