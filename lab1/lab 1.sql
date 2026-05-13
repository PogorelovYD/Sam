-- Ищем всех Уильямов и сортируем по дате найма
SELECT * 
FROM salespeople 
WHERE first_name = 'William' 
ORDER BY hire_date ASC;

-- Товары с ценой в диапазоне от 1000 до 2000
-- Товары с ценой между 1000 и 2000
SELECT * 
FROM products 
WHERE base_msrp BETWEEN 1000 AND 2000 
ORDER BY base_msrp DESC;

CREATE TABLE west_dealers AS 
SELECT * FROM dealerships 
WHERE state IN ('WA', 'OR', 'CA');

-- Добавляем столбец
ALTER TABLE west_dealers ADD COLUMN zone TEXT;

-- Заполняем значением
UPDATE west_dealers SET zone = 'West';

-- Удаляем записи, где дата закрытия заполнена (не пустая)
DELETE FROM west_dealers 
WHERE date_closed IS NOT NULL;

SELECT dealership_id, city, state, date_opened, date_closed, zone 
FROM west_dealers;

SELECT * FROM west_dealers;