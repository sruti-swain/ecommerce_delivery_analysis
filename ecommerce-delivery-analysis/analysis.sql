
-- =====================================================
-- E-COMMERCE ORDER AND DELIVERY ANALYSIS
-- SQL Analytics Project
-- Database: ecommerce_orders.db
-- Table: orders
-- =====================================================


-- QUERY 1: View all order records
SELECT *
FROM orders
LIMIT 10;


-- QUERY 2: Check total orders and data quality
SELECT
    COUNT(*) AS total_orders,
    SUM(
        CASE
            WHEN Data_Quality_Status = 'Valid' THEN 1
            ELSE 0
        END
    ) AS valid_orders,
    SUM(
        CASE
            WHEN Data_Quality_Status != 'Valid' THEN 1
            ELSE 0
        END
    ) AS invalid_orders
FROM orders;


-- QUERY 3: Find duplicate order IDs
-- Useful for data quality validation
SELECT
    Order_ID,
    COUNT(*) AS record_count
FROM orders
GROUP BY Order_ID
HAVING COUNT(*) > 1;


-- QUERY 4: Find orders with missing delivery dates
SELECT
    Order_ID,
    City,
    Category,
    Order_Status
FROM orders
WHERE Delivery_Date IS NULL;


-- QUERY 5: Find invalid delivery date sequences
SELECT
    Order_ID,
    Order_Date,
    Delivery_Date,
    Data_Quality_Status
FROM orders
WHERE Data_Quality_Status = 'Invalid Delivery Date';


-- QUERY 6: Calculate average delivery time
SELECT
    ROUND(AVG(Delivery_Days), 2)
        AS average_delivery_days
FROM orders
WHERE Delivery_Days IS NOT NULL
  AND Data_Quality_Status = 'Valid';


-- QUERY 7: Analyze delivery performance
SELECT
    Delivery_Performance,
    COUNT(*) AS total_orders
FROM orders
GROUP BY Delivery_Performance
ORDER BY total_orders DESC;


-- QUERY 8: Compare delivery performance by city
SELECT
    City,
    COUNT(*) AS total_orders,
    ROUND(AVG(Delivery_Days), 2)
        AS average_delivery_days,
    SUM(
        CASE
            WHEN Delivery_Performance = 'Delayed' THEN 1
            ELSE 0
        END
    ) AS delayed_orders
FROM orders
WHERE City IS NOT NULL
  AND Data_Quality_Status = 'Valid'
GROUP BY City
ORDER BY average_delivery_days DESC;


-- QUERY 9: Calculate the delayed delivery percentage
SELECT
    ROUND(
        100.0 * SUM(
            CASE
                WHEN Delivery_Performance = 'Delayed' THEN 1
                ELSE 0
            END
        ) / NULLIF(
            SUM(
                CASE
                    WHEN Delivery_Performance IN ('Delayed', 'On Time')
                    THEN 1
                    ELSE 0
                END
            ), 0
        ),
        2
    ) AS delayed_delivery_percentage
FROM orders
WHERE Data_Quality_Status = 'Valid';


-- QUERY 10: Analyze orders by product category
SELECT
    Category,
    COUNT(*) AS total_orders,
    ROUND(AVG(Delivery_Days), 2)
        AS average_delivery_days
FROM orders
WHERE Category IS NOT NULL
  AND Data_Quality_Status = 'Valid'
GROUP BY Category
ORDER BY total_orders DESC;


-- QUERY 11: Find the five slowest completed deliveries
SELECT
    Order_ID,
    City,
    Category,
    Delivery_Days
FROM orders
WHERE Delivery_Days IS NOT NULL
  AND Data_Quality_Status = 'Valid'
ORDER BY Delivery_Days DESC
LIMIT 5;


-- QUERY 12: Monthly order volume
SELECT
    strftime('%Y-%m', Order_Date) AS order_month,
    COUNT(*) AS total_orders
FROM orders
WHERE Order_Date IS NOT NULL
  AND Data_Quality_Status = 'Valid'
GROUP BY strftime('%Y-%m', Order_Date)
ORDER BY order_month;
