# 🛍️ Shopping Dataset — Data Exploration & Cleaning

A beginner-level data science project where I loaded a real e-commerce
dataset, explored it, cleaned it, and extracted basic insights using Python and Pandas.

---

## 📌 What This Project Does

This project walks through the full basic data cleaning pipeline:

1. Load a CSV dataset into a Pandas DataFrame
2. Explore the data — shape, columns, data types, missing values
3. Handle missing values — fill with median or 'Unknown'
4. Filter rows and select useful columns
5. Remove duplicate rows
6. Create a derived column (`savings = initial_price - final_price`)
7. Save the cleaned dataset as a new CSV file

---

## 📂 Project Structure

```
shopping-data-cleaning/
│
├── shopping_dataset.csv          # Original raw dataset
├── cleaned_shopping_dataset.csv  # Cleaned output dataset
├── intermediate_cleaning.ipynb   # Jupyter Notebook with all steps
└── README.md                     # This file
```

---

## 📊 Dataset

**Source:** [Kaggle — Ecommerce Dataset (Products & Sizes Included)](https://www.kaggle.com/datasets/anvitkumar/shopping-dataset)

### Columns Used

| Column | Description |
|---|---|
| product_id | Unique product identifier |
| title | Product name |
| category | Product category |
| rating | Average customer rating |
| ratings_count | Number of ratings |
| initial_price | Original price before discount |
| discount | Discount percentage |
| final_price | Price after discount |
| seller_name | Name of the seller |
| sizes | Available sizes |

---

## 🧹 Cleaning Steps Explained

### Step 1 — Load
Used `pd.read_csv()` to load the dataset into a Pandas DataFrame.

### Step 2 — Explore
Used `df.head()`, `df.info()`, `df.describe()`, and `df.value_counts()`
to understand the structure, data types, and missing values before
touching anything.

### Step 3 — Handle Missing Values
- `final_price` was stored as a string — converted to numeric using
  `pd.to_numeric(errors='coerce')`
- Missing numeric values (price, rating, discount) → filled with **median**
- Missing text values (seller_name, category, sizes) → filled with `'Unknown'`

> Why median and not mean?  
> Mean gets affected by extreme values. For example, one product
> priced at ₹50,000 would pull the average up unfairly.
> Median stays in the middle regardless.

### Step 4 — Filter & Select
- Selected only 10 useful columns, dropping raw scraped columns
  like `images`, `videos`, `product_specifications`
- Filtered rows by rating > 4.0 and discount > 20%

### Step 5 — Remove Duplicates
Used `df.drop_duplicates()` to remove any rows that were exact copies
of another row.

### Step 6 — Derived Column
Created a new column:
```
savings = initial_price - final_price
```
This tells us how much money a customer saves on each product.
Also used `groupby()` to find average savings by category.

### Step 7 — Save
Saved the cleaned DataFrame as `cleaned_shopping_dataset.csv`
using `df.to_csv(index=False)`.

> `index=False` prevents Pandas from adding an extra numbered
> column to the output file.

---

## ▶️ How to Run This Project

### 1. Clone the repository
```bash
git clone https://github.com/your-username/shopping-data-cleaning.git
cd shopping-data-cleaning
```

### 2. Install Pandas (if not already installed)
```bash
pip install pandas
```

### 3. Open the notebook
```bash
jupyter notebook intermediate_cleaning.ipynb
```
Or open it directly in VS Code with the Jupyter extension.

### 4. Run all cells
Click **Run All** at the top, or run cells one by one with `Shift + Enter`.

---

## 🛠️ Libraries Used

| Library | Purpose |
|---|---|
| Pandas | Loading, exploring, cleaning, and saving data |

No other libraries required.

---

## 💡 Key Learnings

- Always explore data before modifying anything
- Fix data types first — everything else depends on correct types
- Use median (not mean) to fill missing numeric values
- Never overwrite raw data — always save to a new file
- `groupby()` is the most useful tool for finding patterns in data

---

## 👤 Author

**Mohd Nomaan**  
B.Tech AI/CS — SKIT Jaipur  
GitHub: [GH-Shinichi](https://github.com/GH-Shinichi)  
LinkedIn: [mohd-nomaan](https://linkedin.com/in/mohd-nomaan-a65158353)
