# Business Insights Report: Olist E-Commerce Performance (10-Chart Analysis)
**Date**: June 23, 2026  
**Author**: Data Analyst  
**Analysis Timeframe**: September 2017 – August 2018 (12-Month Period)  
**Total Revenue**: R$ 10,368,678.87  
**Total Orders**: 75,343  
**Average Order Value (AOV)**: R$ 137.62  

---

## 1. Executive Summary
This report presents an in-depth performance analysis of the Olist e-commerce platform in Brazil. By evaluating transaction data, product categories, geographic distribution, payment types, weekly purchasing habits, shipping costs, and customer review scores, we identify key growth trends, evaluate logistics efficiency, assess consumer preferences, and provide 5 numbered, data-driven business recommendations to improve profitability, shipping speeds, and customer loyalty.

---

## 2. Data Cleaning Decisions
To ensure the highest accuracy of our findings, the raw datasets were processed under the following data cleaning decisions:
* **Active Sales Only**: Excluded orders with status `canceled` or `unavailable` from the analysis. Unpaid or returned items do not represent realized revenue.
* **12-Month Timeframe Selection**: Selected the period from **September 2017 to August 2018** inclusive. The dataset spans 2016 to late 2018, but the selected period represents a stable, continuous, and high-volume 12-month window.
* **Review Score Deduplication**: Some orders contain multiple reviews or review updates. To prevent artificial duplication of order values and double-counting of revenue, we calculated the average review score per `order_id` before merging.
* **Category Name Translation**: Translated Portuguese product category names to English. Missing translations or null values were filled with 'Unknown'.
* **Outlier Capping for Visualization**: The histogram of order values was capped at the 99th percentile (R$ 1,005.00) to ensure readability by omitting extreme outliers.

---

## 3. Sales Analysis (Answers to the 5 Key Questions)

### Q1: Which product category has the highest revenue?
The **health_beauty** category has the highest revenue, generating **R$ 1,003,687.59** (9.7% of total sales revenue) during the 12-month period. It is closely followed by *watches_gifts* (R$ 880.8k) and *bed_bath_table* (R$ 808.0k).
*(Refer to chart: [01_revenue_by_category.png](file:///c:/Users/Lenovo/Desktop/PROJECT%2001%20E-Commerce%20Sales%20Analysis/visualizations/01_revenue_by_category.png))*

### Q2: Which month had peak sales?
**November 2017** was the peak sales month, generating **R$ 1,003,862.14** in revenue and recording **7,421** completed orders. This represents a major peak driven by Black Friday promotions.
*(Refer to chart: [02_monthly_sales_trend.png](file:///c:/Users/Lenovo/Desktop/PROJECT%2001%20E-Commerce%20Sales%20Analysis/visualizations/02_monthly_sales_trend.png))*

### Q3: Which region performs best?
The state of **São Paulo (SP)** is by far the best performing region. It generated **R$ 4,039,060.25**, accounting for **39.0%** of total platform revenue. Rio de Janeiro (RJ) came second at 13.5% (R$ 1.40M) and Minas Gerais (MG) third at 12.1% (R$ 1.25M).
*(Refer to chart: [03_regional_sales.png](file:///c:/Users/Lenovo/Desktop/PROJECT%2001%20E-Commerce%20Sales%20Analysis/visualizations/03_regional_sales.png))*

### Q4: What is the average order value trend?
The average order value (AOV) is relatively stable, ranging between **R$ 126.49** (February 2018) and **R$ 147.01** (September 2017), with an overall 12-month average of **R$ 137.62**. AOV experienced a slight drop during high-volume promotional months (e.g., R$ 135.27 in November 2017 and R$ 131.55 in January 2018), indicating that volume growth was driven by smaller-ticket items or discounts.
*(Refer to tables in: [dashboard.xlsx](file:///c:/Users/Lenovo/Desktop/PROJECT%2001%20E-Commerce%20Sales%20Analysis/dashboard.xlsx))*

### Q5: What is the customer review score distribution?
Customer satisfaction is generally high, with **77.6%** of orders receiving positive ratings (57.6% 5-star, 20.0% 4-star). However, a significant **11.1%** of transactions resulted in 1-star reviews. Our analysis shows a massive correlation with shipping: 1-star reviews have an average delivery lead time of **20.3 days** compared to just **10.2 days** for 5-star reviews.
*(Refer to charts: [05_review_scores_distribution.png](file:///c:/Users/Lenovo/Desktop/PROJECT%2001%20E-Commerce%20Sales%20Analysis/visualizations/05_review_scores_distribution.png) and [10_delivery_time_vs_review_score.png](file:///c:/Users/Lenovo/Desktop/PROJECT%2001%20E-Commerce%20Sales%20Analysis/visualizations/10_delivery_time_vs_review_score.png))*

---

## 4. Business Insights & Actionable Recommendations

### 1. Optimize Marketing Budget for the "Health & Beauty" Category
* **Insight**: As shown in the category revenue chart ([01_revenue_by_category.png](file:///c:/Users/Lenovo/Desktop/PROJECT%2001%20E-Commerce%20Sales%20Analysis/visualizations/01_revenue_by_category.png)), Health & Beauty is Olist's top-performing category, generating over R$ 1.00M in revenue. According to our category-month heatmap ([06_category_monthly_heatmap.png](file:///c:/Users/Lenovo/Desktop/PROJECT%2001%20E-Commerce%20Sales%20Analysis/visualizations/06_category_monthly_heatmap.png)), this category shows consistent, strong performance throughout the year, with a massive peak of R$ 116.8k in August 2018.
* **Recommendation**: Reallocate marketing budget to focus heavily on search engine ads and social media campaigns for Health & Beauty. Implement subscription-based buying options (recurring deliveries for cosmetics and vitamins) to secure long-term recurring revenue.

### 2. Formulate a 30-60-90 Day Plan for November (Black Friday) Order Spikes
* **Insight**: The monthly sales trend chart ([02_monthly_sales_trend.png](file:///c:/Users/Lenovo/Desktop/PROJECT%2001%20E-Commerce%20Sales%20Analysis/visualizations/02_monthly_sales_trend.png)) shows a sharp spike in order volume in November 2017 (7,421 orders, up 63% from October's 4,547). Additionally, order volume is highest on Mondays, Tuesdays, and Wednesdays ([08_order_volume_by_day_of_week.png](file:///c:/Users/Lenovo/Desktop/PROJECT%2001%20E-Commerce%20Sales%20Analysis/visualizations/08_order_volume_by_day_of_week.png)), showing that customers place orders early in the week, putting immediate strain on supply chain operations.
* **Recommendation**: Logistics managers should implement a 90-day pre-holiday readiness plan:
  * **90 Days Out**: Review seller capacities and coordinate inventory levels.
  * **60 Days Out**: Onboard secondary delivery partners to mitigate bottleneck risks.
  * **30 Days Out**: Set up early promotions to distribute shipping volumes and prevent a single-week bottleneck. Ensure extra carrier pick-ups are scheduled for Mondays through Wednesdays.

### 3. Establish a Dedicated Distribution Center (Fulfillment Hub) in São Paulo
* **Insight**: The regional sales analysis ([03_regional_sales.png](file:///c:/Users/Lenovo/Desktop/PROJECT%2001%20E-Commerce%20Sales%20Analysis/visualizations/03_regional_sales.png)) reveals that São Paulo (SP) generates 39% of total revenue. Combining SP with neighboring states Rio de Janeiro (RJ) and Minas Gerais (MG) accounts for **over 64%** of Olist's total sales. Conversely, remote states like Paraíba (PB) and Roraima (RR) face extremely high average freight costs exceeding R$ 42.00 per order ([09_average_freight_by_state.png](file:///c:/Users/Lenovo/Desktop/PROJECT%2001%20E-Commerce%20Sales%20Analysis/visualizations/09_average_freight_by_state.png)).
* **Recommendation**: Open a fulfillment hub in the state of São Paulo. Storing top-selling items locally will reduce shipping times (enabling next-day or same-day delivery for SP buyers) and significantly lower shipping costs, maximizing operating margins. For high-freight states, consider setting up separate distribution partnerships to reduce shipping barriers.

### 4. Implement Threshold-Based Free Shipping to Lift Median Order Value
* **Insight**: The order values distribution histogram ([04_order_values_distribution.png](file:///c:/Users/Lenovo/Desktop/PROJECT%2001%20E-Commerce%20Sales%20Analysis/visualizations/04_order_values_distribution.png)) displays a median order value of R$ 90.00, which is significantly lower than the average order value (AOV) of R$ 137.62. This indicates that the majority of orders are small-value transactions.
* **Recommendation**: Introduce a threshold-based free shipping promotion, set at **R$ 120.00** (roughly 33% higher than the median order value). This will incentivize customers to add complementary or lower-priced items (like accessories or filler products) to their carts to cross the free-shipping line, lifting overall AOV.

### 5. Establish a Logistics SLA Protocol and Post-Purchase Satisfaction Recovery
* **Insight**: Despite 77.6% positive ratings, a severe 11.1% of transactions received a 1-star review ([05_review_scores_distribution.png](file:///c:/Users/Lenovo/Desktop/PROJECT%2001%20E-Commerce%20Sales%20Analysis/visualizations/05_review_scores_distribution.png)). Chart [10_delivery_time_vs_review_score.png](file:///c:/Users/Lenovo/Desktop/PROJECT%2001%20E-Commerce%20Sales%20Analysis/visualizations/10_delivery_time_vs_review_score.png) shows a clear and direct relationship: 1-star reviews are heavily linked to long delivery lead times (averaging 20.3 days vs 10.2 days for 5-star reviews). Furthermore, credit card transactions represent **73.9%** of total transaction value ([07_payment_types_distribution.png](file:///c:/Users/Lenovo/Desktop/PROJECT%2001%20E-Commerce%20Sales%20Analysis/visualizations/07_payment_types_distribution.png)), which means disputes and chargebacks are a major threat to revenue.
* **Recommendation**: 
  * Enforce strict Service Level Agreements (SLAs) with logistics carriers, penalizing repeat shipping delays.
  * Establish an automated system that flags 1-star and 2-star reviews instantly, triggering a customer service ticket.
  * Offer direct compensation (refunds or discount vouchers) within 24 hours of a poor review to recover unhappy customers, preventing brand damage and credit card chargeback costs.

---

## 5. Most Surprising Finding
The most surprising finding is that during the **November 2017 peak (Black Friday)**, despite total orders spiking by over **63%** (from 4,547 to 7,421) and total monthly revenue hitting a record R$ 1.00M, the **Average Order Value (AOV) actually dropped to R$ 135.27** (down from R$ 145.19 in October). This indicates that the volume spike was driven by customers purchasing lower-priced discounted items rather than larger bulk orders, suggesting that promotions should focus on upselling complementary items during peak sales.
