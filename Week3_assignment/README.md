Week 3 Assignment - SQL Analysis Using Subqueries, CTEs and Window Functions
Overview
This assignment focuses on performing sales analysis using SQL concepts such as Subqueries, Common Table Expressions (CTEs), Window Functions, and Joins.
The Superstore dataset was imported into SQLite through a Jupyter Notebook environment. The raw dataset was then normalized into separate tables for customers, products, and orders before performing analytical queries.

Dataset
Dataset Used: Superstore Sales Dataset
The dataset contains information related to:

Customers
Products
Orders
Sales
Quantity
Profit


Data Preparation
The following steps were performed before analysis:

Loaded the Superstore dataset into Pandas.
Connected to a SQLite database.
Created a raw table named superstore_raw.
Created separate tables:

customers
products
orders


Inserted data using SELECT DISTINCT.
Validated data for:

Missing values
Duplicate records
Row counts


Created indexes on frequently used columns to improve query performance.


SQL Concepts Used
Subqueries

Orders with sales above average sales
Highest sales order for each customer

Common Table Expressions (CTEs)

Total sales per customer
Customers with above-average sales

Window Functions

Customer ranking based on total sales
Row numbering within customer orders
Top customers based on sales

Joins

Combined customer information with sales summaries


Assignment Tasks Completed
Step 1 - Database Setup

Imported dataset into SQLite
Created customers table
Created products table
Created orders table
Inserted records using SELECT DISTINCT

Step 2 - SQL Analysis

Find orders with sales greater than average sales
Find highest sales order for each customer
Calculate total sales per customer
Identify customers with above-average sales
Rank customers based on total sales
Assign row numbers to orders within customers
Display top 3 customers based on total sales

Step 3 - Final Combined Query
Generated a report showing:

Customer Name
Total Sales
Customer Rank

using CTEs, Joins, and Window Functions.

Mini Project - Customer Sales Insights
The following business questions were analyzed:

Who are the top 5 customers?
Who are the bottom 5 customers?
Which customers made only one order?
Which customers have above-average sales?
What is the highest order value per customer?


Key Learnings
Through this assignment, I gained practical experience with:

SQL Subqueries
Common Table Expressions (CTEs)
Window Functions
Ranking and Partitioning
Data Validation
Query Optimization using Indexes
Business-Oriented Data Analysis


Tools Used

Python
Pandas
SQLite
Jupyter Notebook
VS Code


Author
Mohd Nomaan
Data Engineering Internship Assignment - Week 3
