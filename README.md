# Technical Notes

**Live handbook:** [https://musfira992.github.io/notes/](https://musfira992.github.io/notes/)

A browsable handbook of technical notes and primers spanning genomics, Databricks, software engineering, statistics, and laboratory techniques. The published site is a Pandoc HTML build with a table of contents and readable typography. The Markdown sources in this repository remain the source of truth.

## Who this is for

- Bioinformatics and computational biology learners who need approachable primers
- Data engineers and analysts working with Databricks, Spark, and lakehouse patterns
- Software-minded scientists who want maintainable Python, Git, and UNIX habits
- Anyone refreshing core statistics, visualisation, or wet-lab technique foundations

## About the author

These notes are by [Musfira Jamil](https://www.musfirajamil.com). Explore more writing, research, and projects on the personal site, or follow the work on GitHub at [github.com/Musfira992](https://github.com/Musfira992).

## Origin

Content in this repository originated as **Primers** on [musfirajamil.com](https://www.musfirajamil.com/primers). Each note here is a Markdown migration of that material so the library can be browsed as a handbook site, on GitHub, or with GitBook-style tooling.

## How to browse

- **Handbook website (recommended):** [https://musfira992.github.io/notes/](https://musfira992.github.io/notes/) - single-page handbook with TOC, categories, and all notes rendered to HTML.
- **On GitHub:** open files under `notes/` from the table of contents below.
- **With GitBook:** this repo includes a `SUMMARY.md` sidebar table of contents. Point GitBook (or compatible docs tooling) at the repository root.
- **Interactive widgets:** some tutorials (for example the DNA sequence primer) keep interactive widgets on https://www.musfirajamil.com/primers.

## Rebuild the handbook

Requires [Pandoc](https://pandoc.org/). From the repository root:

```bash
./scripts/build-handbook.sh
```

This regenerates `docs/index.html`, `docs/styles.css`, and `docs/.nojekyll` from `SUMMARY.md` order and the Markdown files under `notes/`. GitHub Pages serves the site from the `/docs` folder on `main`.

## Table of contents

### Interactive Tutorials

- [Reading a DNA Sequence](notes/interactive-tutorials/reading-a-dna-sequence.md)

### Genomics

- [DeepExplainer on Simulated Genomic Data (DeepLIFT)](notes/genomics/deepexplainer-simulated-genomic-data-deeplift.md)

### DataBricks Series

- [AI Drug Discovery Made Easy: Your Complete Guide to Chemprop on Databricks](notes/databricks-series/chemprop-drug-discovery-on-databricks.md)
- [3 Common Data Modeling Techniques](notes/databricks-series/databricks-series-data-modeling-techniques.md)
- [Dimensional Modeling and Kimball Architecture](notes/databricks-series/databricks-series-dimensional-modeling-kimball.md)
- [DataBricks Series - SQL Fundamentals](notes/databricks-series/databricks-series-sql-fundamentals.md)
- [Common Analytics Query Patterns](notes/databricks-series/databricks-series-analytics-query-patterns.md)
- [Processing Big Data with Apache Spark in Databricks](notes/databricks-series/databricks-series-apache-spark.md)
- [Building Data Pipelines in Databricks](notes/databricks-series/databricks-series-data-pipelines.md)

### Software Engineering

- [On Building Reliable Data Products](notes/software-engineering/building-reliable-data-products.md)
- [Tips for Writing Maintainable Python Code](notes/software-engineering/maintainable-python.md)
- [Common UNIX Commands](notes/software-engineering/common-unix-commands.md)
- [Git Essentials](notes/software-engineering/git-essentials.md)
- [Hello Julia](notes/software-engineering/hello-julia.md)
- [Software Engineering Concepts Every Bioinformatics Professional Should Know](notes/software-engineering/software-engineering-for-bioinformatics.md)

### Statistics

- [The Art of Data Visualisation](notes/statistics/art-of-data-visualization.md)
- [Exploratory Data Analysis](notes/statistics/exploratory-data-analysis.md)

### Data Generation Techniques

- [DNA/RNA Extraction](notes/data-generation-techniques/dna-rna-extraction.md)
- [Protein Extraction](notes/data-generation-techniques/protein-extraction.md)
- [Western Blotting](notes/data-generation-techniques/western-blotting.md)
- [PCR](notes/data-generation-techniques/pcr-primer.md)
- [Agarose Gel Electrophoresis](notes/data-generation-techniques/agarose-gel-electrophoresis.md)
- [SDS-PAGE, Cloning, and Recombinant DNA Technology](notes/data-generation-techniques/sds-page-cloning-recombinant-dna.md)

## Repository layout

```
README.md
SUMMARY.md
book.json
scripts/build-handbook.sh
docs/                 # GitHub Pages site (Pandoc HTML)
  index.html
  styles.css
  .nojekyll
notes/
  interactive-tutorials/
  genomics/
  databricks-series/
  software-engineering/
  statistics/
  data-generation-techniques/
```

Questions or corrections are welcome via the personal site. Happy learning.
