import warnings
warnings.filterwarnings("ignore")

from extract import extract_data
from transform import clean_and_log
from load import load_to_staging, create_dwh_and_load

def main():
    # 1. Extract
    customers, orders, payments, events, products = extract_data()
    
    # 2. Transform
    clean_cust, clean_ord, clean_pay, clean_ev, clean_prod = clean_and_log(
        customers, orders, payments, events, products
    )
    
    # 3. Load
    engine = load_to_staging(clean_cust, clean_ord, clean_pay, clean_ev, clean_prod)
    engine = create_dwh_and_load(engine)
    
    print("ETL процесс завершен успешно!")

if __name__ == "__main__":
    main()
