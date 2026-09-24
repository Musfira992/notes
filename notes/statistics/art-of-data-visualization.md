---
title: "The Art of Data Visualisation"
date: 2026-09-06
source: https://www.musfirajamil.com/blog/art-of-data-visualization
---

# The Art of Data Visualisation

_Visualisation as disciplined communication: choose honest encodings, reduce clutter, use colour carefully, and let the analytical question drive the chart._

Data visualisation is where analysis meets understanding. A clear chart can surface a batch effect, a cohort imbalance, or a surprising biological pattern in seconds; a confusing chart can hide the same signal for weeks. The "art" is not decoration, it is disciplined communication.

This primer focuses on practical choices for analysts working across bioinformatics and general data work, using Australian English spelling throughout: we are talking about **visualisation**.

## Begin with the question

Every figure should answer a question a reader actually has. Examples:

* Do treatment and control separate on global expression space?
* Which categories dominate the total, and by how much?
* How does a metric change over time or across batches?

If you cannot state the question in one sentence, pause before opening a plotting library. Visualisation without a question becomes gallery art, pleasant, not persuasive.

## Choose encodings that match the data

* **Position** along a common scale is the most accurate perceptual channel, prefer scatter and position-based comparisons when precision matters.
* **Length** (bars) works well for categorical magnitudes.
* **Colour** is excellent for categories or coarse gradients, poor for reading precise values.
* **Area and angle** (pies, poorly designed bubbles) are easy to misread, use sparingly.

Match chart type to structure: distributions (histograms, ECDFs, violin/box with care), relationships (scatter), compositions (stacked bars or clear tables), and change (line charts with honest baselines).

## Respect statistical honesty

Start axes at zero for bar charts of magnitudes. For line charts of change, truncated axes can be legitimate, but label them clearly. Show uncertainty when you have it (intervals, bootstrap bands) instead of implying false precision. Avoid dual axes that invite false alignment stories.

In omics QC, plot raw diagnostics before fancy summaries: library sizes, gene detection rates, PCA coloured by batch *and* biological labels. The boring plot often prevents the wrong conclusion.

## Reduce clutter; keep context

Remove chartjunk, heavy gridlines, 3D effects, ornamental legends. Keep what aids reading: units, sample sizes, and the definition of each series. Direct labels often beat a distant legend when there are few categories.

```
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6, 4))
ax.scatter(
 df["pc1"],
 df["pc2"],
 c=df["batch"].astype("category").cat.codes,
 alpha=0.8,
)
ax.set_xlabel("PC1")
ax.set_ylabel("PC2")
ax.set_title("PCA coloured by sequencing batch")
fig.tight_layout()
```

Prefer an explicit colour map and legend in figures you share, the sketch above is about structure, not a finished graphic.

## Colour with care

Use colourblind-safe palettes for anything shared widely. Reserve strong colours for the series that matter; grey out the rest. In heatmaps, diverging scales need a meaningful midpoint (often zero for centred values). Never rely on colour alone when print or projectors may flatten the story, reinforce with shape or facets.

## Small multiples beat overloaded panels

When you have several related views (per-chromosome, per-assay, per-site), facet them. Humans compare aligned small charts better than one chart with eight overlapping encodings. Consistency of scale across facets is a feature, not a limitation.

## Tables are visualisations too

Sometimes the best "plot" is a tidy table with sorted rows, clear units, and a handful of well-chosen summary columns. Dashboards that force every metric into a sparkline often make comparison harder, not easier.

## Iterate with an audience in mind

1. Draft for yourself, explore freely.
2. Edit for a colleague, remove jargon and ambiguous legends.
3. Polish for stakeholders, state the takeaway in the title or caption.

Captions should say what to notice, not merely repeat axis labels. "PC1 separates library prep batches more than genotype" is a caption; "PCA plot" is a missed opportunity.

## Closing

Great visualisation is empathy plus accuracy: you encode data so another person can see what you saw, or politely disagree with evidence in view. Master a small set of honest chart forms, label generously, and let the question drive the design. The art follows from that craft.
