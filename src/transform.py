import pandas as pd

def clean_and_log(customers, orders, payments, events, products):
    print("Data Quality START!")
    
    bad_records = []
    
    # Очистка customers
    customers['created_at_clean'] = pd.to_datetime(customers['created_at'], errors='coerce')
    bad_cust = customers[customers['created_at_clean'].isna()].copy()
    if not bad_cust.empty:
        bad_cust['error_reason'] = 'Invalid created_at date'
        bad_records.append(bad_cust)
    
    clean_customers = customers[customers['created_at_clean'].notna()].copy()
    clean_customers['created_at'] = clean_customers['created_at_clean']
    clean_customers = clean_customers.drop(columns=['created_at_clean'])
    
    # Очистка orders
    bad_order_id = orders[orders['customer_id'].isna()].copy()
    if not bad_order_id.empty:
        bad_order_id['error_reason'] = 'Missing customer_id'
        bad_records.append(bad_order_id)
    
    orders_valid_id = orders[orders['customer_id'].notna()].copy()
    orders_valid_id['order_timestamp_clean'] = pd.to_datetime(orders_valid_id['order_timestamp'], errors='coerce')
    bad_order_date = orders_valid_id[orders_valid_id['order_timestamp_clean'].isna()].copy()
    if not bad_order_date.empty:
        bad_order_date['error_reason'] = 'Invalid order_timestamp'
        bad_records.append(bad_order_date)
    
    clean_orders = orders_valid_id[orders_valid_id['order_timestamp_clean'].notna()].copy()
    clean_orders['order_timestamp'] = clean_orders['order_timestamp_clean']
    clean_orders = clean_orders.drop(columns=['order_timestamp_clean'])
    
    # Очистка payments
    payments['payment_method'] = payments['payment_method'].fillna('Unknown')
    payments['amount_clean'] = pd.to_numeric(payments['amount'], errors='coerce')
    bad_pay_amt = payments[payments['amount_clean'].isna()].copy()
    if not bad_pay_amt.empty:
        bad_pay_amt['error_reason'] = 'Invalid amount (error_amount)'
        bad_records.append(bad_pay_amt)
    
    payments_valid_amt = payments[payments['amount_clean'].notna()].copy()
    payments_valid_amt['payment_timestamp_clean'] = pd.to_datetime(payments_valid_amt['payment_timestamp'], errors='coerce')
    bad_pay_date = payments_valid_amt[payments_valid_amt['payment_timestamp_clean'].isna()].copy()
    if not bad_pay_date.empty:
        bad_pay_date['error_reason'] = 'Invalid payment_timestamp'
        bad_records.append(bad_pay_date)
    
    clean_payments = payments_valid_amt[payments_valid_amt['payment_timestamp_clean'].notna()].copy()
    clean_payments['amount'] = clean_payments['amount_clean']
    clean_payments['payment_timestamp'] = clean_payments['payment_timestamp_clean']
    clean_payments = clean_payments.drop(columns=['amount_clean', 'payment_timestamp_clean'])
    
    # Очистка events
    bad_ev_id = events[(events['event_id'] == 'BAD_ID') | (events['customer_id'].isna())].copy()
    if not bad_ev_id.empty:
        bad_ev_id['error_reason'] = 'Invalid event_id or customer_id'
        bad_records.append(bad_ev_id)
    
    events_valid_id = events[(events['event_id'] != 'BAD_ID') & (events['customer_id'].notna())].copy()
    events_valid_id['event_timestamp_clean'] = pd.to_datetime(events_valid_id['event_timestamp'], errors='coerce')
    bad_ev_date = events_valid_id[events_valid_id['event_timestamp_clean'].isna()].copy()
    if not bad_ev_date.empty:
        bad_ev_date['error_reason'] = 'Invalid event_timestamp (broken)'
        bad_records.append(bad_ev_date)
    
    clean_events = events_valid_id[events_valid_id['event_timestamp_clean'].notna()].copy()
    clean_events['event_timestamp'] = clean_events['event_timestamp_clean']
    clean_events = clean_events.drop(columns=['event_timestamp_clean'])
    
    # Очистка products
    products['price_clean'] = pd.to_numeric(products['price'], errors='coerce')
    bad_prod = products[products['price_clean'].isna()].copy()
    if not bad_prod.empty:
        bad_prod['error_reason'] = 'Invalid price (N/A)'
        bad_records.append(bad_prod)
    
    clean_products = products[products['price_clean'].notna()].copy()
    clean_products['price'] = clean_products['price_clean']
    clean_products = clean_products.drop(columns=['price_clean'])
    
    # Логирование ошибок
    if bad_records:
        error_log = pd.concat(bad_records, ignore_index=True)
        error_log.to_csv('error_log.csv', index=False)
        print(f"Найдено плохих записей: {len(error_log)}, сохранены в 'error_log.csv'")
    else:
        print("Ошибок в данных нет!")
    
    print("Очистка завершена!")
    return clean_customers, clean_orders, clean_payments, clean_events, clean_products
