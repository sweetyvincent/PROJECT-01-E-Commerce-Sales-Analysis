# Project 01: E-Commerce Sales Analysis & Management Dashboard

A comprehensive data analysis and business intelligence project on the **Olist Brazilian E-Commerce Dataset**. This project analyzes sales performance, category trends, regional distributions, and customer satisfaction over a 12-month period. It includes automated data cleaning pipelines, detailed visualizations, an interactive Excel management dashboard, and actionable business insights.

---

## 🛠️ Project Repository Structure

* `olist_*_dataset.csv` / `product_category_name_translation.csv`: Raw data source files.
* `run_analysis.py`: Main python script for data cleaning, aggregation, answering business questions, and saving charts.
* `build_dashboard.py`: Python script that programmatically generates `dashboard.xlsx` and embeds formatted KPI tables and visual charts.
* `sales_analysis.ipynb`: A complete Jupyter Notebook showcasing the data cleaning steps, code, analysis answers, and inline charts.
* `dashboard.xlsx`: The final 1-page executive-ready management dashboard.
* `business_insights_report.md`: Detailed business insights report containing 5 actionable recommendations and a summary of findings.
* `visualizations/`: Directory containing the 10 custom-designed analytical charts.
* `README.md`: This file, documenting the project.

---

## 🚀 How to Run and Replicate the Analysis

### 1. Prerequisites
Ensure you have Python 3.8+ installed. Install the required libraries using pip:
```bash
pip install pandas numpy matplotlib seaborn openpyxl
```

### 2. Run the Data Analysis and Generate Charts
Execute the analysis script to load raw CSVs, apply cleaning rules, output analysis answers, and save the visualizations:
```bash
python run_analysis.py
```
This script will output the answers to the console and create a `visualizations/` folder containing the 10 PNG charts.

### 3. Generate the Executive Excel Dashboard
Run the dashboard generator script to build the styled Excel dashboard containing KPI cards, performance tables, and embedded visualizations:
```bash
python build_dashboard.py
```
This generates the interactive workbook `dashboard.xlsx` in the root folder.

---

## 🧹 Data Cleaning Decisions
1. **Unrealized Revenue Filtering**: Excluded orders with status `canceled` or `unavailable` because only completed/shipped transactions count towards gross sales.
2. **Stable 12-Month Window**: Selected **September 2017 to August 2018 inclusive** as the analysis timeframe. This filters out the sparse, incomplete periods at the beginning (2016) and end (late 2018) of the dataset, providing exactly 12 months of high-volume sales for trend analysis.
3. **Deduplicate Review Scores**: Calculated the average review score per `order_id` prior to joining, ensuring that multiple reviews on a single order did not duplicate order values or inflate revenue during joins.
4. **Category Translations**: Translated Portuguese category names to English. Unmapped or missing values were labeled as `'Unknown'`.
5. **Outlier Capping**: Capped the order value distribution at the 99th percentile (R$ 1,005.00) in the histogram to omit extreme values and ensure readability.

---

## 📊 Summary of Sales Analysis (5 Key Questions)

* **Q1: Top Category by Revenue**: `health_beauty` with R$ 1,003,687.59 (9.7% share).
* **Q2: Peak Sales Month**: `2017-11` (Black Friday month) with R$ 1,003,862.14 in revenue and 7,421 orders.
* **Q3: Best Performing Region**: State of **São Paulo (SP)** with R$ 4,039,060.25 (39.0% of total revenue).
* **Q4: Average Order Value Trend**: AOV is stable, averaging **R$ 137.62** overall. AOV experienced a slight drop during peak promotional months like November (R$ 135.27) and January (R$ 131.55).
* **Q5: Customer Review Scores**:
  * 5 Stars: 57.6%
  * 4 Stars: 20.0%
  * 3 Stars: 8.1%
  * 2 Stars: 3.1%
  * 1 Star: 11.1%
  *(Positive sentiment is 77.6%; however, a notable 11.1% 1-star reviews indicates a critical logistics/service recovery gap).*

---

## 📈 Visualizations Generated (Minimum 10 Charts)

All charts are saved in the `visualizations/` folder:
1. `01_revenue_by_category.png` (Bar chart: Top 10 product categories by revenue)
2. `02_monthly_sales_trend.png` (Line chart: Dual-axis monthly revenue and order volume trends)
3. `03_regional_sales.png` (Bar chart: Top 10 customer states by revenue showing % share)
4. `04_order_values_distribution.png` (Histogram: Distribution of total order values with mean/median markers)
5. `05_review_scores_distribution.png` (Donut/Pie chart: Distribution of customer review ratings)
6. `06_category_monthly_heatmap.png` (Heatmap: Top 10 categories monthly revenue showing seasonal trends)
7. `07_payment_types_distribution.png` (Donut/Pie chart: Payment method distribution by transaction value)
8. `08_order_volume_by_day_of_week.png` (Bar chart: Order volume by day of the week)
9. `09_average_freight_by_state.png` (Bar chart: Top 10 states by highest average freight/shipping cost)
10. `10_delivery_time_vs_review_score.png` (Bar chart: Average actual delivery lead time in days for each review score)

---

## 📋 Executive Dashboard Details (`dashboard.xlsx`)

The dashboard is built programmatically as a single-page summary for management review.
* **KPI Summary Cards**: Total Revenue, Total Orders, Average Order Value (AOV), Top Category, and Peak Month.
* **Aggregated Tables**:
  * Month-by-month sales and AOV trends.
  * Top 10 categories by revenue and % share.
  * Regional performance (Top 10 states by revenue and % share).
  * Review score distribution with % share.
  * Payment method revenue breakdown and % share.
  * Average delivery lead time in days vs customer review rating.
* **Embedded Visualizations**: All 10 custom charts are embedded directly in the spreadsheet below the data tables, allowing managers to inspect data and visuals in one place.

---

## 💡 Key Actionable Insights (Highlights)

1. **Leverage Health & Beauty**: Introduce subscription-based buying options for this recurring purchase category.
2. **Holiday Scaling**: Implement a 90-day logistics plan ahead of the November Black Friday peak to prevent shipping bottlenecks, especially for early-week order volume peaks (Mondays through Wednesdays).
3. **São Paulo Logistics Hub**: Establish a dedicated fulfillment center in SP to offer same-day/next-day shipping, covering 39% of the customer base, and manage freight costs.
4. **Free Shipping Threshold**: Set a free-shipping limit at R$ 120.00 (above the R$ 90.00 median) to lift average cart sizes.
5. **Logistics SLA & Customer Service Recovery**: Automatically flag low ratings and address carrier shipping delays (which average 20.3 days for 1-star reviews compared to 10.2 days for 5-star reviews) to reduce the 11.1% of 1-star reviews.

*(For detailed insights, read the full [Business Insights Report](file:///c:/Users/Lenovo/Desktop/PROJECT%2001%20E-Commerce%20Sales%20Analysis/business_insights_report.md)).*
