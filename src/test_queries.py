import sqlite3

DB_PATH = 'bluestock_mf.db'

queries = {
    "Q1: Top 5 funds by AUM": """
        SELECT amfi_code, scheme_name, fund_house, aum_crore
        FROM fact_performance ORDER BY aum_crore DESC LIMIT 5;
    """,
    "Q2: Avg NAV per month (sample)": """
        SELECT amfi_code, SUBSTR(date, 1, 7) AS month, ROUND(AVG(nav), 4) AS avg_nav
        FROM fact_nav GROUP BY amfi_code, SUBSTR(date, 1, 7) LIMIT 5;
    """,
    "Q3: SIP YoY growth": """
        SELECT month, sip_inflow_crore, yoy_growth_pct
        FROM monthly_sip_inflows WHERE yoy_growth_pct IS NOT NULL ORDER BY month LIMIT 5;
    """,
    "Q4: Transactions by state (top 5)": """
        SELECT state, COUNT(*) AS total_txn, ROUND(SUM(amount_inr), 2) AS total_amt
        FROM fact_transactions GROUP BY state ORDER BY total_amt DESC LIMIT 5;
    """,
    "Q5: Funds with expense ratio < 1%": """
        SELECT amfi_code, scheme_name, expense_ratio_pct
        FROM fact_performance WHERE expense_ratio_pct < 1.0 ORDER BY expense_ratio_pct LIMIT 5;
    """,
    "Q6: Lumpsum per fund (top 5)": """
        SELECT ft.amfi_code, df.scheme_name, ROUND(SUM(ft.amount_inr), 2) AS total
        FROM fact_transactions ft JOIN dim_fund df ON ft.amfi_code = df.amfi_code
        WHERE ft.transaction_type = 'Lumpsum' GROUP BY ft.amfi_code ORDER BY total DESC LIMIT 5;
    """,
    "Q7: Top 10 stocks by portfolio weight": """
        SELECT stock_symbol, stock_name, ROUND(AVG(weight_pct), 2) AS avg_wt
        FROM portfolio_holdings GROUP BY stock_symbol ORDER BY avg_wt DESC LIMIT 5;
    """,
    "Q8: Best funds by 3yr return": """
        SELECT amfi_code, scheme_name, return_3yr_pct
        FROM fact_performance WHERE return_3yr_pct IS NOT NULL ORDER BY return_3yr_pct DESC LIMIT 5;
    """,
    "Q9: Monthly SIP accounts trend": """
        SELECT month, active_sip_accounts_crore, sip_aum_lakh_crore
        FROM monthly_sip_inflows ORDER BY month LIMIT 5;
    """,
    "Q10: Avg txn by age & gender": """
        SELECT age_group, gender, COUNT(*) AS n, ROUND(AVG(amount_inr), 2) AS avg_amt
        FROM fact_transactions GROUP BY age_group, gender ORDER BY avg_amt DESC LIMIT 5;
    """
}

conn = sqlite3.connect(DB_PATH)
for name, sql in queries.items():
    print(f"\n--- {name} ---")
    cur = conn.execute(sql)
    cols = [d[0] for d in cur.description]
    print(f"Columns: {cols}")
    rows = cur.fetchall()
    for r in rows:
        print(r)
conn.close()
print("\nAll 10 queries executed successfully.")
