# Week 8 Mini Project -- E-Commerce Order Analytics System

## Overview

This project was developed as part of the Week 8 Internship assignment
to build an end-to-end data analytics pipeline for an e-commerce order
management system.

The project covers the complete data lifecycle---from generating
realistic synthetic datasets to cleaning data, performing SQL analysis,
generating business reports, and validating data quality through
automated edge-case testing.

------------------------------------------------------------------------

# Project Objectives

-   Generate realistic e-commerce datasets with intentional data quality
    issues.
-   Clean and validate the generated datasets.
-   Build a SQLite database from the cleaned data.
-   Perform SQL-based business analysis.
-   Generate automated business reports.
-   Validate data quality using automated tests.

------------------------------------------------------------------------

# Technologies Used

-   Python 3
-   Pandas
-   SQLite3
-   SQL
-   Jupyter Notebook
-   unittest
-   pathlib

------------------------------------------------------------------------

# Project Structure

``` text
Week8_assignment/
│
├── README.md
├── Part 1/
│   ├── data_generation/
│   │   └── generate.ipynb
│   └── raw/
├── Part 2/
│   ├── data_cleaning/
│   │   └── cleaning_notebook.ipynb
│   └── cleaned_data/
├── Part 3/
│   ├── database_setup/
│   ├── database/
│   │   └── ecommerce.db
│   ├── basic_queries/
│   ├── intermediate_queries/
│   └── advanced_queries/
├── Part 4/
│   └── reporting/
│       └── generate_report.ipynb
└── Part 5/
    └── testing/
        └── test_edge_cases.ipynb
```

------------------------------------------------------------------------

# Project Workflow

## Part 1 -- Data Generation

Generated synthetic datasets for:

-   Customers
-   Products
-   Orders
-   Order Items

The generated data intentionally includes missing values, invalid
emails, incorrect dates, negative quantities, zero quantities, invalid
discounts, future-dated orders, and broken references for testing.

## Part 2 -- Data Cleaning

Performed:

-   Missing value handling
-   Date standardization
-   Email validation
-   Product name cleaning
-   Referential integrity checks
-   Data quality reporting

## Part 3 -- SQL Analysis

Loaded cleaned data into SQLite and implemented:

### Basic Analysis

-   Revenue by category
-   Top customers
-   Monthly order trends

### Intermediate Analysis

-   Customers without delivered orders
-   Products with more returns than purchases
-   Return rate by category

### Advanced Analysis

-   Running revenue by region
-   Product ranking using DENSE_RANK()
-   Window function based analytics

## Part 4 -- Reporting

Developed a reporting notebook that generates:

-   Total Orders
-   Total Revenue
-   Unique Customers
-   Top Products
-   Previous-period comparison

## Part 5 -- Edge Case Testing

Implemented automated tests for:

-   Orphan order IDs
-   Discounts greater than 100%
-   Zero quantity records
-   Future-dated orders

------------------------------------------------------------------------

# How to Run

1.  Run Part 1 -- Data Generation
2.  Run Part 2 -- Data Cleaning
3.  Run Part 3 -- Database Setup
4.  Run Basic Queries
5.  Run Intermediate Queries
6.  Run Advanced Queries
7.  Run Part 4 -- Reporting
8.  Run Part 5 -- Edge Case Testing

------------------------------------------------------------------------

# Learning Outcomes

This project demonstrates practical experience with:

-   Data Generation
-   Data Cleaning
-   SQL Analytics
-   SQLite Database Management
-   Python Automation
-   Business Reporting
-   Data Validation
-   Software Testing

------------------------------------------------------------------------

# Author

**Mohd Nomaan**

Week 8 Internship Mini Project
