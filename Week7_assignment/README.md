# Delta Lake Incremental Data Processing — Week 7

## Overview

This week's assignment focuses on **incremental data processing using Delta Lake** on Databricks, applied to the Superstore retail dataset (9,994 order-line records). The core goal was to move beyond static, one-time data loads and implement a pipeline that can handle real-world change: new records arriving, existing records being updated, and records being logically deleted — all without losing data integrity or history.

This document explains what was built, the concepts behind each step, and what I actually learned working through it.

---

## Objective

Given a base dataset, simulate an incremental batch of changes and apply it to the existing table using Delta Lake's `MERGE` operation, while validating that the operation did exactly what it was supposed to — nothing more, nothing less.

---

## Dataset

**Superstore_raw.csv** — 9,994 rows, 21 columns (Order ID, Customer info, Product info, Sales, Quantity, Discount, Profit). This is order-line-level transactional data, not a clean dimension table, so the assignment logic was adapted to treat `Row_ID` as the natural primary key for MERGE matching.

---

## Concepts Covered This Week

### 1. Delta Lake Fundamentals

Delta Lake is a storage layer that sits on top of Parquet files and adds:
- **ACID transactions** — every write (insert, update, delete, merge) is atomic; it either fully succeeds or fully fails, so the table is never left in a half-written state.
- **A transaction log** (`_delta_log`) — every operation on a Delta table is recorded as a new **version**. This is what `DESCRIBE HISTORY` reads from.
- **Schema enforcement** — Delta rejects writes that don't match the table's expected schema, preventing silent data corruption.

**Why it matters here:** every `saveAsTable` and `MERGE` in this project created a new table version (0 → 1 → 2...), and I used `DESCRIBE HISTORY` throughout to inspect exactly what each operation did.

### 2. Delta Table Versioning & Time Travel

Because Delta keeps a full transaction log, you can query **any previous version** of a table using:
```python
spark.read.format("delta").option("versionAsOf", 1).table("my_table")
```
I used this to compare a row's state *before* the MERGE (version 1) against its state *after* (version 2) — proving the transaction log actually captured the change, not just trusting that the MERGE "probably worked."

**Learning:** Time Travel isn't just a novelty feature — it's a genuine debugging and auditing tool. If a MERGE ever produces unexpected results, you can always roll back and inspect exactly what the table looked like before.

### 3. MERGE Operations (UPSERT)

The `MERGE INTO` statement is Delta's mechanism for combining an "update if exists, insert if new" pattern into a single atomic operation:

```sql
MERGE INTO target
USING source
ON target.key = source.key
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
```

**Key thing I learned the hard way:** a blind `WHEN MATCHED THEN UPDATE SET *` updates *every* matched row regardless of whether the data actually changed. A more correct approach adds a condition:
```sql
WHEN MATCHED AND (target.Sales != source.Sales OR target.Ship_Mode != source.Ship_Mode) THEN UPDATE SET *
```
This only rewrites rows that genuinely changed — better for performance and more accurate to what "update" should mean.

**Real bug I hit:** Delta throws `DELTA_MULTIPLE_SOURCE_ROW_MATCHING_TARGET_ROW_IN_MERGE` if the *source* side of a MERGE has more than one row matching the same target row. This happened because my soft-delete batch and update batch weren't mutually exclusive — a `Row_ID` could appear in both. The fix was to explicitly filter the delete candidates to exclude any ID already used in the update batch, rather than assuming `.subtract()` would catch it (it didn't, because I was subtracting *after* modifying the values, so nothing matched anymore).

### 4. Slowly Changing Dimensions (SCD)

This is a data warehousing concept about **how to handle changes to dimension data over time**.

**SCD Type 1 — Overwrite:**
- Old value is simply replaced by the new value.
- No history is kept — the table only ever reflects the current truth.
- Simple, small table size, but you lose the ability to answer "what was this value last month?"
- This is what the main `superstore_master` table implements: matched rows get overwritten in place.

**SCD Type 2 — Preserve History:**
- Instead of overwriting, the old row is "expired" (marked `is_current = False`, given an `effective_end_date`) and a **new row** is inserted with the updated values and `is_current = True`.
- The table grows over time, but you can reconstruct the full history of any record.
- Implemented in a separate table (`superstore_scd2`) using a two-step MERGE pattern: first expire changed rows, then append new versions.

**Why both matter:** in a real analytics environment, you choose SCD1 when only the current state matters (e.g., a customer's current address for shipping), and SCD2 when historical accuracy matters (e.g., "what price was this product listed at when the order was placed?").

### 5. Soft Deletes

Rather than physically removing rows (`DELETE FROM`), this pipeline uses a **soft delete pattern**: an `is_deleted` boolean flag is set to `True` on matched rows instead of removing them.

**Why:** physical deletes lose information permanently and can break downstream joins or audit trails. Soft deletes let you filter out "deleted" records in queries (`WHERE is_deleted = False`) while still retaining them for auditing, recovery, or historical analysis.

### 6. Incremental Processing Design

Rather than reprocessing the entire dataset every time, incremental processing means only the **changed subset** (the "delta") is applied to the target table. This is the foundation of how real production data pipelines stay efficient at scale — a table with millions of rows doesn't get fully rewritten every time 20 rows change.

In this project, the incremental batch was generated **dynamically** from the existing table (sampling real rows, modifying values, assigning new IDs) rather than hardcoded — closer to how a real upstream system would deliver change data.

---

## Validation Strategy

A MERGE that "runs without error" isn't proof it did the right thing. This project validates at every layer:

| Validation | What it proves |
|---|---|
| Delta's native `operationMetrics` (from `DESCRIBE HISTORY`) | The authoritative, Delta-internal record of exactly how many rows were inserted/updated/deleted |
| Row count reconciliation | No rows were silently gained or lost |
| Duplicate `Row_ID` check | The MERGE didn't create ambiguous/duplicate keys |
| Spot-checks on updates, inserts, deletes | The *values* changed correctly, not just the counts |
| Untouched-row integrity check | Rows that should **not** have changed stayed byte-identical — this is the strongest proof the MERGE was surgically precise |
| Sales aggregate reconciliation | A business-level sanity check — does the total make sense given what changed? |
| Time Travel comparison | Confirms the transaction log captured the before/after state correctly |

---

## A Real Data Quality Issue I Encountered

While validating the Sales aggregate (checking `before_total_sales` vs `after_total_sales`), the query failed with a type-cast error: a text value (a fragment of a product name) was sitting inside the `Sales` column for a handful of rows.

**Root cause:** several `Product_Name` values in the raw CSV contain both commas and embedded double-quotes (e.g., `Ampad Poly Cover Wirebound Steno Book, 6"" x 9"" Assorted Colors`). The initial CSV read didn't specify quote/escape handling, so Spark's parser misaligned columns for those specific rows, shifting text into the numeric `Sales` field.

**Fix:** explicitly setting `quote='"'`, `escape='"'`, and `multiLine=True` in `spark.read.csv(...)` told Spark how to correctly interpret escaped quotes inside quoted fields, resolving the misalignment.

**Takeaway:** this is a good example of why validation matters — the MERGE logic itself was correct throughout, but a silent data quality issue from the very first read wasn't caught until an aggregate-level check surfaced it several steps later. Row count and duplicate checks alone wouldn't have caught this; it took an actual value-level sanity check.

---

## Tech Stack

- **Databricks** (Unity Catalog, Serverless compute)
- **PySpark** (DataFrame API + Spark SQL)
- **Delta Lake** (MERGE, Time Travel, transaction log, `operationMetrics`)

---

## Repository Structure

```
Week7_assignment/
├── data/
│   └── Superstore_raw.csv
├── notebooks/
│   └── delta_scd_assignment.ipynb
├── screenshots/
│   ├── data_loading/
│   ├── data_cleaning/
│   ├── scd1/
│   ├── scd2/
│   └── validation/
└── README.md
```

---

## Key Takeaways

1. **A MERGE that runs isn't a MERGE that's correct** — validation at multiple levels (metrics, counts, spot-checks, integrity checks) is what actually proves correctness.
2. **SCD1 vs SCD2 is a design decision, not just a technical pattern** — it depends entirely on whether historical accuracy matters for the use case.
3. **Delta's transaction log is a real audit trail**, not just a rollback mechanism — `operationMetrics` gave a more trustworthy answer than anything I could have calculated manually.
4. **Data quality issues can hide in plain sight** — a CSV parsing edge case didn't surface until several steps downstream, reinforcing why aggregate-level checks matter even after row-count and duplicate checks pass.
