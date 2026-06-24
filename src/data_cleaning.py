import pandas as pd
import os

RAW_DIR = r'data\raw'
PROCESSED_DIR = r'data\processed'

def clean_nav_history():
    print("Cleaning 02_nav_history.csv...")
    df = pd.read_csv(os.path.join(RAW_DIR, '02_nav_history.csv'))
    
    # Parse dates to datetime
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    # Validate NAV > 0
    df['nav'] = pd.to_numeric(df['nav'], errors='coerce')
    df = df[df['nav'] > 0]
    
    # Remove duplicates
    df = df.drop_duplicates(subset=['amfi_code', 'date'])
    
    # Sort by amfi_code + date
    df = df.sort_values(['amfi_code', 'date'])
    
    # Forward-fill missing NAV (holidays)
    def fill_missing_dates(group):
        if group.empty:
            return group
        idx = pd.date_range(group['date'].min(), group['date'].max())
        group = group.set_index('date').reindex(idx)
        group['amfi_code'] = group['amfi_code'].ffill()
        group['nav'] = group['nav'].ffill()
        group = group.rename_axis('date').reset_index()
        return group

    # Pandas groupby apply with resample/reindex
    df = df.groupby('amfi_code', group_keys=False).apply(fill_missing_dates).reset_index(drop=True)
    
    # Ensure dates are stored in YYYY-MM-DD
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')
    
    df.to_csv(os.path.join(PROCESSED_DIR, '02_nav_history.csv'), index=False)
    print(f"Cleaned 02_nav_history.csv: {len(df)} rows")

def clean_investor_transactions():
    print("Cleaning 08_investor_transactions.csv...")
    df = pd.read_csv(os.path.join(RAW_DIR, '08_investor_transactions.csv'))
    
    # Fix date formats
    df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce').dt.strftime('%Y-%m-%d')
    df = df.dropna(subset=['transaction_date'])
    
    # Standardise transaction_type
    def std_trans(x):
        x = str(x).upper().strip()
        if 'SIP' in x: return 'SIP'
        if 'LUMP' in x: return 'Lumpsum'
        if 'REDEMP' in x or 'WITHDRAW' in x: return 'Redemption'
        return 'Other'
    
    df['transaction_type'] = df['transaction_type'].apply(std_trans)
    
    # Validate amount > 0
    df['amount_inr'] = pd.to_numeric(df['amount_inr'], errors='coerce')
    df = df[df['amount_inr'] > 0]
    
    # Check KYC status values
    valid_kyc = ['Verified', 'Pending', 'Rejected']
    df['kyc_status'] = df['kyc_status'].apply(lambda x: str(x).strip().title() if pd.notna(x) and str(x).strip().title() in valid_kyc else 'Unknown')
    
    # Drop duplicates
    df = df.drop_duplicates()
    
    df.to_csv(os.path.join(PROCESSED_DIR, '08_investor_transactions.csv'), index=False)
    print(f"Cleaned 08_investor_transactions.csv: {len(df)} rows")

def clean_scheme_performance():
    print("Cleaning 07_scheme_performance.csv...")
    df = pd.read_csv(os.path.join(RAW_DIR, '07_scheme_performance.csv'))
    
    # Validate return values are numeric
    return_cols = ['return_1yr_pct', 'return_3yr_pct', 'return_5yr_pct', 'benchmark_3yr_pct', 'alpha', 'beta', 'sharpe_ratio', 'sortino_ratio']
    for col in return_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Flag negative Sharpe ratios
    if 'sharpe_ratio' in df.columns:
        df['negative_sharpe_flag'] = (df['sharpe_ratio'] < 0).astype(int)
    
    # Check expense_ratio range (0.1% - 2.5%)
    if 'expense_ratio_pct' in df.columns:
        df['expense_ratio_pct'] = pd.to_numeric(df['expense_ratio_pct'], errors='coerce')
        df = df[(df['expense_ratio_pct'] >= 0.1) & (df['expense_ratio_pct'] <= 2.5)]
    
    # Drop duplicates
    df = df.drop_duplicates()
    
    df.to_csv(os.path.join(PROCESSED_DIR, '07_scheme_performance.csv'), index=False)
    print(f"Cleaned 07_scheme_performance.csv: {len(df)} rows")

def clean_other_datasets():
    print("Cleaning other datasets...")
    other_files = [
        '01_fund_master.csv', '03_aum_by_fund_house.csv', '04_monthly_sip_inflows.csv',
        '05_category_inflows.csv', '06_industry_folio_count.csv', '09_portfolio_holdings.csv',
        '10_benchmark_indices.csv'
    ]
    
    for f in other_files:
        path = os.path.join(RAW_DIR, f)
        if not os.path.exists(path):
            continue
            
        df = pd.read_csv(path)
        
        # Generic cleaning
        df = df.drop_duplicates()
        
        # If it has a date col, parse it
        for col in ['date', 'month', 'portfolio_date']:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                df = df.dropna(subset=[col]) # Drop if date couldn't be parsed
                if col == 'month':
                    df[col] = df[col].dt.strftime('%Y-%m')
                else:
                    df[col] = df[col].dt.strftime('%Y-%m-%d')
        
        df.to_csv(os.path.join(PROCESSED_DIR, f), index=False)
        print(f"Cleaned {f}: {len(df)} rows")

if __name__ == '__main__':
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    clean_nav_history()
    clean_investor_transactions()
    clean_scheme_performance()
    clean_other_datasets()
    print("Data cleaning completed successfully.")
