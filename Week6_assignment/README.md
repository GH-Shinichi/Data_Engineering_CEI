# Week 6 - Spark Intro

## What this week covered

- Spark architecture: Driver, Cluster Manager, and Executors and how they work together
- Lazy Evaluation and how Spark builds a DAG before executing anything
- Reading data from CSV and Parquet files with schema handling
- Performing filtering, column selection, renaming, and type casting on DataFrames
- Adding derived columns using `withColumn`
- Understanding narrow vs wide transformations and when shuffle occurs
- Predicate pushdown in Parquet and why it reduces data loaded into memory
- Null value handling and filtering
- Building a simple read → transform → filter → write pipeline
- Writing output to CSV and Parquet formats
- Best practices: why `.show()` is preferred over `.collect()` on large datasets

## Assignment

The assignment covers 15 questions split into coding and theory.

**Dataset:** A synthetic 500-row dataset (`source.csv`) was created covering product orders with columns: `product_id`, `category`, `price` (stored as string intentionally for casting), `base_price`, `user_id` (with ~5% nulls intentionally for null-handling), `region`, `priority`, `status`, and `amount`.

**Coding questions covered:**
- Q3: Reading CSV with `header=True` and `inferSchema=True`
- Q5: Filtering by category and selecting specific columns
- Q6: Renaming a column and casting price from String to Double
- Q8: Filtering with AND condition across two columns
- Q10: Adding a computed column (`final_price = base_price * 1.18`)
- Q12: Reading Parquet, filtering null `user_id` rows, writing cleaned output to CSV (validated null count = 0 after write)
- Q14: Filtering with OR condition across two columns
- Q15: Demonstrating `.show()` vs `.collect()` with reasoning

**Theory questions covered:**
Q1, Q2, Q4, Q7, Q9, Q11, Q13, Q15 — answers written in `Week6_Theory_Questions.docx`

## Files

- `source.csv` — synthetic dataset used for all coding questions
- `week6_assignment.py` — all coding questions in one script
- `Week6_Theory_Questions.docx` — written answers to all theory questions
- `source_parquet/` — Parquet version of the dataset (used in Q12)
- `cleaned_output/` — Q12 output CSV with nulls removed
