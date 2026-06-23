import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set style for visualisations
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.titlesize': 16
})

# Color palette
PALETTE_PRIMARY = "#1F4E78" # Dark blue
PALETTE_ACCENT = "#D9E1F2" # Light blue
COLOR_MAP = sns.light_palette(PALETTE_PRIMARY, as_cmap=True)

# Create folders for output
os.makedirs("visualizations", exist_ok=True)
print("Created 'visualizations' folder.")

# -------------------------------------------------------------
# 1. Data Loading & Cleaning
# -------------------------------------------------------------
print("\n--- Phase 1: Data Loading & Cleaning ---")

# File paths
DATA_DIR = r"c:\Users\Lenovo\Desktop\PROJECT 01 E-Commerce Sales Analysis"
files = {
    'orders': os.path.join(DATA_DIR, 'olist_orders_dataset.csv'),
    'items': os.path.join(DATA_DIR, 'olist_order_items_dataset.csv'),
    'products': os.path.join(DATA_DIR, 'olist_products_dataset.csv'),
    'reviews': os.path.join(DATA_DIR, 'olist_order_reviews_dataset.csv'),
    'customers': os.path.join(DATA_DIR, 'olist_customers_dataset.csv'),
    'translation': os.path.join(DATA_DIR, 'product_category_name_translation.csv')
}

# Read CSV files
df_orders = pd.read_csv(files['orders'])
df_items = pd.read_csv(files['items'])
df_products = pd.read_csv(files['products'])
df_reviews = pd.read_csv(files['reviews'])
df_customers = pd.read_csv(files['customers'])
# Read translation with utf-8-sig to handle potential BOM character
df_translation = pd.read_csv(files['translation'], encoding='utf-8-sig')

# Document initial shapes
print(f"Loaded raw datasets:")
print(f" - Orders: {df_orders.shape[0]} rows")
print(f" - Order Items: {df_items.shape[0]} rows")
print(f" - Products: {df_products.shape[0]} rows")
print(f" - Reviews: {df_reviews.shape[0]} rows")
print(f" - Customers: {df_customers.shape[0]} rows")
print(f" - Translations: {df_translation.shape[0]} rows")

# Cleaning Decision 1: Filter out canceled and unavailable orders
# In e-commerce, unpaid/canceled/unavailable orders do not contribute to actual revenue.
active_orders = df_orders[~df_orders['order_status'].isin(['canceled', 'unavailable'])].copy()
print(f"Cleaning: Removed canceled and unavailable orders. Active orders: {active_orders.shape[0]} rows.")

# Cleaning Decision 2: Convert date columns to datetime
date_cols = [
    'order_purchase_timestamp', 'order_approved_at', 
    'order_delivered_carrier_date', 'order_delivered_customer_date', 
    'order_estimated_delivery_date'
]
for col in date_cols:
    active_orders[col] = pd.to_datetime(active_orders[col])

# Cleaning Decision 3: Filter to 12-month period (September 2017 to August 2018 inclusive)
start_date = pd.to_datetime('2017-09-01 00:00:00')
end_date = pd.to_datetime('2018-08-31 23:59:59')
df_orders_12m = active_orders[
    (active_orders['order_purchase_timestamp'] >= start_date) & 
    (active_orders['order_purchase_timestamp'] <= end_date)
].copy()
print(f"Cleaning: Filtered orders to 12-month period (2017-09 to 2018-08). Orders count: {df_orders_12m.shape[0]}")

# Cleaning Decision 4: Handle duplicate reviews
# Some order IDs have multiple reviews (due to multiple items, revisions, or resubmissions).
# We take the mean review score for each order_id to avoid duplicating order values upon merging.
df_reviews_unique = df_reviews.groupby('order_id', as_index=False).agg({
    'review_score': 'mean',
    'review_id': 'first',
    'review_creation_date': 'first',
    'review_answer_timestamp': 'first'
})
print(f"Cleaning: Deduplicated review scores by taking average score per order. Reviews count: {df_reviews_unique.shape[0]}")

# Cleaning Decision 5: Clean column names in translation table
# Handled BOM character by using 'utf-8-sig', let's print columns to verify
df_translation.columns = df_translation.columns.str.replace(r'^\ufeff', '', regex=True)

# Merge Datasets
# Main merge: orders_12m -> items -> products -> translation -> customers -> reviews
merged = df_orders_12m.merge(df_items, on='order_id', how='inner')
print(f"Merged with Order Items: {merged.shape[0]} rows (items sold)")

merged = merged.merge(df_products, on='product_id', how='left')
# Merge with translations to get English category names
merged = merged.merge(df_translation, on='product_category_name', how='left')

# Cleaning Decision 6: Handle missing product categories
# If product category name is missing, fill with 'Unknown'
merged['product_category_name_english'] = merged['product_category_name_english'].fillna('Unknown')
# If translation is missing but original category exists, format and use original
missing_trans = (merged['product_category_name_english'] == 'Unknown') & (merged['product_category_name'].notna())
merged.loc[missing_trans, 'product_category_name_english'] = merged.loc[missing_trans, 'product_category_name'].apply(
    lambda x: str(x).replace('_', ' ').title()
)

merged = merged.merge(df_customers, on='customer_id', how='left')
merged = merged.merge(df_reviews_unique, on='order_id', how='left')

# Fill missing review scores (if any) with the overall mean review score for the dataset
mean_score = merged['review_score'].mean()
merged['review_score'] = merged['review_score'].fillna(mean_score)

print(f"Final Merged Dataset: {merged.shape[0]} rows, columns: {list(merged.columns)}")

# -------------------------------------------------------------
# 2. Sales Analysis (5 Questions)
# -------------------------------------------------------------
print("\n--- Phase 2: Sales Analysis ---")

# (1) Which product category has the highest revenue?
category_revenue = merged.groupby('product_category_name_english')['price'].sum().sort_values(ascending=False)
top_category = category_revenue.index[0]
top_category_rev = category_revenue.iloc[0]
print(f"Q1: Top Category: '{top_category}' with revenue of R$ {top_category_rev:,.2f}")

# (2) Which month had peak sales?
# Extract year-month for grouping
merged['purchase_month'] = merged['order_purchase_timestamp'].dt.strftime('%Y-%m')
monthly_sales = merged.groupby('purchase_month')['price'].sum().sort_values(ascending=False)
peak_month = monthly_sales.index[0]
peak_month_sales = monthly_sales.iloc[0]
print(f"Q2: Peak Month: {peak_month} with revenue of R$ {peak_month_sales:,.2f}")

# (3) Which region performs best?
# We use customer state for region
region_sales = merged.groupby('customer_state')['price'].sum().sort_values(ascending=False)
top_state = region_sales.index[0]
top_state_sales = region_sales.iloc[0]
top_state_pct = (top_state_sales / merged['price'].sum()) * 100
print(f"Q3: Best Performing Region: State of {top_state} with revenue of R$ {top_state_sales:,.2f} ({top_state_pct:.1f}% of total)")

# (4) What is the average order value trend?
# AOV = Total revenue per month / Total unique orders per month
monthly_aov = merged.groupby('purchase_month').agg(
    total_revenue=('price', 'sum'),
    unique_orders=('order_id', 'nunique')
)
monthly_aov['aov'] = monthly_aov['total_revenue'] / monthly_aov['unique_orders']
print("Q4: Average Order Value (AOV) Trend:")
for m, row in monthly_aov.sort_index().iterrows():
    print(f" - {m}: AOV = R$ {row['aov']:.2f} (Orders: {int(row['unique_orders'])}, Rev: R$ {row['total_revenue']:,.2f})")

# (5) What is the customer review score distribution?
# Review score is at order level, so let's get unique orders and their review scores
df_order_reviews = merged.drop_duplicates('order_id')
review_dist = df_order_reviews['review_score'].round().value_counts().sort_index()
print("Q5: Customer Review Score Distribution:")
for score, count in review_dist.items():
    pct = (count / df_order_reviews.shape[0]) * 100
    print(f" - Score {int(score)}: {count} orders ({pct:.1f}%)")

# Calculate KPIs for Dashboard
total_revenue = merged['price'].sum()
total_orders = merged['order_id'].nunique()
aov_overall = total_revenue / total_orders
print(f"\nOverall KPIs:")
print(f" - Total Revenue: R$ {total_revenue:,.2f}")
print(f" - Total Orders: {total_orders}")
print(f" - Overall AOV: R$ {aov_overall:.2f}")

# Save results to a summary file for reference
with open(os.path.join(DATA_DIR, "analysis_answers.txt"), "w", encoding="utf-8") as f:
    f.write("=== SALES ANALYSIS RESULTS ===\n\n")
    f.write(f"Q1: Top Product Category by Revenue\n")
    f.write(f"Category: {top_category}\n")
    f.write(f"Revenue: R$ {top_category_rev:,.2f}\n\n")
    f.write(f"Q2: Peak Sales Month\n")
    f.write(f"Month: {peak_month}\n")
    f.write(f"Revenue: R$ {peak_month_sales:,.2f}\n\n")
    f.write(f"Q3: Best Performing Region (Customer State)\n")
    f.write(f"State: {top_state}\n")
    f.write(f"Revenue: R$ {top_state_sales:,.2f} ({top_state_pct:.1f}%)\n\n")
    f.write(f"Q4: Average Order Value (AOV) Trend\n")
    for m, row in monthly_aov.sort_index().iterrows():
        f.write(f"{m}: AOV = R$ {row['aov']:.2f}, Orders = {int(row['unique_orders'])}, Revenue = R$ {row['total_revenue']:,.2f}\n")
    f.write("\nQ5: Customer Review Score Distribution (rounded to nearest integer)\n")
    for score, count in review_dist.items():
        pct = (count / df_order_reviews.shape[0]) * 100
        f.write(f"Score {int(score)}: {count} ({pct:.1f}%)\n")

# -------------------------------------------------------------
# 3. Visualisations
# -------------------------------------------------------------
print("\n--- Phase 3: Generating Visualizations ---")

# Plot 1: Bar chart (revenue by category) - Top 10
plt.figure(figsize=(10, 6))
top_10_cats = category_revenue.head(10)
sns.barplot(x=top_10_cats.values / 1e6, y=top_10_cats.index, color=PALETTE_PRIMARY)
plt.title("Top 10 Product Categories by Revenue (Sep 2017 - Aug 2018)", pad=15)
plt.xlabel("Revenue (R$ Millions)")
plt.ylabel("Product Category")
plt.tight_layout()
plt.savefig("visualizations/01_revenue_by_category.png", dpi=300)
plt.close()
print("Saved visualization 1: Revenue by Category.")

# Plot 2: Line chart (monthly sales trend - Revenue & Volume)
fig, ax1 = plt.subplots(figsize=(10, 6))
monthly_sorted = monthly_aov.sort_index()
months_labels = monthly_sorted.index

color = '#1F4E78' # Primary Dark Blue
ax1.set_xlabel('Month')
ax1.set_ylabel('Total Revenue (R$ Millions)', color=color)
line1 = ax1.plot(months_labels, monthly_sorted['total_revenue'] / 1e6, color=color, marker='o', linewidth=2.5, label='Revenue')
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_xticklabels(months_labels, rotation=45)

ax2 = ax1.twinx()  
color = '#C55A11' # Accent Orange for Volume
ax2.set_ylabel('Number of Orders', color=color)
line2 = ax2.plot(months_labels, monthly_sorted['unique_orders'], color=color, marker='s', linestyle='--', linewidth=2, label='Orders')
ax2.tick_params(axis='y', labelcolor=color)

# Add legend
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper left')

plt.title("Monthly Sales Trend (Sep 2017 - Aug 2018)", pad=15)
fig.tight_layout()
plt.savefig("visualizations/02_monthly_sales_trend.png", dpi=300)
plt.close()
print("Saved visualization 2: Monthly Sales Trend.")

# Plot 3: Bar chart (regional sales - Top 10 States)
plt.figure(figsize=(10, 6))
top_10_states = region_sales.head(10)
sns.barplot(x=top_10_states.index, y=top_10_states.values / 1e6, color=PALETTE_PRIMARY)
plt.title("Top 10 States by Revenue (Sep 2017 - Aug 2018)", pad=15)
plt.xlabel("Customer State")
plt.ylabel("Revenue (R$ Millions)")
# Add percentage labels on top of bars
total_rev_sum = merged['price'].sum()
for i, val in enumerate(top_10_states.values):
    pct = (val / total_rev_sum) * 100
    plt.text(i, val / 1e6 + 0.1, f"{pct:.1f}%", ha='center', va='bottom', fontsize=9, fontweight='bold')
plt.tight_layout()
plt.savefig("visualizations/03_regional_sales.png", dpi=300)
plt.close()
print("Saved visualization 3: Regional Sales.")

# Plot 4: Histogram (order values - capped at 99th percentile for outlier handling)
plt.figure(figsize=(10, 6))
order_totals = merged.groupby('order_id').agg({'price': 'sum', 'freight_value': 'sum'})
order_totals['total_value'] = order_totals['price'] + order_totals['freight_value']

# Outlier handling: cap at 99th percentile to make histogram highly readable
cap_limit = order_totals['total_value'].quantile(0.99)
filtered_orders = order_totals[order_totals['total_value'] <= cap_limit]

sns.histplot(filtered_orders['total_value'], bins=40, color=PALETTE_PRIMARY, kde=True)
plt.axvline(order_totals['total_value'].median(), color='#C55A11', linestyle='--', linewidth=2, 
            label=f"Median Order Value: R$ {order_totals['total_value'].median():.2f}")
plt.axvline(order_totals['total_value'].mean(), color='#7F7F7F', linestyle='-', linewidth=2, 
            label=f"Mean Order Value: R$ {order_totals['total_value'].mean():.2f}")

plt.title(f"Distribution of Order Values (Capped at 99th Percentile: R$ {cap_limit:.2f})", pad=15)
plt.xlabel("Order Value (R$ Price + Freight)")
plt.ylabel("Count of Orders")
plt.legend()
plt.tight_layout()
plt.savefig("visualizations/04_order_values_distribution.png", dpi=300)
plt.close()
print("Saved visualization 4: Order Values Distribution.")

# Plot 5: Pie/Donut chart (review scores)
plt.figure(figsize=(8, 8))
review_counts = df_order_reviews['review_score'].round().value_counts().sort_index()
# Label formats
labels = [f"Score {int(k)} ({v:,})" for k, v in review_counts.items()]
# Color palette: custom greens and reds for satisfaction
colors = ['#C00000', '#FFC000', '#A6A6A6', '#8FAADC', '#2F5597'] # Red, Orange, Gray, Light Blue, Dark Blue

plt.pie(review_counts, labels=labels, autopct='%1.1f%%', startangle=140, 
        colors=colors, wedgeprops=dict(width=0.4, edgecolor='w'))
plt.title("Distribution of Customer Review Scores (Sep 2017 - Aug 2018)", pad=20)
plt.tight_layout()
plt.savefig("visualizations/05_review_scores_distribution.png", dpi=300)
plt.close()
print("Saved visualization 5: Review Scores Distribution.")

# Plot 6: Heatmap (category vs month)
plt.figure(figsize=(12, 8))
# Pivot top 10 categories over months
top_10_cats_names = category_revenue.head(10).index
heatmap_data = merged[merged['product_category_name_english'].isin(top_10_cats_names)]
heatmap_pivot = heatmap_data.pivot_table(
    index='product_category_name_english',
    columns='purchase_month',
    values='price',
    aggfunc='sum'
).reindex(top_10_cats_names)

# Convert to thousands for cleaner numbers in cell annotations
sns.heatmap(heatmap_pivot / 1000, annot=True, fmt=".1f", cmap="Blues", cbar_kws={'label': 'Revenue (R$ Thousands)'})
plt.title("Heatmap: Top 10 Product Categories Monthly Revenue (R$ Thousands)", pad=15)
plt.xlabel("Month of Purchase")
plt.ylabel("Product Category")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("visualizations/06_category_monthly_heatmap.png", dpi=300)
plt.close()
print("Saved visualization 6: Category-Month Revenue Heatmap.")
print("\n--- All visualizations saved successfully! ---")
