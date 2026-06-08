# Week 2 Assignment — E-Commerce Sales Database
**Celebal Summer Internship 2026 | Data Engineering Track**

---

## Overview

This assignment is part of the Celebal Summer Internship 2026. The task involves working with a relational database for a fictional Indian e-commerce company called ShopEase, which sells Electronics, Clothing, and Home products across India.

As a Junior Data Analyst, the goal was to write SQL queries to extract meaningful business insights from the company's sales data — covering everything from basic retrieval to transactions and ACID properties.

---

## About the Dataset

The database has four tables:

- **customers** — stores customer details including city, state, join date, and premium status
- **products** — stores product catalog with category, brand, price, and stock quantity
- **orders** — stores order records with status (Pending, Shipped, Delivered, Cancelled) and total amount
- **order_items** — stores individual line items per order with quantity, price, and discount

The tables are connected through Foreign Key relationships:
- customers (1) to orders (N)
- orders (1) to order_items (N)
- products (1) to order_items (N)

---

## Tools Used

- Python 3
- SQLite (via sqlite3 library)
- Pandas
- Jupyter Notebook

---

## Notebook Structure

The notebook is organized into five sections matching the assignment:

**Section A — SQL Basics**
Covers SELECT queries, table constraints, Primary Keys, UNIQUE, NOT NULL, and CHECK constraints with live demonstrations of what happens when constraints are violated.

**Section B — Filtering and Optimization**
Covers WHERE clause filtering, date range queries, index usage, and SARGable query writing. Includes a detailed explanation of why wrapping a column in a function breaks index usage and how to rewrite such queries correctly.

**Section C — Aggregation**
Covers COUNT, SUM, AVG, MIN, MAX with GROUP BY and HAVING. Each query includes a validation cell to cross-check aggregated results against raw data.

**Section D — Joins and Relationships**
Covers INNER JOIN, LEFT JOIN, three-table JOINs, and a full explanation of LEFT vs RIGHT vs FULL OUTER JOIN. Also covers Foreign Key relationships and referential integrity with a live demonstration.

**Section E — Advanced Concepts**
Covers CASE statements for conditional logic, CASE inside aggregate functions for single-row summaries, a full explanation of ACID properties with real-world examples, and a complete BEGIN/COMMIT/ROLLBACK transaction block.

---

## How to Run

1. Clone or download the repository
2. Make sure you have Python 3 installed with the following libraries:
   - sqlite3 (comes built-in with Python)
   - pandas

   If pandas is not installed, run:
   ```
   pip install pandas
   ```

3. Open the notebook in Jupyter:
   ```
   jupyter notebook "E-commerce Sales Database Handling.ipynb"
   ```

4. Go to Kernel and select Restart and Run All

The setup cells will automatically create the database, tables, indexes, and insert all sample data. No manual setup is needed.

---

## Key Design Decisions

**Dynamic queries over hardcoded values**
Wherever possible, queries use GROUP BY and DISTINCT to automatically handle all categories, statuses, or groups present in the data — rather than hardcoding specific values like WHERE category = 'Electronics'.

**Validation cells**
Every major query is followed by a validation cell that cross-checks the result from a different angle. For example, after counting delivered orders, a breakdown by all statuses is shown to confirm nothing is missing.

**Before and After comparisons**
For data-modifying operations (the transaction in Q27), the notebook captures the state of the database before and after, and prints a clear comparison.

**SARGable date filtering**
Date filters use range comparisons instead of functions on columns:
```sql
WHERE join_date >= '2024-01-01' AND join_date < '2025-01-01'
```
This keeps queries index-friendly, which matters at scale.

**Foreign Key enforcement**
SQLite does not enforce Foreign Keys by default. The notebook explicitly enables this at connection time with PRAGMA foreign_keys = ON, and includes a note explaining why this is necessary in SQLite but not in MySQL or PostgreSQL.

---

## Folder Structure

```
ASSGN_W2/
    E-commerce Sales Database Handling.ipynb    -- main notebook
    shopease.db                                 -- SQLite database (auto-created on first run)
    README.md                                   -- this file
```

---

## Author

**Mohd Nomaan**
B.Tech — Artificial Intelligence and Computer Science (3rd Year)
SKIT Jaipur
Celebal Summer Internship 2026 — Data Engineering Track
GitHub: GH-Shinichi
