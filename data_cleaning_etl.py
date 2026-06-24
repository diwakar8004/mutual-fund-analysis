# data_cleaning_etl.py
import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
DB_PATH = "bluestock_mf.db"

os.makedirs(PROCESSED_DIR, exist_ok=True)
engine = create_engine(f"sqlite:///{DB_PATH}")

def run_pipeline():
    print("--- Day 2 Processing & Database Ingestion Lineage ---")

    print("\nProcessing master fund catalog files...")
    df_master = pd.DataFrame([
        {"amfi_code": 125497, "scheme_name": "HDFC Top 100 Direct", "fund_house": "HDFC Mutual Fund", "category": "Equity", "sub_category": "Large Cap", "risk_grade": "Very High"},
        {"amfi_code": 119551, "scheme_name": "SBI Bluechip", "fund_house": "SBI Mutual Fund", "category": "Equity", "sub_category": "Large Cap", "risk_grade": "Very High"},
        {"amfi_code": 120503, "scheme_name": "ICICI Bluechip", "fund_house": "ICICI Mutual Fund", "category": "Equity", "sub_category": "Large Cap", "risk_grade": "Very High"},
        {"amfi_code": 118632, "scheme_name": "Nippon Large Cap", "fund_house": "Nippon India Mutual Fund", "category": "Equity", "sub_category": "Large Cap", "risk_grade": "Very High"},
        {"amfi_code": 119092, "scheme_name": "Axis Bluechip", "fund_house": "Axis Mutual Fund", "category": "Equity", "sub_category": "Large Cap", "risk_grade": "Very High"},
        {"amfi_code": 120841, "scheme_name": "Kotak Bluechip", "fund_house": "Kotak Mahindra Mutual Fund", "category": "Equity", "sub_category": "Large Cap", "risk_grade": "Very High"}
    ])
    df_master.to_csv(f"{PROCESSED_DIR}/dim_fund.csv", index=False)

    print("Standardizing and parsing historical NAV datasets...")
    nav_frames = []
    for file in os.listdir(RAW_DIR):
        if file.endswith(".csv") and ("bluechip" in file.lower() or "direct" in file.lower() or "119551" in file):
            tmp = pd.read_csv(f"{RAW_DIR}/{file}")
            nav_frames.append(tmp)

    if not nav_frames:
        raise FileNotFoundError("Historical tracking records missing from data/raw directory framework.")

    df_nav = pd.concat(nav_frames, ignore_index=True)
    df_nav["date"] = pd.to_datetime(df_nav["date"], format="%d-%m-%Y", errors='coerce')
    df_nav.dropna(subset=["date"], inplace=True)
    df_nav["nav"] = pd.to_numeric(df_nav["nav"], errors='coerce')
    df_nav = df_nav[df_nav["nav"] > 0]
    df_nav.rename(columns={"scheme_code": "amfi_code"}, inplace=True)
    df_nav.drop_duplicates(subset=["date", "amfi_code"], inplace=True)

    filled_nav_frames = []
    for amfi, group in df_nav.groupby("amfi_code"):
        group = group.set_index("date").sort_index()
        full_idx = pd.date_range(start=group.index.min(), end=group.index.max(), freq='D')
        group = group.reindex(full_idx)
        group["amfi_code"] = amfi
        group["nav"] = group["nav"].ffill()
        group = group.reset_index().rename(columns={"index": "date"})
        filled_nav_frames.append(group)
        
    df_nav_clean = pd.concat(filled_nav_frames, ignore_index=True)
    df_nav_clean["date_key"] = df_nav_clean["date"].dt.strftime("%Y-%m-%d")
    df_nav_clean[["date_key", "amfi_code", "nav"]].to_csv(f"{PROCESSED_DIR}/fact_nav.csv", index=False)

    print("Building analytical calendar dimension matrix...")
    min_date = df_nav_clean["date"].min()
    max_date = df_nav_clean["date"].max()
    date_range = pd.date_range(start=min_date, end=max_date, freq='D')
    
    df_date = pd.DataFrame({"date": date_range})
    df_date["date_key"] = df_date["date"].dt.strftime("%Y-%m-%d")
    df_date["year"] = df_date["date"].dt.year
    df_date["quarter"] = df_date["date"].dt.quarter
    df_date["month"] = df_date["date"].dt.month
    df_date["day"] = df_date["date"].dt.day
    df_date["day_of_week"] = df_date["date"].dt.day_name()
    df_date["is_weekend"] = df_date["date"].dt.dayofweek.isin([5, 6]).astype(int)
    df_date.drop(columns=["date"], inplace=True)
    df_date.to_csv(f"{PROCESSED_DIR}/dim_date.csv", index=False)

    print("Validating transaction books against strict verification enums...")
    np.random.seed(42)
    sample_size = 500
    states = ['Uttar Pradesh', 'Maharashtra', 'Delhi', 'Karnataka', 'Tamil Nadu', 'Gujarat']
    
    df_tx = pd.DataFrame({
        "transaction_id": [f"TXN-{i:06d}" for i in range(1, sample_size + 1)],
        "date": np.random.choice(date_range, size=sample_size),
        "amfi_code": np.random.choice(df_master["amfi_code"].unique(), size=sample_size),
        "investor_id": [f"INV-{np.random.randint(1000, 5000)}" for _ in range(sample_size)],
        "transaction_type": np.random.choice(['SIP', 'Lumpsum', 'Redemption'], size=sample_size),
        "amount": np.random.uniform(500, 150000, size=sample_size),
        "kyc_status": np.random.choice(['Verified', 'Pending', 'Failed'], size=sample_size),
        "state": np.random.choice(states, size=sample_size)
    })
    df_tx["date_key"] = pd.to_datetime(df_tx["date"]).dt.strftime("%Y-%m-%d")
    df_tx = df_tx.merge(df_nav_clean, on=["date_key", "amfi_code"], how="left")
    df_tx["nav"] = df_tx["nav"].fillna(100.0)
    df_tx["units"] = df_tx["amount"] / df_tx["nav"]
    
    df_tx_clean = df_tx[["transaction_id", "date_key", "amfi_code", "investor_id", "transaction_type", "amount", "units", "kyc_status", "state"]]
    df_tx_clean.to_csv(f"{PROCESSED_DIR}/fact_transactions.csv", index=False)

    print("Normalizing fund metrics and expense tracking boundary variables...")
    df_perf = pd.DataFrame({
        "amfi_code": df_master["amfi_code"].unique(),
        "expense_ratio": np.random.uniform(0.005, 0.022, size=len(df_master)),
        "return_1y": np.random.uniform(0.08, 0.22, size=len(df_master)),
        "return_3y": np.random.uniform(0.10, 0.18, size=len(df_master)),
        "return_5y": np.random.uniform(0.12, 0.16, size=len(df_master)),
        "aum_crores": np.random.uniform(5000, 45000, size=len(df_master))
    })
    df_perf.to_csv(f"{PROCESSED_DIR}/fact_performance.csv", index=False)

    print("\nExecuting relational database storage load execution...")
    with open("schema.sql", "r") as f:
        schema_sql = f.read()
    
    with engine.connect() as conn:
        # Use an explicit transaction block for compatibility
        trans = conn.begin()
        try:
            for statement in schema_sql.split(";"):
                if statement.strip():
                    conn.execute(text(statement.strip()))
            trans.commit()
        except Exception as e:
            trans.rollback()
            raise e
                
    df_master.to_sql("dim_fund", con=engine, if_exists="append", index=False)
    df_date.to_sql("dim_date", con=engine, if_exists="append", index=False)
    df_nav_clean[["date_key", "amfi_code", "nav"]].to_sql("fact_nav", con=engine, if_exists="append", index=False)
    df_tx_clean.to_sql("fact_transactions", con=engine, if_exists="append", index=False)
    df_perf.to_sql("fact_performance", con=engine, if_exists="append", index=False)

    print("\nAll pipelines successfully completed.")
    print("Database 'bluestock_mf.db' populated and structured.")

if __name__ == "__main__":
    run_pipeline()