# Mutual Fund Data Analytics

Welcome to the Mutual Fund Data Analytics project! This project aims to build a robust end-to-end data pipeline to ingest, process, and analyze mutual fund data, providing actionable insights through detailed dashboards and reports.

## Project Structure

The project is organized into the following standard data engineering directory structure:

```text
MUTUALFUNDDATAANALYTICS/
│
├── data/
│   ├── raw/                  # Immutable raw datasets downloaded and fetched via API
│   └── processed/            # Cleaned and transformed datasets ready for modeling
│
├── notebooks/                # Jupyter Notebooks for Exploratory Data Analysis (EDA)
│
├── sql/                      # SQL scripts for database schema creation and queries
│
├── dashboard/                # Power BI / Tableau dashboard files
│
├── reports/                  # Exported PDF/HTML reports and findings
│
├── .gitignore                # Ignored files and directories (venv, __pycache__, etc.)
├── requirements.txt          # Python project dependencies
├── etl_pipeline.py           # Day 1: Script to fetch live NAV data from mfapi.in
└── data_exploration.py       # Day 1: Script to load datasets and summarize metadata
```

## Setup & Installation

Follow these steps to set up the project locally:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/kvasuaditya-star/MUTUALFUNDSDATAANALYTICS.git
   cd MUTUALFUNDSDATAANALYTICS
   ```

2. **Create a Virtual Environment (Optional but recommended)**
   ```bash
   python -m venv venv
   
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Day 1 Executables

### 1. Data Ingestion Pipeline
The `etl_pipeline.py` script fetches real-time historical Net Asset Value (NAV) data from the `mfapi.in` public REST API for 6 key Mutual Fund schemes (including HDFC Top 100, SBI Bluechip, and others). The resulting JSON is parsed and saved automatically as CSV files in the `data/raw/` folder.

**Usage:**
```bash
python etl_pipeline.py
```

### 2. Exploratory Data Analysis
The `data_exploration.py` script automates the initial exploration of the 10 core CSV datasets (e.g., fund master, AUM, inflows, benchmark indices). It loads each file into memory using Pandas, checks for missing data anomalies, and outputs structural metadata (shape, data types, and head). It also runs a deep-dive specifically on the `01_fund_master.csv`.

**Usage:**
```bash
python data_exploration.py
```

---

*This project is continuously evolving. Further updates will include SQL database loading, advanced EDA, and interactive dashboards.*
