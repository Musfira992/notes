---
title: "Western Blotting"
date: 2026-09-06
source: https://www.musfirajamil.com/blog/western-blotting
---

# Western Blotting

_Western blotting explained warmly and clearly: SDS-PAGE, transfer, antibodies, and detection, plus what semi-quantitative band intensity can and cannot tell you about protein levels._

Western blotting is the workhorse method for asking whether a specific protein is present in a sample, and, semi-quantitatively, whether its level differs between conditions. The name "blot" refers to transferring proteins from a gel onto a membrane, where antibodies can find their target among thousands of other polypeptides.

## The logic of the assay

A typical Western workflow has four conceptual acts:

1. **Separate** proteins by size using SDS-PAGE (see also the SDS-PAGE primer in this series).
2. **Transfer** the separated proteins onto a membrane (usually nitrocellulose or PVDF).
3. **Probe** with a primary antibody that recognises the target, then a labelled secondary antibody.
4. **Detect** the label, historically film with enhanced chemiluminescence, nowadays often digital imagers or fluorescent secondaries.

Specificity comes from the antibody, not from the gel. The gel only sorts by approximate molecular weight so you can check that the band sits near the expected size.

## Transfer and membrane

After electrophoresis, proteins are driven onto the membrane by an electric field (wet, semi-dry, or related transfer systems). The membrane binds proteins non-specifically, creating a replica of the gel pattern. Incomplete transfer of large proteins, over-transfer of small ones, or air bubbles can create missing or patchy bands, another reason loading controls and membrane stains (Ponceau S, for example) are useful sanity checks.

## Blocking, antibodies, and wash discipline

Before antibodies go on, the membrane is **blocked** with a protein solution (milk or BSA are common) so antibodies do not stick everywhere. Primary antibody incubation allows specific binding; washes remove unbound antibody; secondary antibody recognises the primary and carries the detection enzyme or fluorophore.

Most artefacts live in this stage: too much antibody yields background smear; too little yields invisibility; poor washing leaves speckles; wrong secondary species yields nothing. Antibody validation, does it see the right size? Does a knockout or knockdown abolish the band?, is the difference between a pretty picture and a credible result.

## What "semi-quantitative" really means

Westerns are excellent for presence/absence and rough fold changes within a carefully controlled blot. They are weaker as absolute quantitation. Detection chemistries saturate; transfer efficiency varies across the membrane; antibody affinity is nonlinear. Good practice includes:

* a **loading control** (a housekeeping protein or total-protein stain) to normalise lane input;
* avoiding overexposed bands when comparing intensity;
* biological replicates, not just technical reloads of one extract;
* reporting molecular-weight markers and expected sizes.

Phospho-specific antibodies add a further twist: they report a modified subpopulation, so total protein controls for that target matter when interpreting signalling changes.

## Reading blots as a data person

When you inherit densitometry spreadsheets or published figures, ask what was normalised, whether lanes were cropped from the same membrane, and whether the antibody had orthogonal validation. Cropping and contrast adjustments are normal for display but should not invent bands. If you are modelling treatment effects from quantified bands, treat the intensities as assay readouts with clear batch structure (each membrane is a batch).

## Takeaway

Western blotting separates proteins, moves them to a membrane, and uses antibodies to reveal a target band. It is powerful for specific detection and cautious comparison, provided transfer, blocking, antibody choice, and loading controls are taken seriously. Treat band intensity as semi-quantitative evidence, not as a mass-spectrometer substitute.
