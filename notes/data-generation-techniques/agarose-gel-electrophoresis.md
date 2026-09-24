---
title: "Agarose Gel Electrophoresis"
date: 2026-09-06
source: https://www.musfirajamil.com/blog/agarose-gel-electrophoresis
---

# Agarose Gel Electrophoresis

_How agarose gels separate DNA and RNA by size, how to read ladders and bands, and why this simple QC step still anchors PCR, digests, and nucleic-acid integrity checks._

Agarose gel electrophoresis is how molecular biologists "see" DNA and RNA fragments. You load samples into a gel, apply a voltage, and watch nucleic acids migrate so that smaller fragments travel farther. Bands illuminated with a DNA-binding dye become a simple, visual size distribution, still one of the most useful QC checks in any cloning or PCR workflow.

## Why molecules move

At neutral pH, DNA and RNA carry a negative charge on their phosphate backbone, so they migrate toward the positive electrode. Agarose forms a porous mesh; larger fragments thread through more slowly. Within the useful range of a given gel percentage, migration distance relates to the logarithm of fragment length for linear DNA, which is why a ladder of known sizes lets you interpolate unknowns.

## Gel percentage and resolution

Lower percentage agarose (for example ~0.7-1%) resolves larger fragments better; higher percentage gels tighten resolution for small PCR products. Very large genomic DNA and very small oligos sit at opposite edges of what a standard slab gel can do well, pulsed-field or polyacrylamide methods take over outside that window.

Buffer systems (TAE or TBE are common) maintain pH and provide ions for current. Voltage is a compromise: higher voltage is faster but can heat the gel and reduce resolution or distort bands.

## Loading, ladders, and dyes

Samples are mixed with loading dye for density (so they sink into wells) and tracking dyes that migrate at characteristic rates. A molecular-weight **ladder** in a neighbouring lane is essential for size estimates. Intercalating or groove-binding stains make bands visible under the appropriate light; modern stains are often safer than older ethidium bromide workflows, but all DNA-binding dyes deserve respect and proper disposal.

RNA gels and denaturing conditions are used when secondary structure would otherwise blur size interpretation, a reminder that "a band on a gel" always depends on the nucleic acid's conformation and the buffer chemistry.

## What you learn from a gel

* **Did PCR work?** A band at the expected size is encouraging; multiple bands suggest non-specificity.
* **Is the digest complete?** Restriction digests should shift plasmid bands to predicted fragment sizes.
* **Is RNA intact?** Distinct ribosomal RNA bands (in eukaryotic total RNA) versus a low-molecular-weight smear tell different stories.
* **Is the prep contaminated with genomic DNA?** High-molecular-weight material in an RNA prep can be a warning.

Gels are qualitative to semi-quantitative. Band brightness scales roughly with mass, but staining saturation and imaging settings make densitometry approximate.

## Practical tips that save afternoons

Include a no-template PCR control and run it on the same gel. Do not overload wells, smiling or smeared bands often mean too much DNA or too much salt. If a band is needed for cloning, minimise UV exposure when excising, because UV damages DNA. Document ladder identity and gel percentage in your notes; a photo without that context is hard to reinterpret months later.

## Takeaway

Agarose gel electrophoresis separates nucleic acids by size in an electric field through a porous gel. With a ladder, appropriate agarose percentage, and sensible staining, it remains the fastest reality check for PCR, digests, and nucleic-acid integrity, a visual bridge between the bench and every dataset that depends on clean amplicons or intact RNA.
