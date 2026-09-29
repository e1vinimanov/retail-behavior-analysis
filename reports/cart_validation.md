# Cart event validation

Input: add_to_cart(1).parquet
Rows: 7,541,117
Distinct non-null customers: 2,333,463
Earliest timestamp: 2022-06-23 00:10:20
Latest timestamp: 2022-12-08 00:09:55
Null counts: {'client_id': 0, 'timestamp': 0, 'sku': 0}
Exact repeated rows beyond first occurrence: 161,493
CSV size in bytes: 285,394,291

## Processing
All original rows, columns, ordering, and values preserved. No deduplication, imputation, filtering, or aggregation applied to the export. Strict timestamp parsing passed and reproduced the original strings. No timezone inferred. Repeated records retained because no event ID is supplied to establish whether they are logging errors or real repeated actions.

UTF-8 CSV, comma separator, header included, no added index. CSV read back in batches with explicit types and compared against every source value: PASS.

## PostgreSQL types
client_id BIGINT, timestamp TIMESTAMP WITHOUT TIME ZONE, sku BIGINT.
Null checks above support NOT NULL constraints for this source. Do not impose uniqueness on the event columns. This file contains cart events, not unique carts, customers, or orders.

## Analysis limitation
Timestamp range alone does not prove uninterrupted tracking. Seven-day conversion eligibility must use a common assumed observation cutoff supported by both cart and purchase data. Match customer AND product and require the purchase to follow the cart event.

## Reproduction
Run prepare_cart.py with the original Parquet path and output directory as positional arguments. Dependency: pyarrow 25.0.1.
