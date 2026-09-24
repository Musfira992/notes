---
title: "3 Common Data Modeling Techniques"
date: 2026-09-06
source: https://www.musfirajamil.com/blog/databricks-series-data-modeling-techniques
---

# 3 Common Data Modeling Techniques

_A practical tour of flat, relational, and dimensional modelling, with Databricks SQL examples so you can choose the right shape for analytics and pipelines._

Data modelling is how you decide what your tables mean and how they relate. In Databricks you will often meet three styles: **flat**, **relational**, and **dimensional**. None is universally best. Each trades simplicity against flexibility, and each fits different stages of a lakehouse pipeline.

## Flat models

A flat model is a single wide table: one row per event or entity, with many columns and little or no joining. Think of a CSV of sales with customer name, product name, and region all denormalised onto the same row. Flat models are easy to load, easy to query for beginners, and common for landing zones or feature tables.

The downside is redundancy. The same customer details repeat on every order row. Updates become painful, and storage grows. Flat tables also encourage analytics that are hard to reuse across teams.

```
CREATE OR REPLACE TABLE sales_flat AS
SELECT
 order_id,
 order_date,
 customer_id,
 customer_name,
 product_id,
 product_name,
 quantity,
 unit_price,
 quantity * unit_price AS line_amount
FROM bronze.orders_raw;
```

Use flat models for exploration, machine learning feature stores, or narrow reporting extracts. Avoid them as the long-term system of record when many teams need consistent definitions.

## Relational models

Relational modelling normalises entities into related tables: customers, products, orders, order lines. Keys link them. This is the classic OLTP and enterprise warehouse style. In Databricks it often appears in silver layers where you clean and conform source systems.

```
CREATE OR REPLACE TABLE dim_customer_rel (
 customer_id STRING PRIMARY KEY,
 customer_name STRING,
 email STRING,
 city STRING
);

CREATE OR REPLACE TABLE fact_order_line_rel (
 order_line_id STRING PRIMARY KEY,
 order_id STRING,
 customer_id STRING,
 product_id STRING,
 quantity INT,
 unit_price DECIMAL(12,2)
);
```

Queries then join on keys:

```
SELECT c.customer_name, SUM(f.quantity * f.unit_price) AS revenue
FROM fact_order_line_rel f
JOIN dim_customer_rel c ON f.customer_id = c.customer_id
GROUP BY c.customer_name;
```

Relational models reduce duplication and protect integrity. They can be slower for heavy analytics if you join many large tables without good partitioning and clustering. They also ask analysts to understand the schema deeply.

## Dimensional models

Dimensional modelling organises data for analysis: *facts* hold measures (sales amount, quantity), and *dimensions* hold descriptive context (date, customer, product). The classic star schema puts one fact table at the centre with dimensions around it.

```
CREATE OR REPLACE TABLE fact_sales (
 date_key INT,
 customer_key BIGINT,
 product_key BIGINT,
 quantity INT,
 sales_amount DECIMAL(14,2)
);

CREATE OR REPLACE TABLE dim_product (
 product_key BIGINT,
 product_id STRING,
 product_name STRING,
 category STRING
);
```

Dimensional models shine for BI tools and repeated business questions: revenue by category, orders by month, churn by segment. They are usually built in gold layers after you have cleaned relational or semi-structured sources.

## Choosing in Databricks

* **Bronze:** keep close to source, often flat or lightly structured.
* **Silver:** relational or well-keyed entities for reuse.
* **Gold:** dimensional stars or wide flat marts for consumption.

Start from the questions people ask. If analysts need flexible drill-downs across many attributes, lean dimensional. If you are integrating operational systems, lean relational. If you need a fast one-off extract, a flat table is fine, just do not pretend it is a warehouse.

Good modelling is less about dogma and more about clarity: every column should have a clear grain, a clear owner, and a clear path into the next layer of your lakehouse.
