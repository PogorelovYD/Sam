SELECT
    MAX(base_msrp) AS max_car_price,
    MIN(base_msrp) AS min_car_price,
    MAX(base_msrp) - MIN(base_msrp) AS price_difference
FROM products
WHERE product_type = 'automobile';

SELECT
    year,
    ROUND(AVG(base_msrp), 2) AS avg_product_price
FROM products
GROUP BY year
ORDER BY year;

SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    ROUND(SUM(s.sales_amount)::numeric, 2) AS total_purchase_amount
FROM customers c
INNER JOIN sales s
    ON c.customer_id = s.customer_id
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name
HAVING SUM(s.sales_amount) > 20000
ORDER BY total_purchase_amount DESC;