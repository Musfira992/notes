---
title: "Processing Big Data with Apache Spark in Databricks"
date: 2026-09-06
source: https://www.musfirajamil.com/blog/databricks-series-apache-spark
---

# Processing Big Data with Apache Spark in Databricks

_How Apache Spark powers Databricks workloads: DataFrames, transformations, partitioning, and practical habits for reliable large-scale processing._

Apache Spark is the distributed engine underneath most Databricks data engineering. You write transformations against DataFrames (or SQL), and Spark plans them across a cluster. Understanding a few core ideas, lazy evaluation, partitions, shuffle, and caching, pays off quickly when jobs slow down or spill to disk.

## DataFrames, not rows in a loop

Spark works best when you describe *what* you want in bulk operations: filter, select, join, aggregate. Avoid collecting large results to the driver or writing Python loops over partitions unless you truly need custom logic via pandas UDFs or mapInPandas.

```
from pyspark.sql import functions as F

df = spark.table("silver.orders")
clean = (
 df
 .filter(F.col("order_date") >= "2026-01-01")
 .withColumn("line_amount", F.col("quantity") * F.col("unit_price"))
 .groupBy("customer_id")
 .agg(F.sum("line_amount").alias("revenue"))
)
clean.write.mode("overwrite").saveAsTable("gold.customer_revenue")
```

## Lazy plans and actions

Transformations build a logical plan. Actions such as `count`, `collect`, `show`, or a write trigger execution. That laziness lets Catalyst optimise the whole pipeline. Chain filters before wide joins when you can, and prefer SQL or DataFrame APIs over opaque UDFs so the optimiser can see your intent.

## Partitions and shuffle

Data is split into partitions processed in parallel. A **shuffle** redistributes data for joins and group-bys. Shuffles are expensive: they move bytes across the network and can create skew when one key dominates.

* Filter and project early to shrink shuffle input.
* Broadcast small dimension tables with `broadcast()` or rely on auto-broadcast hints when sizes allow.
* Watch for skew, salting keys or Adaptive Query Execution (AQE) can help.

```
from pyspark.sql.functions import broadcast

facts = spark.table("gold.fact_orders")
dim_prod = spark.table("gold.dim_product")
joined = facts.join(broadcast(dim_prod), "product_key")
```

## Delta Lake and Spark together

In Databricks you usually read and write Delta tables. ACID transactions, time travel, and `MERGE` make incremental pipelines safer than raw Parquet folders. Combine Spark transformations with Delta features: optimise layout, vacuum old files carefully, and use Change Data Feed when downstream jobs need only the deltas.

## Cluster and job habits

1. Use job clusters for scheduled work; keep interactive clusters for development.
2. Size for the shuffle-heavy stages, not only the scan.
3. Prefer Photon-accelerated SQL warehouses for BI-shaped queries when available.
4. Log metrics: rows in, rows out, duration, and data skipped by partition pruning.

## When Spark is the right tool

Spark shines for large batch and micro-batch ETL, feature engineering, and joins that no longer fit on a single machine. For lightweight transforms on small tables, a SQL warehouse query may be simpler and cheaper. Match the engine to the data volume and latency, not to habit.

Think in DataFrames, respect the shuffle, and keep tables in Delta with clear layers. That combination is the everyday craft of processing big data in Databricks.
