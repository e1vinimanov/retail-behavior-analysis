# Reproduce the project

## Quick start with aggregate results

Use Python with a compatible environment for the pinned dependencies. pandas 2.2.3 and Matplotlib 3.10.8 were used to validate the aggregate analysis during packaging. PyArrow 25.0.1 was recorded in the original source preparation report. The entire pinned environment has not been reinstalled as part of packaging.

From the project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/analyze_conversion.py
```

On Windows, activate with `.venv\Scripts\activate` instead.

Expected output: conversion percentages of 18.15%, 19.05% and 19.65%, a 14.04% repeat-purchase rate, and a 92.40% share of seven-day conversions within one day.

The script validates the monthly counts, checks the cumulative window ordering and recalculates percentages. It writes `data/processed/conversion_summary.csv` and `reports/figures/conversion_windows.png`.

Open `reports/retail_behavior_dashboard.html` in a browser. The dashboard is a fixed snapshot. It does not automatically refresh when SQL or CSV files change.

## Full source-to-result workflow

1. Download the original Synerise dataset from https://recsys.synerise.com/data-set and extract `product_buy.parquet` and `add_to_cart.parquet` into `data/raw/`. Do not commit raw data.
2. Prepare event CSV files:

```bash
python scripts/prepare_purchases.py data/raw/product_buy.parquet data/interim
python scripts/prepare_cart.py data/raw/add_to_cart.parquet data/interim
```

The scripts strictly parse timestamps, report nulls and duplicate rows, preserve records, and compare the exported CSV values with the source. They load a full Parquet table and calculate duplicate groups in memory, so memory usage exceeds the compressed file size. They are intended for these supplied files, not an unbounded production stream. Run normally without Python's `-O` flag because validation uses assertions.

3. Create or select a separate PostgreSQL database, `retail_behavior`, in DBeaver. Run `sql/00_schema.sql` in a fresh database. Do not rerun table creation if the tables already exist.
4. Import `data/interim/product_buy.csv` into `purchase_events` and `data/interim/add_to_cart.csv` into `cart_events`. Use UTF-8, comma separators, a header row, and timestamp format `yyyy-MM-dd HH:mm:ss`. Map the three columns by name. Import each file once to avoid doubling the event rows.
5. Run `sql/05_data_checks.sql`. Expected counts: 2,318,502 purchases and 7,541,117 cart events. Expected unique IDs: 909,210 buyers and 2,333,463 cart users.
6. Run analysis files `01` through `04` in order. Each creates or replaces its named view and selects its results. These are ordinary views and recompute their results when queried.
7. Export the following query outputs from DBeaver to `data/processed/`, using the filenames below. Use comma-separated CSV with column headers and no thousands separators.

| Query | Filename |
|---|---|
| `SELECT * FROM monthly_repeat_purchase ORDER BY cohort_month` | `monthly_repeat_purchase.csv` |
| `SELECT * FROM monthly_cart_conversion_7d ORDER BY cart_month` | `monthly_cart_conversion_7d.csv` |
| `SELECT * FROM conversion_windows` | `conversion_windows.csv` |

8. Run `python scripts/analyze_conversion.py` again. Validation is intentionally tied to this source snapshot. An assertion failure means the input, export or query result needs investigation.

The original preparation reports are preserved in `reports/`. Their sizes and checks describe the original exports, not a new run on the current computer. If reproducing, retain the new reports generated in `data/interim/` for comparison.
