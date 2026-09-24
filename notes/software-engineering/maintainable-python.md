---
title: "Tips for Writing Maintainable Python Code"
date: 2026-09-06
source: https://www.musfirajamil.com/blog/maintainable-python
---

# Tips for Writing Maintainable Python Code

_Practical habits for readable, reusable Python in analysis and bioinformatics, project layout, pinned environments, small tests, and clarity over cleverness._

Maintainable Python is less about cleverness and more about kindness to your future self, and to whoever inherits your analysis next quarter. In data analysis and bioinformatics, scripts often start as exploratory notebooks and quietly become production. A few habits keep that transition from becoming painful.

## Prefer clarity over cleverness

Readable code wins. Use descriptive names (`filtered_counts` over `df2`), keep functions short enough to skim, and avoid nesting that needs a map to parse. If a line needs a comment to explain *what* it does, rewrite the line. Reserve comments for *why*, the scientific rationale, the quirk in an upstream file, the reason a threshold exists.

```
def filter_low_counts(counts, min_cpm=1.0, min_samples=3):
 """Keep genes with CPM above threshold in enough samples."""
 cpm = counts.div(counts.sum(axis=0), axis=1) * 1e6
 keep = (cpm > min_cpm).sum(axis=1) >= min_samples
 return counts.loc[keep]
```

The docstring and names already carry most of the story.

## Structure projects early

Even small analyses benefit from a predictable layout:

* `data/raw` and `data/processed` (never overwrite raw).
* `src/` for reusable functions.
* `notebooks/` for exploration only.
* `scripts/` or `pipelines/` for runnable entry points.
* `tests/` for the bits that must not silently drift.

Move logic out of notebooks into modules as soon as you find yourself copying cells between projects. Notebooks are wonderful for thinking; modules are better for repeating.

## Dependencies are part of the science

Pin versions for anything that can change numerical results, `numpy`, `pandas`, Bioconductor bridges, plotting stacks. Record the environment with `requirements.txt`, `environment.yml`, or a lock file. In collaborative bioinformatics work, "it worked on my machine" is not a methodology section.

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Type hints and small interfaces

You do not need heavyweight typing everywhere. A few annotations on public functions make IDEs and reviewers more effective:

```
from pathlib import Path
import pandas as pd

def load_sample_sheet(path: Path) -> pd.DataFrame:
 return pd.read_csv(path, dtype={"sample_id": "string"})
```

Keep function signatures boring: explicit inputs, explicit outputs, minimal hidden global state.

## Handle paths and configuration deliberately

Hard-coded absolute paths break the moment someone else clones the repo. Prefer project-relative paths, environment variables for secrets and machine-specific roots, and a single config module or YAML file for analysis parameters (thresholds, genome build, output directories).

## Test the risky bits

You do not need 100% coverage. Test joins that drop rows, ID mapping, date parsing, and any custom statistic you would be embarrassed to get wrong. A tiny `pytest` suite on those functions pays for itself the first time a metadata column changes type.

```
def test_filter_low_counts_keeps_expressed_genes():
 counts = make_toy_counts()
 out = filter_low_counts(counts, min_cpm=1.0, min_samples=2)
 assert "highly_expressed_gene" in out.index
```

## Style tools are cheap insurance

Use a formatter (`ruff format` or `black`), a linter (`ruff`), and consistent import ordering. Agree once as a team and stop debating whitespace. Consistency lowers cognitive load when reviewing scientific code.

## A practical baseline

1. Name things for the domain, not the intermediate step number.
2. Separate exploration from reusable logic.
3. Pin dependencies that affect results.
4. Test irreversible or subtle transforms.
5. Document assumptions next to the code that encodes them.

Maintainable Python is a habit, not a rewrite project. Apply these practices incrementally, each cleaned function and pinned environment makes the next analysis safer and faster.
