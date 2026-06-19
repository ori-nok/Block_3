-- ЗАПРОС 1: Топ-10 клиентов по сумме покупок
SELECT 
    c.full_name AS Клиент,
    SUM(o.quantity * o.unit_price) AS Сумма_покупок
FROM fact_orders o
JOIN dim_customers c ON o.customer_id = c.customer_id
WHERE o.status = 'completed'
GROUP BY c.customer_id, c.full_name
ORDER BY Сумма_покупок DESC
LIMIT 10;

-- ЗАПРОС 2: Выручка по месяцам
SELECT 
    TO_CHAR(payment_timestamp, 'YYYY-MM') AS Месяц,
    SUM(amount) AS Общая_выручка
FROM fact_payments
GROUP BY TO_CHAR(payment_timestamp, 'YYYY-MM')
ORDER BY Месяц;

-- ЗАПРОС 3: Самые популярные товары
SELECT 
    p.product_name AS Товар,
    p.category AS Категория,
    SUM(o.quantity) AS Продано_штук
FROM fact_orders o
JOIN dim_products p ON o.product_id = p.product_id
WHERE o.status = 'completed'
GROUP BY p.product_id, p.product_name, p.category
ORDER BY Продано_штук DESC
LIMIT 10;

-- ЗАПРОС 4: Последняя активность топ-5 пользователей
WITH TopBuyers AS (
    SELECT 
        customer_id,
        COUNT(order_id) AS Количество_заказов
    FROM fact_orders
    GROUP BY customer_id
    ORDER BY Количество_заказов DESC
    LIMIT 5
)
SELECT 
    c.full_name AS Клиент,
    tb.Количество_заказов,
    MAX(e.event_timestamp) AS Последняя_активность
FROM TopBuyers tb
JOIN dim_customers c ON tb.customer_id = c.customer_id
LEFT JOIN fact_events e ON tb.customer_id = e.customer_id
GROUP BY c.customer_id, c.full_name, tb.Количество_заказов
ORDER BY tb.Количество_заказов DESC;

-- ЗАПРОС 5: Пользователи без заказов
SELECT 
    c.customer_id AS ID,
    c.full_name AS Клиент,
    c.email AS Email
FROM dim_customers c
LEFT JOIN fact_orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL
LIMIT 10;
