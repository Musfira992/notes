---
title: "Common Analytics Query Patterns"
date: 2026-09-06
source: https://www.musfirajamil.com/blog/databricks-series-analytics-query-patterns
---

# Common Analytics Query Patterns

_Reusable SQL patterns for analytics on Databricks: filters, aggregations, window functions, cohort logic, and star-schema joins._

Most analytics work is a small set of patterns repeated with different columns. Learn the patterns once, and Databricks SQL (or Spark SQL) becomes much faster to write, and easier to review.

## Filter then aggregate

Start with a clear grain, filter early, then group. Push predicates that prune partitions (especially date) as close to the base table as you can.

```
SELECT
 product_category,
 SUM(net_amount) AS revenue,
 COUNT(DISTINCT order_id) AS orders
FROM gold.fact_orders f
JOIN gold.dim_product p ON f.product_key = p.product_key
JOIN gold.dim_date d ON f.order_date_key = d.date_key
WHERE d.full_date BETWEEN DATE '2026-01-01' AND DATE '2026-03-31'
GROUP BY product_category
ORDER BY revenue DESC;
```

## Time series and period comparisons

Window functions compare a row to its neighbours without collapsing the grain. Use them for running totals, previous-period values, and moving averages.

```
SELECT
 full_date,
 daily_revenue,
 LAG(daily_revenue, 7) OVER (ORDER BY full_date) AS revenue_7d_ago,
 AVG(daily_revenue) OVER (
 ORDER BY full_date
 ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
 ) AS moving_avg_7d
FROM daily_sales;
```

## Ranking and top-N

Rank within a partition when stakeholders ask for "top products per region". Prefer `ROW_NUMBER` when you need a deterministic single winner, and `DENSE_RANK` when ties should share a rank.

```
WITH ranked AS (
 SELECT
 region,
 product_name,
 revenue,
 ROW_NUMBER() OVER (
 PARTITION BY region
 ORDER BY revenue DESC
 ) AS rn
 FROM region_product_revenue
)
SELECT * FROM ranked WHERE rn <= 5;
```

## Cohorts and retention sketches

Cohort analysis groups users by first activity month, then tracks return activity. Keep the cohort assignment in a reusable view so dashboards stay consistent.

```
WITH first_order AS (
 SELECT customer_key, MIN(full_date) AS cohort_date
 FROM gold.fact_orders f
 JOIN gold.dim_date d ON f.order_date_key = d.date_key
 GROUP BY customer_key
)
SELECT
 date_trunc('MONTH', fo.cohort_date) AS cohort_month,
 date_trunc('MONTH', d.full_date) AS activity_month,
 COUNT(DISTINCT f.customer_key) AS active_customers
FROM gold.fact_orders f
JOIN gold.dim_date d ON f.order_date_key = d.date_key
JOIN first_order fo ON f.customer_key = fo.customer_key
GROUP BY 1, 2;
```

## Star joins and bridge tables

Join facts to dimensions on surrogate keys. When a fact relates to many values of one dimension (for example an order with many promotions), use a bridge table rather than exploding the fact grain silently.

## Semi-additive and careful measures

Not everything sums. Account balances and inventory snapshots are semi-additive: you may sum across products but not across days. Document that in the catalogue and encode it in metrics views so tools do not invent wrong totals.

* Use `SUM` for additive facts like revenue and quantity.
* Use last-in-period logic for snapshots.
* Prefer distinct counts only when the grain truly requires them, they are expensive.

## Make patterns reusable

Wrap stable logic in views or metric layers. Keep notebooks for exploration, not as the only definition of "monthly revenue". When a pattern shows up three times, promote it. That is how analytics teams stay organised as the lakehouse grows.
