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

SELECT 
    c.first_name,
    c.last_name,
    'Customer' AS guest_type
FROM customers c
WHERE c.city = 'Los Angeles'

UNION

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

	SELECT
    sp.first_name,
    sp.last_name,
    sp.title,
    d.city
FROM salespeople sp
INNER JOIN dealerships d
    ON sp.dealership_id = d.dealership_id
WHERE d.city = 'Houston';

SELECT
    product_id,
    product_type,
    base_msrp
FROM products
WHERE base_msrp = (
    SELECT MAX(base_msrp)
    FROM products
);

SELECT
    LEFT(last_name, 1) AS first_letter_last_name,
    email
FROM customers;