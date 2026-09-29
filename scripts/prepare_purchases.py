"""Validate and export purchase events. Usage: python prepare_purchases.py INPUT OUTPUT_DIR"""
from pathlib import Path
import sys
import hashlib
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq
import pyarrow.csv as csv

source = Path(sys.argv[1])
out = Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
table = pq.read_table(source)
assert table.column_names == ['client_id', 'timestamp', 'sku'], table.column_names
assert pa.types.is_int64(table['client_id'].type)
assert pa.types.is_int64(table['sku'].type)
parsed = pc.strptime(table['timestamp'], format='%Y-%m-%d %H:%M:%S', unit='s', error_is_null=False)
normalized = pc.strftime(parsed, format='%Y-%m-%d %H:%M:%S')
assert normalized.equals(table['timestamp']), 'Unexpected timestamp representation'
nulls = {name: table[name].null_count for name in table.column_names}
unique_rows = table.group_by(table.column_names).aggregate([]).num_rows
extra_duplicates = table.num_rows - unique_rows
output = out / 'product_buy.csv'
csv.write_csv(table, output)
restored = csv.read_csv(output, convert_options=csv.ConvertOptions(column_types=table.schema))
assert restored.equals(table, check_metadata=False), 'CSV round-trip mismatch'
dates = pc.min_max(parsed).as_py()
report = f'''# Purchase-event export validation

Source: {source.name}, Synerise public retail dataset.
Rows: {table.num_rows:,}
Distinct non-null customer IDs: {pc.count_distinct(table['client_id']).as_py():,}
Earliest timestamp: {dates['min']}
Latest timestamp: {dates['max']}
Null counts by column: {nulls}
Exact duplicate rows beyond the first occurrence: {extra_duplicates:,}

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
Output bytes: {output.stat().st_size:,}
SHA-256: {hashlib.sha256(output.read_bytes()).hexdigest()}

## PostgreSQL import types
client_id: BIGINT
timestamp: TIMESTAMP WITHOUT TIME ZONE
sku: BIGINT
Do not define any of these columns, or their combination, as a primary key without additional evidence.

## Reproduction
Install pyarrow, then run:
python prepare_purchases.py /path/to/product_buy.parquet /path/to/output_folder
'''
(out / 'purchase_validation.md').write_text(report)
print(report)
