-- Удаляем старые таблицы
DROP TABLE IF EXISTS fact_payments CASCADE;
DROP TABLE IF EXISTS fact_events CASCADE;
DROP TABLE IF EXISTS fact_orders CASCADE;
DROP TABLE IF EXISTS dim_products CASCADE;
DROP TABLE IF EXISTS dim_customers CASCADE;

-- Создаем справочник клиентов
CREATE TABLE dim_customers (
    customer_id BIGINT PRIMARY KEY,
    full_name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    city VARCHAR(100),
    created_at TIMESTAMP
);

-- Создаем справочник товаров
CREATE TABLE dim_products (
    product_id BIGINT PRIMARY KEY,
    product_name VARCHAR(255),
    category VARCHAR(100),
    price NUMERIC(10,2),
    currency VARCHAR(10),
    is_active BOOLEAN
);

-- Создаем таблицу фактов заказов
CREATE TABLE fact_orders (
    order_id BIGINT PRIMARY KEY,
    customer_id BIGINT REFERENCES dim_customers(customer_id),
    product_id BIGINT REFERENCES dim_products(product_id),
    quantity INT,
    unit_price NUMERIC(10,2),
    currency VARCHAR(10),
    order_timestamp TIMESTAMP,
    status VARCHAR(50)
);

-- Создаем таблицу фактов платежей
CREATE TABLE fact_payments (
    payment_id BIGINT PRIMARY KEY,
    order_id BIGINT REFERENCES fact_orders(order_id),
    payment_method VARCHAR(50),
    amount NUMERIC(10,2),
    currency VARCHAR(10),
    payment_timestamp TIMESTAMP
);

-- Создаем таблицу фактов событий
CREATE TABLE fact_events (
    event_id BIGINT PRIMARY KEY,
    customer_id BIGINT REFERENCES dim_customers(customer_id),
    product_id BIGINT REFERENCES dim_products(product_id),
    event_type VARCHAR(50),
    event_timestamp TIMESTAMP
);

-- ЗАГРУЗКА ДАННЫХ ИЗ STAGING

-- Клиенты
INSERT INTO dim_customers
SELECT DISTINCT
    CAST(customer_id AS BIGINT),
    full_name, email, phone, city,
    CAST(created_at AS TIMESTAMP)
FROM stg_customers;

-- Товары
INSERT INTO dim_products
SELECT DISTINCT
    CAST(product_id AS BIGINT),
    product_name, category,
    CAST(price AS NUMERIC(10,2)),
    currency, is_active
FROM stg_products;

-- Заказы
INSERT INTO fact_orders
SELECT DISTINCT ON (CAST(order_id AS BIGINT))
    CAST(order_id AS BIGINT),
    CAST(customer_id AS BIGINT),
    CAST(product_id AS BIGINT),
    CAST(quantity AS INT),
    CAST(unit_price AS NUMERIC(10,2)),
    currency,
    CAST(order_timestamp AS TIMESTAMP),
    status
FROM stg_orders
WHERE CAST(customer_id AS BIGINT) IN (SELECT customer_id FROM dim_customers)
  AND CAST(product_id AS BIGINT) IN (SELECT product_id FROM dim_products)
ORDER BY CAST(order_id AS BIGINT);

-- Платежи
INSERT INTO fact_payments
SELECT DISTINCT ON (CAST(payment_id AS BIGINT))
    CAST(payment_id AS BIGINT),
    CAST(order_id AS BIGINT),
    payment_method,
    CAST(amount AS NUMERIC(10,2)),
    currency,
    CAST(payment_timestamp AS TIMESTAMP)
FROM stg_payments
WHERE CAST(order_id AS BIGINT) IN (SELECT order_id FROM fact_orders)
ORDER BY CAST(payment_id AS BIGINT);

-- События
INSERT INTO fact_events
SELECT DISTINCT ON (CAST(event_id AS BIGINT))
    CAST(event_id AS BIGINT),
    CAST(customer_id AS BIGINT),
    CAST(product_id AS BIGINT),
    event_type,
    CAST(event_timestamp AS TIMESTAMP)
FROM stg_events
WHERE CAST(customer_id AS BIGINT) IN (SELECT customer_id FROM dim_customers)
  AND CAST(product_id AS BIGINT) IN (SELECT product_id FROM dim_products)
ORDER BY CAST(event_id AS BIGINT);
