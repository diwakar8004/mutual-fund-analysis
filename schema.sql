-- schema.sql
DROP TABLE IF EXISTS fact_transactions;
DROP TABLE IF EXISTS fact_nav;
DROP TABLE IF EXISTS fact_performance;
DROP TABLE IF EXISTS dim_fund;
DROP TABLE IF EXISTS dim_date;

-- Dimensions
CREATE TABLE dim_fund (
    amfi_code INTEGER PRIMARY KEY,
    scheme_name TEXT NOT NULL,
    fund_house TEXT,
    category TEXT,
    sub_category TEXT,
    risk_grade TEXT
);

CREATE TABLE dim_date (
    date_key TEXT PRIMARY KEY,
    year INTEGER,
    quarter INTEGER,
    month INTEGER,
    day INTEGER,
    day_of_week TEXT,
    is_weekend INTEGER
);

-- Facts
CREATE TABLE fact_nav (
    nav_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_key TEXT,
    amfi_code INTEGER,
    nav REAL NOT NULL,
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

CREATE TABLE fact_transactions (
    transaction_id TEXT PRIMARY KEY,
    date_key TEXT,
    amfi_code INTEGER,
    investor_id TEXT,
    transaction_type TEXT CHECK(transaction_type IN ('SIP', 'Lumpsum', 'Redemption')),
    amount REAL NOT NULL,
    units REAL,
    kyc_status TEXT CHECK(kyc_status IN ('Verified', 'Pending', 'Failed')),
    state TEXT,
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

CREATE TABLE fact_performance (
    performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER,
    expense_ratio REAL,
    return_1y REAL,
    return_3y REAL,
    return_5y REAL,
    aum_crores REAL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);