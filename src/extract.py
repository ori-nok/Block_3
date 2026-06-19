import pandas as pd
import xml.etree.ElementTree as ET

def extract_data():
    df_customers = pd.read_csv('data/customers.csv')
    print(f"customers.csv: {len(df_customers)} ctpok")
    
    df_orders = pd.read_json('data/orders.json')
    print(f"orders.json: {len(df_orders)} ctpok")
    
    df_payments = pd.read_csv('data/payments.csv', sep='^')
    print(f"payments.csv: {len(df_payments)} ctpok")
    
    tree = ET.parse('data/events.xml')
    root = tree.getroot()
    events_list = []
    for event in root.findall('event'):
        event_dict = {}
        for child in event:
            event_dict[child.tag] = child.text
        events_list.append(event_dict)
    df_events = pd.DataFrame(events_list)
    print(f"events.xml: {len(df_events)} ctpok")
    
    df_products = pd.read_excel('data/products.xlsx')
    print(f"products.xlsx: {len(df_products)} ctpok")
    
    return df_customers, df_orders, df_payments, df_events, df_products
