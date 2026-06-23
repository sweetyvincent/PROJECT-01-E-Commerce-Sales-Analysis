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
    'payments': os.path.join(DATA_DIR, 'olist_order_payments_dataset.csv'),
    'translation': os.path.join(DATA_DIR, 'product_category_name_translation.csv')
}

# Read CSV files
df_orders = pd.read_csv(files['orders'])
df_items = pd.read_csv(files['items'])
df_products = pd.read_csv(files['products'])
df_reviews = pd.read_csv(files['reviews'])
df_customers = pd.read_csv(files['customers'])
df_payments = pd.read_csv(files['payments'])
df_translation = pd.read_csv(files['translation'], encoding='utf-8-sig')

# Document initial shapes
print(f"Loaded raw datasets:")
print(f" - Orders: {df_orders.shape[0]} rows")
print(f" - Order Items: {df_items.shape[0]} rows")
print(f" - Products: {df_products.shape[0]} rows")
print(f" - Reviews: {df_reviews.shape[0]} rows")
print(f" - Customers: {df_customers.shape[0]} rows")
print(f" - Payments: {df_payments.shape[0]} rows")
print(f" - Translations: {df_translation.shape[0]} rows")

# Cleaning Decision 1: Filter out canceled and unavailable orders
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
df_reviews_unique = df_reviews.groupby('order_id', as_index=False).agg({
    'review_score': 'mean',
    'review_id': 'first',
    'review_creation_date': 'first',
    'review_answer_timestamp': 'first'
})
print(f"Cleaning: Deduplicated review scores by taking average score per order. Reviews count: {df_reviews_unique.shape[0]}")

# Cleaning Decision 5: Clean column names in translation table
df_translation.columns = df_translation.columns.str.replace(r'^\ufeff', '', regex=True)

# Merge Datasets for main analysis
merged = df_orders_12m.merge(df_items, on='order_id', how='inner')
print(f"Merged with Order Items: {merged.shape[0]} rows (items sold)")

merged = merged.merge(df_products, on='product_id', how='left')
merged = merged.merge(df_translation, on='product_category_name', how='left')

# Cleaning Decision 6: Handle missing product categories
merged['product_category_name_english'] = merged['product_category_name_english'].fillna('Unknown')
missing_trans = (merged['product_category_name_english'] == 'Unknown') & (merged['product_category_name'].notna())
merged.loc[missing_trans, 'product_category_name_english'] = merged.loc[missing_trans, 'product_category_name'].apply(
    lambda x: str(x).replace('_', ' ').title()
)

merged = merged.merge(df_customers, on='customer_id', how='left')
merged = merged.merge(df_reviews_unique, on='order_id', how='left')
merged['review_score'] = merged['review_score'].fillna(merged['review_score'].mean())
merged['purchase_month'] = merged['order_purchase_timestamp'].dt.strftime('%Y-%m')

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
monthly_sales = merged.groupby('purchase_month')['price'].sum().sort_values(ascending=False)
peak_month = monthly_sales.index[0]
peak_month_sales = monthly_sales.iloc[0]
print(f"Q2: Peak Month: {peak_month} with revenue of R$ {peak_month_sales:,.2f}")

# (3) Which region performs best?
region_sales = merged.groupby('customer_state')['price'].sum().sort_values(ascending=False)
top_state = region_sales.index[0]
top_state_sales = region_sales.iloc[0]
top_state_pct = (top_state_sales / merged['price'].sum()) * 100
print(f"Q3: Best Performing Region: State of {top_state} with revenue of R$ {top_state_sales:,.2f} ({top_state_pct:.1f}% of total)")

# (4) What is the average order value trend?
monthly_aov = merged.groupby('purchase_month').agg(
    total_revenue=('price', 'sum'),
    unique_orders=('order_id', 'nunique')
)
monthly_aov['aov'] = monthly_aov['total_revenue'] / monthly_aov['unique_orders']
print("Q4: Average Order Value (AOV) Trend:")
for m, row in monthly_aov.sort_index().iterrows():
    print(f" - {m}: AOV = R$ {row['aov']:.2f}")

# (5) What is the customer review score distribution?
df_order_reviews = merged.drop_duplicates('order_id')
review_dist = df_order_reviews['review_score'].round().value_counts().sort_index()
print("Q5: Customer Review Score Distribution:")
for score, count in review_dist.items():
    pct = (count / df_order_reviews.shape[0]) * 100
    print(f" - Score {int(score)}: {count} orders ({pct:.1f}%)")

# Calculate overall KPIs
total_revenue = merged['price'].sum()
total_orders = merged['order_id'].nunique()
aov_overall = total_revenue / total_orders

# -------------------------------------------------------------
# 3. Visualisations - 10 Charts
# -------------------------------------------------------------
print("\n--- Phase 3: Generating Visualizations (Minimum 10) ---")

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

color = '#1F4E78'
ax1.set_xlabel('Month')
ax1.set_ylabel('Total Revenue (R$ Millions)', color=color)
line1 = ax1.plot(months_labels, monthly_sorted['total_revenue'] / 1e6, color=color, marker='o', linewidth=2.5, label='Revenue')
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_xticks(range(len(months_labels)))
ax1.set_xticklabels(months_labels, rotation=45)

ax2 = ax1.twinx()  
color = '#C55A11'
ax2.set_ylabel('Number of Orders', color=color)
line2 = ax2.plot(months_labels, monthly_sorted['unique_orders'], color=color, marker='s', linestyle='--', linewidth=2, label='Orders')
ax2.tick_params(axis='y', labelcolor=color)

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
total_rev_sum = merged['price'].sum()
for i, val in enumerate(top_10_states.values):
    pct = (val / total_rev_sum) * 100
    plt.text(i, val / 1e6 + 0.05, f"{pct:.1f}%", ha='center', va='bottom', fontsize=9, fontweight='bold')
plt.tight_layout()
plt.savefig("visualizations/03_regional_sales.png", dpi=300)
plt.close()
print("Saved visualization 3: Regional Sales.")

# Plot 4: Histogram (order values - capped at 99th percentile)
plt.figure(figsize=(10, 6))
order_totals = merged.groupby('order_id').agg({'price': 'sum', 'freight_value': 'sum'})
order_totals['total_value'] = order_totals['price'] + order_totals['freight_value']
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
labels = [f"Score {int(k)} ({v:,})" for k, v in review_counts.items()]
colors = ['#C00000', '#FFC000', '#A6A6A6', '#8FAADC', '#2F5597']

plt.pie(review_counts, labels=labels, autopct='%1.1f%%', startangle=140, 
        colors=colors, wedgeprops=dict(width=0.4, edgecolor='w'))
plt.title("Distribution of Customer Review Scores (Sep 2017 - Aug 2018)", pad=20)
plt.tight_layout()
plt.savefig("visualizations/05_review_scores_distribution.png", dpi=300)
plt.close()
print("Saved visualization 5: Review Scores Distribution.")

# Plot 6: Heatmap (category vs month)
plt.figure(figsize=(12, 8))
top_10_cats_names = category_revenue.head(10).index
heatmap_data = merged[merged['product_category_name_english'].isin(top_10_cats_names)]
heatmap_pivot = heatmap_data.pivot_table(
    index='product_category_name_english',
    columns='purchase_month',
    values='price',
    aggfunc='sum'
).reindex(top_10_cats_names)

sns.heatmap(heatmap_pivot / 1000, annot=True, fmt=".1f", cmap="Blues", cbar_kws={'label': 'Revenue (R$ Thousands)'})
plt.title("Heatmap: Top 10 Product Categories Monthly Revenue (R$ Thousands)", pad=15)
plt.xlabel("Month of Purchase")
plt.ylabel("Product Category")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("visualizations/06_category_monthly_heatmap.png", dpi=300)
plt.close()
print("Saved visualization 6: Category-Month Revenue Heatmap.")


# --- NEW VISUALIZATIONS (TO HIT 10 CHARTS MINIMUM) ---

# Plot 7: Donut Chart - Payment Method Distribution
plt.figure(figsize=(8, 8))
# Merge payments with 12m orders
orders_pay = df_orders_12m.merge(df_payments, on='order_id', how='inner')
pay_dist = orders_pay.groupby('payment_type')['payment_value'].sum().sort_values(ascending=False)
# Remove undefined payment types if any
pay_dist = pay_dist[pay_dist.index != 'not_defined']

labels_pay = [f"{pt.replace('_', ' ').title()} (R$ {val/1e6:.2f}M)" for pt, val in pay_dist.items()]
colors_pay = ['#1F4E78', '#2F5597', '#8FAADC', '#C55A11', '#A6A6A6']

plt.pie(pay_dist, labels=labels_pay, autopct='%1.1f%%', startangle=90,
        colors=colors_pay[:len(pay_dist)], wedgeprops=dict(width=0.4, edgecolor='w'))
plt.title("Payment Method Share by Transaction Value (Sep 2017 - Aug 2018)", pad=20)
plt.tight_layout()
plt.savefig("visualizations/07_payment_types_distribution.png", dpi=300)
plt.close()
print("Saved visualization 7: Payment Types Distribution.")

# Plot 8: Bar Chart - Order Volume by Day of the Week
plt.figure(figsize=(10, 6))
merged['purchase_day_name'] = merged['order_purchase_timestamp'].dt.day_name()
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekly_orders = merged.drop_duplicates('order_id').groupby('purchase_day_name').size().reindex(day_order)

sns.barplot(x=weekly_orders.index, y=weekly_orders.values, color='#2F5597')
plt.title("Order Volume by Day of the Week (Sep 2017 - Aug 2018)", pad=15)
plt.xlabel("Day of the Week")
plt.ylabel("Number of Orders")
for i, val in enumerate(weekly_orders.values):
    plt.text(i, val + 150, f"{val:,}", ha='center', va='bottom', fontsize=9, fontweight='bold')
plt.tight_layout()
plt.savefig("visualizations/08_order_volume_by_day_of_week.png", dpi=300)
plt.close()
print("Saved visualization 8: Weekly Shopping Activity.")

# Plot 9: Bar Chart - Average Freight Cost by Customer State (Top 10)
plt.figure(figsize=(10, 6))
# Get average freight value per order by customer state
state_freight = merged.groupby('customer_state')['freight_value'].mean().sort_values(ascending=False).head(10)
sns.barplot(x=state_freight.index, y=state_freight.values, color='#C55A11')
plt.title("Average Freight (Shipping) Cost by Customer State (Top 10 Highest)", pad=15)
plt.xlabel("Customer State")
plt.ylabel("Average Freight Value (R$)")
for i, val in enumerate(state_freight.values):
    plt.text(i, val + 0.5, f"R$ {val:.2f}", ha='center', va='bottom', fontsize=9, fontweight='bold')
plt.tight_layout()
plt.savefig("visualizations/09_average_freight_by_state.png", dpi=300)
plt.close()
print("Saved visualization 9: Average Freight Cost by State.")

# Plot 10: Bar Chart - Delivery Lead Time vs. Customer Review Score
plt.figure(figsize=(10, 6))
# Calculate delivery lead time (days) at order level
df_delivery = df_orders_12m.dropna(subset=['order_delivered_customer_date']).copy()
df_delivery['delivery_lead_time_days'] = (df_delivery['order_delivered_customer_date'] - df_delivery['order_purchase_timestamp']).dt.days
# Exclude negative times if data entry errors
df_delivery = df_delivery[df_delivery['delivery_lead_time_days'] >= 0]

# Merge with reviews
df_delivery_reviews = df_delivery.merge(df_reviews_unique, on='order_id', how='inner')
# Group by rounded review score
delivery_time_vs_review = df_delivery_reviews.groupby('review_score')['delivery_lead_time_days'].mean()

sns.barplot(x=delivery_time_vs_review.index.astype(int), y=delivery_time_vs_review.values, palette='RdYlGn_r')
plt.title("Average Delivery Time vs. Customer Review Rating", pad=15)
plt.xlabel("Review Rating (Stars)")
plt.ylabel("Average Actual Delivery Time (Days)")
for i, val in enumerate(delivery_time_vs_review.values):
    plt.text(i, val + 0.3, f"{val:.1f} days", ha='center', va='bottom', fontsize=10, fontweight='bold')
plt.tight_layout()
plt.savefig("visualizations/10_delivery_time_vs_review_score.png", dpi=300)
plt.close()
print("Saved visualization 10: Delivery Time vs Review Score.")

print("\n--- All 10 visualizations saved successfully! ---")
