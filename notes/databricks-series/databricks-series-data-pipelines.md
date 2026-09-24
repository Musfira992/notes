---
title: "Building Data Pipelines in Databricks"
date: 2026-09-06
source: https://www.musfirajamil.com/blog/databricks-series-data-pipelines
---

# Building Data Pipelines in Databricks

_A practical guide to Databricks pipelines: medallion layers, incremental loads, orchestration, quality checks, and operational habits that keep data trustworthy._

A data pipeline moves information from sources to something people can trust, tables, dashboards, or models, on a schedule and with clear ownership. In Databricks that usually means notebooks or workflows reading raw files or CDC streams, writing Delta tables through bronze, silver, and gold layers, and publishing into Unity Catalog.

## Medallion layers as a contract

* **Bronze:** append-only landing, schema-on-read or lightly typed, retain source quirks.
* **Silver:** cleaned, deduplicated, conformed entities and events.
* **Gold:** business marts, dimensional models, and aggregates for consumption.

Treat each layer as a contract. Downstream jobs should not reach into bronze for business logic. That separation keeps reprocessing and debugging organised when a source changes shape.

## Incremental over full reload

Prefer incremental processing: read only new files, new partitions, or Change Data Feed rows, then merge into silver. Full reloads are fine for small dimensions; they become costly and slow for large facts.

```
-- Merge daily increments into silver
MERGE INTO silver.orders t
USING staging.orders_day s
ON t.order_id = s.order_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;
```

Idempotency matters. Re-running yesterday's job should not double-count. Use deterministic keys, merge logic, and partition overlays so retries are safe.

## Orchestration with Workflows

Databricks Workflows (jobs) chain tasks: ingest, transform, test, and notify. Keep tasks small and explicit, one responsibility per task, so failures are easy to isolate. Pass parameters for run dates rather than hard-coding paths inside notebooks.

1. Ingest to bronze (Auto Loader or batch copy).
2. Transform to silver with validation.
3. Build gold marts.
4. Run data quality checks and refresh downstream caches.

## Quality and observability

Pipelines without checks eventually lie. Add expectations at silver: non-null keys, valid ranges, referential integrity samples. Quarantine bad rows instead of failing silently. Emit row counts and freshness metrics so on-call engineers can see whether gold is stale before stakeholders do.

```
from pyspark.sql import functions as F

silver = spark.table("silver.orders")
assert silver.filter(F.col("order_id").isNull()).count() == 0
freshness_hours = (
 spark.sql(
 "SELECT (unix_timestamp() - unix_timestamp(MAX(_ingested_at))) / 3600 "
 "FROM silver.orders"
 ).first()[0]
)
```

## Governance and environments

Use Unity Catalog for permissions and lineage. Separate dev, staging, and prod catalogues or schemas. Promote code through repos and job definitions, not by editing production notebooks by hand. Secrets belong in secret scopes, never in cells.

## Design for change

Sources evolve. Version schemas thoughtfully, prefer additive columns, and document breaking changes. Keep visualisation and BI tools pointed at gold views so you can rearrange physical tables without breaking every dashboard.

Good Databricks pipelines are boring in the best way: incremental, tested, observable, and layered. When those habits are in place, modelling and analytics work can move quickly without sacrificing trust.
