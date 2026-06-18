import sqlite3
import os
import csv
import json
import xml.etree.ElementTree as ET

# Пути к базам и данным (поднимаемся на 3 уровня вверх до корня Block_3)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, 'target_database.db')
DATA_DIR = os.path.join(BASE_DIR, 'data')

def init_db(cursor):
    """1. Создание таблиц прямо из кода (с очисткой старых данных)"""
    print("Инициализация таблиц...")
    
    # Стираем старые таблицы, чтобы избежать ошибок дублирования при перезапусках
    cursor.execute("DROP TABLE IF EXISTS customers;")
    cursor.execute("DROP TABLE IF EXISTS products;")
    cursor.execute("DROP TABLE IF EXISTS orders;")
    cursor.execute("DROP TABLE IF EXISTS payments;")
    cursor.execute("DROP TABLE IF EXISTS events;")
    
    ddl_script = """
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        full_name TEXT,
        email TEXT,
        phone TEXT,
        city TEXT,
        created_at TEXT
    );

    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT,
        category TEXT,
        price REAL,
        currency TEXT,
        is_active TEXT
    );

    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        unit_price REAL,
        currency TEXT,
        order_timestamp TEXT,
        status TEXT
    );

    CREATE TABLE IF NOT EXISTS payments (
        payment_id INTEGER PRIMARY KEY,
        order_id INTEGER,
        payment_method TEXT,
        amount TEXT,
        currency TEXT,
        payment_timestamp TEXT
    );

    CREATE TABLE IF NOT EXISTS events (
        event_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        event_type TEXT,
        event_timestamp TEXT,
        product_id INTEGER
    );
    """
    cursor.executescript(ddl_script)
    print("Таблицы успешно созданы!")

def load_customers(cursor):
    """2. Загрузка customers.csv"""
    file_path = os.path.join(DATA_DIR, 'customers.csv')
    if not os.path.exists(file_path): 
        print("Предупреждение: Файл customers.csv не найден в папке data/")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute("""
                INSERT INTO customers (customer_id, full_name, email, phone, city, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (row['customer_id'], row['full_name'], row['email'], row['phone'], row['city'], row['created_at']))
    print("Данные клиентов загружены!")

def load_products(cursor):
    """3. Загрузка products.csv"""
    file_path = os.path.join(DATA_DIR, 'products.csv')
    if not os.path.exists(file_path):
        file_path = os.path.join(DATA_DIR, 'products.xlsx - products.csv')
    if not os.path.exists(file_path): 
        print("Предупреждение: Файл с продуктами не найден в папке data/")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute("""
                INSERT INTO products (product_id, product_name, category, price, currency, is_active)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (row['product_id'], row['product_name'], row['category'], row['price'], row['currency'], row['is_active']))
    print("Данные продуктов загружены!")

def load_orders(cursor):
    """4. Загрузка orders.json"""
    file_path = os.path.join(DATA_DIR, 'orders.json')
    if not os.path.exists(file_path): 
        print("Предупреждение: Файл orders.json не найден в папке data/")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        orders = json.load(f)
        for order in orders:
            cursor.execute("""
                INSERT INTO orders (order_id, customer_id, product_id, quantity, unit_price, currency, order_timestamp, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (order['order_id'], order['customer_id'], order['product_id'], order['quantity'], order['unit_price'], order['currency'], order['order_timestamp'], order['status']))
    print("Данные заказов загружены!")

def load_payments(cursor):
    """5. Загрузка payments.csv (Разделитель '^')"""
    file_path = os.path.join(DATA_DIR, 'payments.csv')
    if not os.path.exists(file_path): 
        print("Предупреждение: Файл payments.csv не найден в папке data/")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='^')
        for row in reader:
            cursor.execute("""
                INSERT INTO payments (payment_id, order_id, payment_method, amount, currency, payment_timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (row['payment_id'], row['order_id'], row['payment_method'], row['amount'], row['currency'], row['payment_timestamp']))
    print("Данные платежей загружены!")

def load_events(cursor):
    """6. Загрузка events.xml"""
    file_path = os.path.join(DATA_DIR, 'events.xml')
    if not os.path.exists(file_path): 
        print("Предупреждение: Файл events.xml не найден в папке data/")
        return

    tree = ET.parse(file_path)
    root = tree.getroot()
    for event in root.findall('event'):
        event_id = event.find('event_id').text
        customer_id = event.find('customer_id').text
        event_type = event.find('event_type').text
        event_timestamp = event.find('event_timestamp').text
        product_id = event.find('product_id').text

        cursor.execute("""
            INSERT INTO events (event_id, customer_id, event_type, event_timestamp, product_id)
            VALUES (?, ?, ?, ?, ?)
        """, (event_id, customer_id, event_type, event_timestamp, product_id))
    print("Данные логов (events) загружены!")

def main():
    print("=== СТАРТ ETL ПРОЦЕССА ===")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Последовательно запускаем шаги
    init_db(cursor)
    load_customers(cursor)
    load_products(cursor)
    load_orders(cursor)
    load_payments(cursor)
    load_events(cursor)
    
    conn.commit()
    conn.close()
    print("=== ETL ПРОЦЕСС УСПЕШНО ЗАВЕРШЕН! ===")

if __name__ == "__main__":
    main()