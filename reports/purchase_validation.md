# Purchase-event export validation

Source: product_buy.parquet, Synerise public retail dataset.
Rows: 2,318,502
Distinct non-null customer IDs: 909,210
Earliest timestamp: 2022-06-23 00:12:15
Latest timestamp: 2022-12-08 00:09:15
Null counts by column: {'client_id': 0, 'timestamp': 0, 'sku': 0}
Exact duplicate rows beyond the first occurrence: 380,903

## Processing decisions
- All three original columns, original row order, and all records are preserved.
- Timestamp strings were parsed strictly and checked against the original representation. All non-null values passed. Export retains YYYY-MM-DD HH:MM:SS text without an inferred timezone.
- No rows were deleted, imputed, deduplicated, or aggregated. Without an event ID or order ID, identical rows cannot safely be classified as errors.
- Customer and product IDs remain 64-bit integers. Their uniqueness is not assumed.
- Purchase events must not be described as distinct orders or customers.
- This export covers purchases only. Other event files and page visits are not included.

## Export validation
UTF-8, comma-separated, header included, no generated index column.
CSV was read back with explicit types and compared against every source value: PASS.
Output bytes: 87,740,414
SHA-256: 9eafc21bdc9221dc52afcd3f435947799b26fcdf3ed8070432619d770c882602

## PostgreSQL import types
client_id: BIGINT
timestamp: TIMESTAMP WITHOUT TIME ZONE
sku: BIGINT
Do not define any of these columns, or their combination, as a primary key without additional evidence.

## Reproduction
Install pyarrow, then run:
python prepare_purchases.py /path/to/product_buy.parquet /path/to/output_folder
