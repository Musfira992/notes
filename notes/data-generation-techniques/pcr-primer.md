---
title: "PCR"
date: 2026-09-06
source: https://www.musfirajamil.com/blog/pcr-primer
---

# PCR

_A clear primer on the polymerase chain reaction: denature, anneal, extend; primer design and annealing temperature; and the failure modes that show up on gels and in qPCR curves._

PCR, the polymerase chain reaction, is the method that taught molecular biology to copy DNA on demand. From genotyping and cloning to library preparation for sequencing, PCR (and its quantitative cousin qPCR) sits underneath an enormous fraction of modern biology and diagnostics. This primer focuses on the core idea, the cycle, and the practical knobs that decide success or failure.

## The central idea

DNA polymerase synthesises a new strand using an existing strand as template. PCR weaponises that reaction by:

* supplying **two primers** that flank the region you want to amplify;
* using heat to **denature** double-stranded DNA each cycle;
* allowing primers to **anneal** at a lower temperature;
* letting a heat-stable polymerase **extend** from those primers;
* repeating the cycle so that, in the ideal exponential phase, product roughly doubles each round.

After 25-35 cycles, even a few starting template molecules can yield enough product to see on a gel, clone, or sequence. That sensitivity is the method's power and its contamination risk.

## Ingredients in conceptual form

A basic reaction mixes template DNA, forward and reverse primers, dNTPs (the nucleotide building blocks), buffer with magnesium, and a thermostable polymerase (Taq and engineered variants are common). Primer design is half the battle: primers should be specific to the target, similar in melting temperature, and free of strong self-complementarity that creates primer-dimers.

Magnesium concentration, annealing temperature, and extension time are the usual tuning parameters. Too-low annealing temperature invites off-target bands; too-high yields no product. Extension time scales with amplicon length and polymerase speed.

## What the thermocycler is doing

Each cycle is a timed temperature programme. Early cycles are precious: if primers mis-prime when template is scarce, those errors get amplified. Hot-start polymerases reduce activity until a high-temperature activation step, cutting down on non-specific products formed during setup.

After amplification, products are often checked by agarose gel electrophoresis (size and purity) or used directly in downstream enzymatic steps. Nested PCR, touchdown PCR, and long-range PCR are variations on the same denature-anneal-extend theme for harder templates.

## qPCR and RT-PCR in one breath

**qPCR** monitors product accumulation each cycle with fluorescence, enabling relative (and, with standards, absolute) quantification. **RT-PCR** starts from RNA: reverse transcriptase makes complementary DNA (cDNA), then PCR amplifies it, the backbone of many gene-expression assays. Neither changes the core logic; they add enzymes and detection chemistry upstream or during cycling.

## Failure modes worth recognising

1. **No band**, bad primers, degraded template, wrong annealing temperature, missing polymerase or Mg²⁺, or inhibitors from extraction.
2. **Extra bands**, non-specific priming; raise annealing temperature, redesign primers, or use hot-start enzyme.
3. **Primer-dimer smear at low molecular weight**, primers preferring each other over template.
4. **Contamination**, amplified product from a previous run seeding new reactions; negative controls are non-negotiable.

## Takeaway

PCR amplifies a chosen DNA interval by cycling denaturation, primer annealing, and polymerase extension. Primer design, annealing temperature, and clean template determine whether you get a crisp specific product or a mess. Understand those levers and you can interpret gels, qPCR curves, and sequencing libraries with far less mystery.
