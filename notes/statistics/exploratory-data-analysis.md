---
title: "Exploratory Data Analysis"
date: 2026-09-06
source: https://www.musfirajamil.com/blog/exploratory-data-analysis
---

# Exploratory Data Analysis

_A practical EDA sequence for analysts and bioinformaticians, inventory, quality, distributions, relationships, high-dimensional structure, and documented decisions._

Exploratory data analysis (EDA) is the disciplined habit of looking before you model. In bioinformatics and applied analytics, EDA is how you discover batch effects, mislabelled samples, skewed distributions, and the shape of relationships that should inform, or forbid, a particular method. Skipping it is how elegant models fail on contact with reality.

## What EDA is for

EDA answers questions like:

* What is in this dataset, at what grain, and how complete is it?
* Where are outliers, missingness patterns, and impossible values?
* Which variables dominate variation, and are they biological or technical?
* Are groups balanced enough for the comparison we want?

It is not a substitute for confirmatory analysis. It is the map you draw so confirmatory work asks fair questions.

## A practical sequence

1. **Inventory**, dimensions, types, primary keys, joinability to metadata.
2. **Quality**, missingness, duplicates, range checks, unit sanity.
3. **Univariate views**, distributions of key measures.
4. **Relationships**, pairwise plots, correlations with caveats, stratified summaries.
5. **Structure**, PCA/MDS or clustering for high-dimensional assays; contingency views for categorical designs.
6. **Notes**, write down surprises while they are fresh.

## Start with metadata alignment

Before plotting expression or sensor streams, confirm that every measurement column matches a metadata row. Check ID formats, rename maps, and one-to-one expectations. Many "biological" PCA separations are actually swapped labels or mixed genome builds.

```
assert set(counts.columns) == set(meta["sample_id"])
meta = meta.set_index("sample_id").loc[counts.columns]
```

Assertions like these are EDA infrastructure, cheap and invaluable.

## Distributions before means

Summary tables hide multimodality. Plot library sizes, gene-wise detection rates, ages, doses, or whatever drives your domain. Ask whether a log transform is needed, whether zeros are structural, and whether a few samples dominate totals.

For counts data, mean-variance trends and filter effects deserve a look before differential testing. For tabular business or field data, histograms and ECDFs often beat a single KPI tile.

## Missing data is a pattern, not a nuisance

Plot missingness by column and by row. Is it random, block-wise (an assay failed), or informative (not measured below a limit)? The mechanism changes whether imputation, exclusion, or explicit "missing" categories are appropriate. Do not silently drop rows in a pipeline without recording how many disappeared and why.

## Relationship views with humility

Scatterplots, box plots by group, and simple correlation matrices are useful, and easy to over-interpret. Correlation is not causation; confounding is common in observational biological and agricultural data. Use EDA to generate hypotheses and to spot confounders (batch, site, depth, age) that belong in later models.

## High-dimensional structure

For omics matrices, PCA or similar embeddings coloured by technical and biological factors are standard EDA. Look at scree plots: if early components track plate or prep date more than condition, address that before celebrating a volcano plot. Complementary views, hierarchical clustering of samples, QC metric overlays, help confirm the story.

```
# Sketch: standardise and compute PCA on a feature matrix X
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

X_std = StandardScaler().fit_transform(X)
pcs = PCA(n_components=10).fit_transform(X_std)
```

## Keep a running log

EDA that lives only in scrollback is wasted. Keep a short markdown or notebook section: filters applied, samples removed, oddities pending follow-up. That log becomes methods text and protects you when a result needs auditing.

## Time-box exploration

EDA can expand forever. Set a goal ("decide whether batch correction is needed", "confirm cohort eligibility") and a time box. When the goal is met, write the decision and move to confirmatory analysis. You can always return with a sharper question.

## Closing

Good EDA is curious, sceptical, and documented. It privileges plots and checks that could change your mind. Build a repeatable personal checklist for each new dataset, inventory, quality, distributions, relationships, structure, notes, and you will catch more truth earlier, with fewer heroic debugging sessions later.
