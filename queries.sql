-- queries.sql

-- 1. Top 5 Funds by AUM Size
SELECT f.scheme_name, p.aum_crores 
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
ORDER BY p.aum_crores DESC 
LIMIT 5;

-- 2. Average Historical Price (NAV) per Month Block
SELECT f.scheme_name, d.year, d.month, AVG(n.nav) as avg_monthly_nav
FROM fact_nav n
JOIN dim_date d ON n.date_key = d.date_key
JOIN dim_fund f ON n.amfi_code = f.amfi_code
GROUP BY n.amfi_code, d.year, d.month
ORDER BY d.year DESC, d.month DESC LIMIT 12;

-- 3. SIP Transaction Volume Growth by Year
SELECT d.year, COUNT(t.transaction_id) as total_sip_count, SUM(t.amount) as total_sip_capital
FROM fact_transactions t
JOIN dim_date d ON t.date_key = d.date_key
WHERE t.transaction_type = 'SIP'
GROUP BY d.year;

-- 4. Capital Distribution Mapped by State
SELECT state, COUNT(transaction_id) as transaction_volume, SUM(amount) as aggregate_capital_inflow
FROM fact_transactions
GROUP BY state
ORDER BY aggregate_capital_inflow DESC;

-- 5. Cost-Efficient Asset Alternatives (Expense Ratio < 1%)
SELECT f.scheme_name, (p.expense_ratio * 100) as expense_percentage
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
WHERE p.expense_ratio < 0.01;

-- 6. KYC Validation Status Breakdown by State
SELECT state, kyc_status, COUNT(*) as tracking_count
FROM fact_transactions
GROUP BY state, kyc_status
ORDER BY state;

-- 7. Total Outflow Capital Liquidated via Redemption Actions
SELECT f.scheme_name, SUM(t.amount) as total_liquidation_amount
FROM fact_transactions t
JOIN dim_fund f ON t.amfi_code = f.amfi_code
WHERE t.transaction_type = 'Redemption'
GROUP BY f.scheme_name;

-- 8. High Performers: 5-Year Return Horizon > 15%
SELECT f.scheme_name, (p.return_5y * 100) as five_year_return_pct
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
WHERE p.return_5y > 0.15;

-- 9. Net Retained Capital Balance per Fund
SELECT f.scheme_name,
       SUM(CASE WHEN t.transaction_type IN ('SIP', 'Lumpsum') THEN t.amount ELSE 0 END) - 
       SUM(CASE WHEN t.transaction_type = 'Redemption' THEN t.amount ELSE 0 END) AS net_retained_capital
FROM fact_transactions t
JOIN dim_fund f ON t.amfi_code = f.amfi_code
GROUP BY f.scheme_name;

-- 10. Lifecycle Peak Price Highs (Maximum NAV)
SELECT f.scheme_name, MAX(n.nav) as lifecycle_high_nav
FROM fact_nav n
JOIN dim_fund f ON n.amfi_code = f.amfi_code
GROUP BY n.amfi_code;