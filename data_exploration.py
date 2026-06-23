import pandas as pd
import os

data_dir = 'data/raw'
datasets = [
    '01_fund_master.csv',
    '02_nav_history.csv',
    '03_aum_by_fund_house.csv',
    '04_monthly_sip_inflows.csv',
    '05_category_inflows.csv',
    '06_industry_folio_count.csv',
    '07_scheme_performance.csv',
    '08_investor_transactions.csv',
    '09_portfolio_holdings.csv',
    '10_benchmark_indices.csv'
]

print("--- DATASET EXPLORATION ---")

fund_master_df = None

for file_name in datasets:
    file_path = os.path.join(data_dir, file_name)
    if os.path.exists(file_path):
        print(f"\n==================================================")
        print(f"Loading {file_name}...")
        df = pd.read_csv(file_path)
        
        print(f"--- Shape: {df.shape}")
        print(f"--- Data Types:")
        print(df.dtypes)
        print(f"--- Head (first 5 rows):")
        print(df.head())
        
        # Checking for missing values as a form of "anomaly" detection
        missing = df.isnull().sum()
        if missing.any():
            print(f"--- Anomalies (Missing values detected):")
            print(missing[missing > 0])
        else:
            print("--- No missing values detected.")
            
        if file_name == '01_fund_master.csv':
            fund_master_df = df
    else:
        print(f"\nWarning: {file_name} not found at {file_path}")

print("\n==================================================")
print("--- FUND MASTER DEEP DIVE ---")
if fund_master_df is not None:
    try:
        # Exploring the specified columns, assume typical naming conventions
        # if column names vary, this will throw an error and we can adjust
        print("Columns available:", list(fund_master_df.columns))
        
        # Let's dynamically find column names ignoring case
        cols_lower = {c.lower(): c for c in fund_master_df.columns}
        
        # Find Fund House
        fund_house_col = cols_lower.get('fund_house') or cols_lower.get('amc')
        if fund_house_col:
            print("\nUnique Fund Houses:")
            print(fund_master_df[fund_house_col].unique())
            
        # Find Category
        cat_col = cols_lower.get('category') or cols_lower.get('scheme_category')
        if cat_col:
            print("\nUnique Categories:")
            print(fund_master_df[cat_col].unique())
            
        # Find Sub-category
        subcat_col = cols_lower.get('sub_category') or cols_lower.get('sub-category') or cols_lower.get('scheme_type')
        if subcat_col:
            print("\nUnique Sub-categories:")
            print(fund_master_df[subcat_col].unique())
            
        # Find Risk Grade
        risk_col = cols_lower.get('risk_grade') or cols_lower.get('risk') or cols_lower.get('risk_level')
        if risk_col:
            print("\nUnique Risk Grades:")
            print(fund_master_df[risk_col].unique())
            
        # AMFI Scheme Code
        amfi_col = cols_lower.get('amfi_code') or cols_lower.get('scheme_code') or cols_lower.get('scheme code')
        if amfi_col:
            print("\nAMFI Scheme Code Structure (First 10 codes):")
            print(fund_master_df[amfi_col].head(10))
            print("Data type of AMFI Code:", fund_master_df[amfi_col].dtype)
            
    except Exception as e:
        print("Error during fund master exploration:", e)
else:
    print("fund_master.csv was not loaded. Skipping exploration.")
