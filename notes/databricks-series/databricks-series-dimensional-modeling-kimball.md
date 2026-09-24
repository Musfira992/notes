---
title: "Dimensional Modeling and Kimball Architecture"
date: 2026-09-06
source: https://www.musfirajamil.com/blog/databricks-series-dimensional-modeling-kimball
---

# Dimensional Modeling and Kimball Architecture

_How Kimball-style dimensional modelling maps onto a Databricks lakehouse: facts, dimensions, conformed keys, and practical design habits._

Kimball dimensional modelling is a practical way to design analytics data so business questions are easy to ask and hard to get wrong. In Databricks, the same ideas sit comfortably in a medallion lakehouse: cleaned silver entities feed gold stars that BI tools and SQL notebooks consume.

## Core ideas

A **fact table** records measurable events at a declared grain, for example one row per order line per day. A **dimension table** describes the who, what, where, and when. Surrogate keys (integers or bigints you generate) link facts to dimensions so natural keys from source systems can change without breaking history.

* **Grain:** state the grain in one sentence before you write DDL.
* **Additive measures:** prefer amounts you can sum safely across dimensions.
* **Conformed dimensions:** shared date, customer, and product dims across marts.

## Star schema shape

In a star, the fact sits in the middle. Dimensions hang off it with few joins. Snowflakes normalise dimensions further (product to category to department). Stars are usually simpler for analysts; snowflakes can reduce duplication but add join complexity.

```
CREATE OR REPLACE TABLE gold.fact_orders (
 order_date_key INT NOT NULL,
 customer_key BIGINT NOT NULL,
 product_key BIGINT NOT NULL,
 order_id STRING NOT NULL,
 quantity INT,
 net_amount DECIMAL(14,2),
 CONSTRAINT pk_fact_orders PRIMARY KEY (order_id, product_key)
);

CREATE OR REPLACE TABLE gold.dim_date (
 date_key INT PRIMARY KEY,
 full_date DATE,
 year INT,
 month_name STRING,
 fiscal_quarter STRING
);
```

## Slowly changing dimensions

Customer attributes change. Kimball Type 1 overwrites the current value. Type 2 keeps history with effective dates or version rows. In Databricks, Delta tables make Type 2 practical: merge new versions, expire old ones, and point facts at the correct surrogate key for that point in time.

```
-- Conceptual Type 2 pattern
MERGE INTO gold.dim_customer t
USING staging.customer_changes s
ON t.customer_id = s.customer_id AND t.is_current = true
WHEN MATCHED AND t.email <> s.email THEN UPDATE SET
 t.is_current = false,
 t.valid_to = current_date()
WHEN NOT MATCHED THEN INSERT *;
```

Keep SCD logic in one place (a notebook job or dbt model) so every mart inherits the same history rules.

## Kimball on a lakehouse

Classic Kimball assumed a relational warehouse bus. On Databricks you still want a *bus*: shared conformed dimensions published once, then reused. What changes is storage and compute, Delta Lake, Unity Catalog, and SQL warehouses, not the modelling discipline.

1. Define business processes and grains with stakeholders.
2. Build conformed dimensions in gold (date, customer, product).
3. Load facts with surrogate keys and declared additive measures.
4. Document grain, sources, and refresh cadence in the catalogue.

## Practical habits

Name tables clearly (`fact_` and `dim_`). Avoid putting descriptive text on facts. Prefer integer date keys for pruning. Partition large facts by date when queries filter that way, and liquid-cluster or Z-order high-cardinality join keys when needed.

Kimball is not ceremony for its own sake. It is a shared language: when someone says "the grain is one shipment per day", everyone knows what a duplicate means and which dashboard is trustworthy. That clarity is what makes dimensional modelling worth learning in Databricks.
