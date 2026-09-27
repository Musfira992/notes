# Technical Notes

Five short handbooks of learning notes and primers.

**Library:** [https://www.musfirajamil.com/notes/](https://www.musfirajamil.com/notes/)

| Handbook | Live page | Sources |
| --- | --- | --- |
| [Genomics](books/genomics/README.md) | [/notes/genomics/](https://www.musfirajamil.com/notes/genomics/) | `notes/genomics/`, `notes/interactive-tutorials/` |
| [Databricks](books/databricks/README.md) | [/notes/databricks/](https://www.musfirajamil.com/notes/databricks/) | `notes/databricks-series/` |
| [Software Engineering for Bioinformatics](books/software-engineering/README.md) | [/notes/software-engineering/](https://www.musfirajamil.com/notes/software-engineering/) | `notes/software-engineering/` |
| [Statistics](books/statistics/README.md) | [/notes/statistics/](https://www.musfirajamil.com/notes/statistics/) | `notes/statistics/` |
| [Data Generation Techniques](books/data-generation/README.md) | [/notes/data-generation/](https://www.musfirajamil.com/notes/data-generation/) | `notes/data-generation-techniques/` |

GitHub Pages serves the `/docs` folder on `main`. The custom domain stays `www.musfirajamil.com`, and this library is published at `/notes/`. `docs/index.html` is the hub. Each handbook is `docs/<slug>/index.html`.

## Who this is for

- Bioinformatics and computational biology learners who need approachable primers
- Data engineers and analysts working with Databricks, Spark, and lakehouse patterns
- Software-minded scientists who want maintainable Python, Git, and UNIX habits
- Anyone refreshing core statistics, visualisation, or wet-lab technique foundations

## About the author

These notes are by [Musfira Jamil](https://www.musfirajamil.com). Explore more writing, research, and projects on the personal site, or follow the work on GitHub at [github.com/Musfira992](https://github.com/Musfira992).

## Origin

Content in this repository originated as primers on [musfirajamil.com](https://www.musfirajamil.com/primers), and as learning notes written while picking up a topic. Each chapter is still the Markdown file under `notes/`. The site groups those files into five handbooks and a short hub.

## How to browse

- **Handbook website (recommended):** the hub and the five live pages in the table above. Each handbook has a table of contents and the chapter prose.
- **On GitHub:** open a book under `books/<slug>/`, or open chapter files from the lists below.
- **With GitBook:** the repository root is the library (`README.md`, `SUMMARY.md`, and `book.json`). It lists the five books. It is not a single table of contents of every chapter. Each mini-book is its own GitBook root at `books/<slug>/`, with that directory's `book.json` and `SUMMARY.md`. Chapter links in those summaries are relative to the book directory and point at `notes/`.
- **Interactive widgets:** some tutorials (for example the DNA sequence primer) keep interactive widgets on https://www.musfirajamil.com/primers. That primer is a chapter of the Genomics handbook. Its Markdown stays in `notes/interactive-tutorials/`.

## Rebuild the site

Requires [Pandoc](https://pandoc.org/). From the repository root:

```bash
./scripts/build-handbook.sh
```

The script reads each `books/<slug>/SUMMARY.md` and `books/<slug>/book.json`, assembles one manuscript per handbook, and writes:

- `docs/index.html` (hub for [/notes/](https://www.musfirajamil.com/notes/))
- `docs/genomics/index.html`
- `docs/databricks/index.html`
- `docs/software-engineering/index.html`
- `docs/statistics/index.html`
- `docs/data-generation/index.html`
- `docs/.nojekyll`

Shared styling lives in `docs/styles.css`. The hub links to `styles.css`. Each handbook links to `../styles.css`, so the sheet loads when the page is served from `/notes/<slug>/`. The build checks those links, the five tables of contents, and that each chapter landed in the handbook named by its summary.

## Book layout

Mini-books live under `books/`. Slugs match the published paths. Chapter files stay in `notes/`.

```
books/<slug>/
  README.md     # introduction and chapter list for GitBook and GitHub
  SUMMARY.md    # GitBook table of contents for this book only
  book.json     # title, subtitle, and GitBook structure
```

`title` and `subtitle` in `book.json` become the handbook title block. The first paragraph of `README.md` is the blurb on the hub and at the top of that handbook. Link chapters with a path relative to the book directory, such as `../../notes/genomics/example.md`.

| Slug | GitBook root | Chapter sources |
| --- | --- | --- |
| `genomics` | `books/genomics/` | `notes/genomics/`, `notes/interactive-tutorials/` |
| `databricks` | `books/databricks/` | `notes/databricks-series/` |
| `software-engineering` | `books/software-engineering/` | `notes/software-engineering/` |
| `statistics` | `books/statistics/` | `notes/statistics/` |
| `data-generation` | `books/data-generation/` | `notes/data-generation-techniques/` |

## Chapters

### Genomics

Published at [/notes/genomics/](https://www.musfirajamil.com/notes/genomics/).

- [Reading a DNA Sequence](notes/interactive-tutorials/reading-a-dna-sequence.md)
- [DeepExplainer on Simulated Genomic Data (DeepLIFT)](notes/genomics/deepexplainer-simulated-genomic-data-deeplift.md)

### Databricks

Published at [/notes/databricks/](https://www.musfirajamil.com/notes/databricks/).

- [AI Drug Discovery Made Easy: Your Complete Guide to Chemprop on Databricks](notes/databricks-series/chemprop-drug-discovery-on-databricks.md)
- [3 Common Data Modeling Techniques](notes/databricks-series/databricks-series-data-modeling-techniques.md)
- [Dimensional Modeling and Kimball Architecture](notes/databricks-series/databricks-series-dimensional-modeling-kimball.md)
- [DataBricks Series - SQL Fundamentals](notes/databricks-series/databricks-series-sql-fundamentals.md)
- [Common Analytics Query Patterns](notes/databricks-series/databricks-series-analytics-query-patterns.md)
- [Processing Big Data with Apache Spark in Databricks](notes/databricks-series/databricks-series-apache-spark.md)
- [Building Data Pipelines in Databricks](notes/databricks-series/databricks-series-data-pipelines.md)

### Software Engineering for Bioinformatics

Published at [/notes/software-engineering/](https://www.musfirajamil.com/notes/software-engineering/).

- [On Building Reliable Data Products](notes/software-engineering/building-reliable-data-products.md)
- [Tips for Writing Maintainable Python Code](notes/software-engineering/maintainable-python.md)
- [Common UNIX Commands](notes/software-engineering/common-unix-commands.md)
- [Git Essentials](notes/software-engineering/git-essentials.md)
- [Hello Julia](notes/software-engineering/hello-julia.md)
- [Software Engineering Concepts Every Bioinformatics Professional Should Know](notes/software-engineering/software-engineering-for-bioinformatics.md)

### Statistics

Published at [/notes/statistics/](https://www.musfirajamil.com/notes/statistics/).

- [The Art of Data Visualisation](notes/statistics/art-of-data-visualization.md)
- [Exploratory Data Analysis](notes/statistics/exploratory-data-analysis.md)

### Data Generation Techniques

Published at [/notes/data-generation/](https://www.musfirajamil.com/notes/data-generation/).

- [DNA/RNA Extraction](notes/data-generation-techniques/dna-rna-extraction.md)
- [Protein Extraction](notes/data-generation-techniques/protein-extraction.md)
- [Western Blotting](notes/data-generation-techniques/western-blotting.md)
- [PCR](notes/data-generation-techniques/pcr-primer.md)
- [Agarose Gel Electrophoresis](notes/data-generation-techniques/agarose-gel-electrophoresis.md)
- [SDS-PAGE, Cloning, and Recombinant DNA Technology](notes/data-generation-techniques/sds-page-cloning-recombinant-dna.md)

## Repository layout

```
README.md                 # this library guide
SUMMARY.md                # library table of contents (five books)
book.json                 # GitBook config for the library
scripts/build-handbook.sh
scripts/assemble_handbooks.py
books/
  genomics/
  databricks/
  software-engineering/
  statistics/
  data-generation/
docs/                     # GitHub Pages site
  index.html              # hub
  styles.css
  .nojekyll
  genomics/index.html
  databricks/index.html
  software-engineering/index.html
  statistics/index.html
  data-generation/index.html
notes/                    # chapter sources, left in place
  interactive-tutorials/
  genomics/
  databricks-series/
  software-engineering/
  statistics/
  data-generation-techniques/
```

Questions or corrections are welcome via the personal site. Happy learning.
