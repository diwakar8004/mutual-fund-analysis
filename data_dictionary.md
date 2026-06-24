# Corporate Data Catalog Dictionary: Mutual Fund Engine Architecture

## 1. dim_fund (Asset Master Catalog Dimension File Layer)
| Column Name | Logical Data Type | Key Constraints | Descriptive Context Mapping Definition |
| :--- | :--- | :--- | :--- |
| `amfi_code` | INTEGER | Primary Key | Unique 6-digit identifier key allocated to targeted structural asset. |
| `scheme_name`| TEXT | None | Standard corporate asset verification name identifier. |
| `fund_house` | TEXT | None | Regulatory Asset Management Company framework designation. |
| `category` | TEXT | None | Primary structural capitalization asset designation model classification. |
| `sub_category`| TEXT | None | Focused granular specialization scope context parameter. |
| `risk_grade` | TEXT | None | Categorical portfolio risk grouping standard framework designation. |

## 2. dim_date (Isochronous Time Calendar Dimension Engine)
| Column Name | Logical Data Type | Key Constraints | Descriptive Context Mapping Definition |
| :--- | :--- | :--- | :--- |
| `date_key` | TEXT | Primary Key | Standard target linkage timestamp vector matching string layout format `YYYY-MM-DD`. |
| `year` | INTEGER | None | Numerical representation of current tracking calendar cycle year. |
| `quarter` | INTEGER | None | Numerical indexing bounds separating tracking quarter cycles [1-4]. |
| `month` | INTEGER | None | Tracking calendar year structural indexing boundary layer identifier [1-12]. |
| `day` | INTEGER | None | Incremental positional tracking variable location counter within month [1-31]. |
| `day_of_week`| TEXT | None | String literal identifier marking current weekday target indexing reference. |
| `is_weekend` | INTEGER | None | Boolean constraint identifier variable checking tracking index status mapping [1=True, 0=False]. |

## 3. fact_transactions (Operational Transaction Matrix System)
| Column Name | Logical Data Type | Key Constraints | Descriptive Context Mapping Definition |
| :--- | :--- | :--- | :--- |
| `transaction_id`| TEXT | Primary Key | Cryptographically unique literal key assigned to specific trading entity records. |
| `date_key` | TEXT | Foreign Key | Temporal association mapping address routing link back to `dim_date`. |
| `amfi_code` | INTEGER | Foreign Key | Physical correlation linkage context mapping vector target to `dim_fund`. |
| `investor_id` | TEXT | None | Categorical identifier classification linking back to personal portfolio layers. |
| `transaction_type`| TEXT| Check Enum | Operational metric identifier defining transaction mechanics: `SIP`, `Lumpsum`, `Redemption`. |
| `amount` | REAL | Value > 0 | Aggregate raw currency volume allocation tracking total scale index. |
| `units` | REAL | None | Derived transaction balance quantity parameter based on historical NAV valuation windows. |
| `kyc_status` | TEXT | Check Enum | Compliance verification boundary validation markers: `Verified`, `Pending`, `Failed`. |
| `state` | TEXT | None | Physical localization region tag logging internal domestic state boundaries. |