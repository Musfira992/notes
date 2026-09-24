---
title: "Reading a DNA Sequence"
date: 2026-06-14
source: https://www.musfirajamil.com/primers/reading-a-dna-sequence
---

# Reading a DNA Sequence

DNA is written in an alphabet of just four letters - **A**, **T**, **G**, and
**C** - representing the nucleotides adenine, thymine, guanine, and cytosine.
Everything from a protein's shape to a crop's nitrogen-use efficiency is
ultimately encoded in long strings of these four characters.

*Interactive widget on the live site: `DnaHelix` (example sequence `ATGGCATTACGTGACTTCGGC`). See https://www.musfirajamil.com/primers/reading-a-dna-sequence.*

## The double helix, as text

The two strands of DNA are **complementary**: A always pairs with T, and G
always pairs with C. Given one strand, you can always reconstruct the other -
try editing the sequence below and hover any base to see its partner.

*Interactive widget on the live site: `SequenceViewer` (example sequence `ATGGCATTACGT`). See https://www.musfirajamil.com/primers/reading-a-dna-sequence.*

## Reading frames

Ribosomes read DNA (via messenger RNA) three letters at a time. Each triplet -
a **codon** - specifies an amino acid. `ATG` is special: it's the **start
codon** that signals where translation begins, and `TAA`, `TAG`, `TGA` are
**stop codons**.

Shift the reading frame below and watch how completely the encoded protein
changes - a single-base shift rewrites everything downstream.

*Interactive widget on the live site: `CodonTranslator` (example sequence `ATGGCATTACGTTAA`). See https://www.musfirajamil.com/primers/reading-a-dna-sequence.*

## Sequence composition

Not all sequences are alike. The proportion of G and C bases - the **GC
content** - influences DNA stability and is one of the first things a
bioinformatician checks when characterising a genome.

*Interactive widget on the live site: `BaseComposition` (example sequence `ATGGCATTACGTGACTTCGGCGCTA`). See https://www.musfirajamil.com/primers/reading-a-dna-sequence.*

## What's next

These widgets are plain React components embedded directly in this Markdown
file - no change to the site's architecture. The same approach scales up to
richer tools: a 3D protein-structure viewer (NGL Viewer), a genome-track
browser (igv.js), or interactive phylogenetic trees, all of which can drop
straight into future tutorials.
