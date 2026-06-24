import os
import sqlite3
import pandas as pd
from sqlalchemy import create_engine

DB_PATH = 'bluestock_mf.db'
SCHEMA_PATH = r'sql\schema.sql'
PROCESSED_DIR = r'data\processed'

def init_db():
    # Remove old DB if it exists so re-runs don't hit duplicate errors
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("Removed old database.")
    
    print("Initializing database schema...")
    with sqlite3.connect(DB_PATH) as conn:
        with open(SCHEMA_PATH, 'r') as f:
            schema_script = f.read()
        conn.executescript(schema_script)

def load_data():
    print("Loading datasets into SQLite...")
    engine = create_engine(f'sqlite:///{DB_PATH}')
    
    file_table_mapping = {
        '01_fund_master.csv': 'dim_fund',
        '02_nav_history.csv': 'fact_nav',
        '03_aum_by_fund_house.csv': 'fact_aum',
        '04_monthly_sip_inflows.csv': 'monthly_sip_inflows',
        '05_category_inflows.csv': 'category_inflows',
        '06_industry_folio_count.csv': 'industry_folio_count',
        '07_scheme_performance.csv': 'fact_performance',
        '08_investor_transactions.csv': 'fact_transactions',
        '09_portfolio_holdings.csv': 'portfolio_holdings',
        '10_benchmark_indices.csv': 'benchmark_indices'
    }
    
    for filename, table_name in file_table_mapping.items():
        file_path = os.path.join(PROCESSED_DIR, filename)
        if not os.path.exists(file_path):
            print(f"Warning: {file_path} not found.")
            continue
            
        print(f"Loading {filename} into table {table_name}...")
        df = pd.read_csv(file_path)
        # We use if_exists='append' to respect the schema created by schema.sql
        df.to_sql(table_name, engine, if_exists='append', index=False)
        print(f"Loaded {len(df)} rows into {table_name}.")

if __name__ == '__main__':
    init_db()
    load_data()
    print("Database loading completed successfully.")
