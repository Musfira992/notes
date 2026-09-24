---
title: "Common UNIX Commands"
date: 2026-09-06
source: https://www.musfirajamil.com/blog/common-unix-commands
---

# Common UNIX Commands

_A compact UNIX toolkit for analysts and bioinformaticians, inspecting large files, composing pipes, compression, search, and everyday shell hygiene._

UNIX command-line tools remain the fastest way to inspect files, glue workflows together, and survive large bioinformatics datasets without opening a GUI. You do not need to memorise everything, a compact toolkit covers most day-to-day work for analysts and data engineers.

This primer focuses on commands I reach for constantly when exploring sequencing outputs, logs, and tabular intermediates.

## Moving around and seeing what is there

```
pwd
ls -lah
cd /path/to/project
tree -L 2 # if installed
```

`ls -lah` shows hidden files, human-readable sizes, and permissions. Permissions matter when shared cluster directories refuse to write.

## Peeking at files safely

Never open a multi-gigabyte FASTQ in a graphical editor. Use streaming viewers:

```
head -n 20 sample.fastq
tail -n 50 run.log
less big_matrix.tsv
wc -l counts.csv
```

`less` lets you search with `/` and quit with `q`. `wc -l` is a quick sanity check after filters.

## Finding things

```
find data/raw -name "*.fastq.gz"
grep -n "ERROR" logs/pipeline.log
rg "sample_id" metadata/ # ripgrep, if available
```

`find` locates files by name or pattern; `grep`/`rg` locate text inside files. Prefer ripgrep on large codebases, it is fast and respects ignore rules.

## Compression and archives

Omics data lives compressed. Essential patterns:

```
gzip file.txt
gunzip file.txt.gz
zcat sample.fastq.gz | head
tar -xzf archive.tar.gz
tar -czf backup.tar.gz results/
```

`zcat` (or `gzip -dc`) streams compressed text without writing an uncompressed copy to disk, invaluable on clusters with tight quotas.

## Pipes, redirects, and composition

The UNIX philosophy shines when you chain small tools:

```
zcat reads.fastq.gz | head -n 400 | grep "^@" | wc -l
cut -f1,3 counts.tsv | sort | uniq -c | sort -nr | head
```

Stdout of one command feeds stdin of the next. Redirect with `>` (overwrite) or `>>` (append); send errors aside with `2>` when needed.

## Columns and quick tabular surgery

```
cut -d',' -f1,4 samples.csv
awk -F'\t' 'NR==1 || $3 > 10' genes.tsv
sort -k2,2nr results.tsv | head
```

`cut` selects fields; `awk` filters and transforms; `sort` orders. For serious tabular work you will still use Python or R, but these one-liners are perfect for smoke tests.

## Permissions, processes, and disk

```
chmod u+x run.sh
df -h
du -sh data/*
top
htop # if installed
kill PID
```

Know when a job is CPU-bound versus waiting on disk. `du` finds which directory ate the quota before someone else's job fails.

## Remote and transfer basics

```
ssh user@cluster
scp local.file user@cluster:/path/
rsync -avP data/ user@cluster:/path/data/
```

`rsync` is usually kinder than `scp` for large directories, it resumes and shows progress.

## Shell hygiene that saves weekends

* Quote variables: `"$file"`, spaces in filenames are common.
* Stop on failure in scripts: `set -euo pipefail`.
* Prefer absolute paths in scheduled jobs.
* Keep a short personal cheatsheet of the ten commands you actually use.

## Closing thought

UNIX fluency is a force multiplier for data work. Learn the small set above deeply, composition, compression, inspection, and search, and you will spend less time fighting files and more time analysing them. Everything else can be looked up as needed.
