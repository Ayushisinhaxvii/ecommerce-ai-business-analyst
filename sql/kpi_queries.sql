-- KPI: Total Orders

SELECT
    COUNT(*) AS total_orders
FROM orders;

SELECT COUNT(*) AS customer_records
FROM customers;
-- KPI: Total Unique Customers
SELECT
    COUNT(DISTINCT customer_unique_id) AS total_customers
FROM customers;

-- Find customers who placed more than one order
SELECT
    customer_unique_id,
    COUNT(*) AS order_count
FROM customers
GROUP BY customer_unique_id
HAVING COUNT(*) > 1
ORDER BY order_count DESC;

-- KPI: Number of Repeat Customers
SELECT COUNT(*) AS repeat_customers
FROM (
    SELECT
        customer_unique_id
    FROM customers
    GROUP BY customer_unique_id
    HAVING COUNT(*) > 1
);

-- KPI: Repeat Customer Rate
SELECT
    ROUND(
        100.0 * 
        COUNT(*) /
        (SELECT COUNT(DISTINCT customer_unique_id)
         FROM customers),
        2
    ) AS repeat_customer_rate
FROM (
    SELECT
        customer_unique_id
    FROM customers
    GROUP BY customer_unique_id
    HAVING COUNT(*) > 1
);

-- Total product sales
SELECT
    SUM(price) AS total_product_sales
FROM order_items;

-- Number of orders containing items
SELECT
    COUNT(DISTINCT order_id) AS orders_with_items
FROM order_items;

-- KPI: Average Order Value based on product price
SELECT
    ROUND(
        SUM(price) / COUNT(DISTINCT order_id),
        2
    ) AS average_order_value
FROM order_items;

-- Compare product sales and freight
SELECT
    SUM(price) AS total_product_sales,
    SUM(freight_value) AS total_freight,
    SUM(price + freight_value) AS total_order_value
FROM order_items;

-- KPI: Average Delivery Time in Days
SELECT
    ROUND(
        AVG(
            julianday(order_delivered_customer_date)
            - julianday(order_purchase_timestamp)
        ),
        2
    ) AS average_delivery_days
FROM orders
WHERE order_status = 'delivered'
  AND order_delivered_customer_date IS NOT NULL;
  
  
  -- Count late delivered orders
SELECT
    COUNT(*) AS late_orders
FROM orders
WHERE order_status = 'delivered'
  AND order_delivered_customer_date IS NOT NULL
  AND order_delivered_customer_date > order_estimated_delivery_date;
  
  
  -- KPI: Late Delivery Rate
SELECT
    ROUND(
        100.0 * SUM(
            CASE
                WHEN order_delivered_customer_date > order_estimated_delivery_date
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS late_delivery_rate
FROM orders
WHERE order_status = 'delivered'
  AND order_delivered_customer_date IS NOT NULL;
  
  
  
 -- KPI: Average Review Score
SELECT
    ROUND(AVG(review_score), 2) AS average_review_score
FROM reviews
WHERE review_score IS NOT NULL;

-- Review Score Distribution
SELECT
    review_score,
    COUNT(*) AS review_count
FROM reviews
WHERE review_score IS NOT NULL
GROUP BY review_score
ORDER BY review_score;

-- Count cancelled orders
SELECT
    COUNT(*) AS canceled_orders
FROM orders
WHERE order_status = 'canceled';


-- KPI: Cancellation Rate
SELECT
    ROUND(
        100.0 * SUM(
            CASE
                WHEN order_status = 'canceled' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS cancellation_rate
FROM orders;