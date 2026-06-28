# Mutual Fund Data Analytics — Bluestock MF Capstone

## Day 3: Exploratory Data Analysis (EDA)

### Deliverables
| File | Description |
|------|-------------|
| `notebooks/EDA_Analysis.ipynb` | Jupyter notebook — 15 charts + 10 key EDA findings |
| `notebooks/run_eda.py` | Standalone script to regenerate all charts |
| `notebooks/charts/` | 15 exported high-resolution PNG charts |

### Charts
1. NAV Trend — All 40 Schemes (2022-2025) — 2023 Bull Run & 2024 Correction highlighted
2. AUM Growth — Grouped bar by fund house — SBI Rs.12.5L Cr dominance annotated
3. SIP Inflow Time-Series — Rs.31,002 Cr ATH (Dec 2025) annotated
4. Category Inflow Heatmap — months x categories, net inflow intensity
5 & 6. Investor Demographics — Age pie + SIP box plot + gender split
7. Geographic Distribution — State bar + T30 vs B30 pie
8. Folio Count Growth — 13.26 Cr to 26.12 Cr with milestones
9. NAV Return Correlation Matrix — 10 fund categories (Seaborn heatmap)
10. Sector Allocation Donut — aggregated equity fund holdings
11-15. Annual returns, SIP YoY growth, industry AUM, volatility, seasonality

### Stack
Python 3.11 | pandas | numpy | matplotlib | seaborn | plotly
Data: Synthetic, calibrated to AMFI published statistics (Jan 2022 - Dec 2025)
