"""Usage: python prepare_cart.py INPUT_PARQUET OUTPUT_DIRECTORY. Requires pyarrow."""
import sys
from pathlib import Path
import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.compute as pc
import pyarrow.csv as csv

source = Path(sys.argv[1])
out = Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
t = pq.read_table(source)
assert t.column_names == ['client_id', 'timestamp', 'sku']
assert pa.types.is_int64(t['client_id'].type) and pa.types.is_int64(t['sku'].type)
dates = pc.strptime(t['timestamp'], format='%Y-%m-%d %H:%M:%S', unit='s', error_is_null=False)
assert pc.strftime(dates, format='%Y-%m-%d %H:%M:%S').equals(t['timestamp'])
nulls = {c: t[c].null_count for c in t.column_names}
bounds = pc.min_max(dates).as_py()
customers = pc.count_distinct(t['client_id']).as_py()
unique_rows = t.group_by(t.column_names).aggregate([]).num_rows
duplicate_excess = t.num_rows - unique_rows
csv_path = out / 'add_to_cart.csv'
csv.write_csv(t, csv_path)
# Compare every value in the CSV to the source in bounded batches.
reader = csv.open_csv(csv_path, convert_options=csv.ConvertOptions(column_types=t.schema))
offset = 0
for batch in reader:
    read = pa.Table.from_batches([batch])
    assert read.equals(t.slice(offset, len(read)), check_metadata=False)
    offset += len(read)
assert offset == t.num_rows
report = f'''# Cart event validation

Input: {source.name}
Rows: {t.num_rows:,}
Distinct non-null customers: {customers:,}
Earliest timestamp: {bounds['min']}
Latest timestamp: {bounds['max']}
Null counts: {nulls}
Exact repeated rows beyond first occurrence: {duplicate_excess:,}
CSV size in bytes: {csv_path.stat().st_size:,}

## Processing
All original rows, columns, ordering, and values preserved. No deduplication, imputation, filtering, or aggregation applied to the export. Strict timestamp parsing passed and reproduced the original strings. No timezone inferred. Repeated records retained because no event ID is supplied to establish whether they are logging errors or real repeated actions.

UTF-8 CSV, comma separator, header included, no added index. CSV read back in batches with explicit types and compared against every source value: PASS.

## PostgreSQL types
client_id BIGINT, timestamp TIMESTAMP WITHOUT TIME ZONE, sku BIGINT.
Null checks above support NOT NULL constraints for this source. Do not impose uniqueness on the event columns. This file contains cart events, not unique carts, customers, or orders.

## Analysis limitation
Timestamp range alone does not prove uninterrupted tracking. Seven-day conversion eligibility must use a common assumed observation cutoff supported by both cart and purchase data. Match customer AND product and require the purchase to follow the cart event.

## Reproduction
Run prepare_cart.py with the original Parquet path and output directory as positional arguments. Dependency: pyarrow {pa.__version__}.
'''
(out/'cart_validation.md').write_text(report)
print(report)
