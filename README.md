# Psilocybin for Depressive and Anxiety Disorders (2022–2026): Hybrid Bibliometric Analysis and Systematic Review 

Randomized controlled trials focus on working-age outpatients. This repository documents the progress of the systematic review. The complete bibliometric section—including search documentation, deduplication process, derived corpus, tables, and figures—is available on Zenodo: https://doi.org/10.5281/zenodo.21893380 

CITATION: Aranda-Rosas, A. E., Lozano-Garcia, L. J., Martinez-Robles, S., Gonzalez-Ballesteros, E., & Trejo-Rodriguez, M. A. (2026). Psilocybin for depressive and anxiety disorders (2022–2026): bibliometric arm of a hybrid bibliometric and meta-analytic study (Version v1.00) [Computer software]. Zenodo

**Companion protocol:** `` (PRISMA-P structure, PRISMA-S search documentation). The meta-analysis component is registered in PROSPERO [CRD420261493650] on September 2, 2026, at 00:44 UTC, version 1.2, and the file is available in this same repository. 

## Search summary 

All searches conducted on September 5, 2026, will be updated in two months; a strategy for WOS has also been added. The protocol and the files in this repository include searches for preprints in **medRxiv** and **Europe PMC** .

Duplication prioritization: WOS > Scopus > PubMed; matches are first sought by normalized DOI and then by normalized title. 

Full search strategies for every database are in `` and in the protocol.

## Repository structure

```
data/       corpus_unique_tridatabase.csv  (derived, deduplicated corpus: source, title, year, DOI, document type)
scripts/    01_deduplication_pipeline.py   (executable pipeline actually used)
            02_bibliometrix_replication.R  (replication in R/bibliometrix + VOSviewer export)
results/    tables/  T0-T8 (PRISMA-S flow, annual production, sources, authors, countries, keywords, most cited, document types)
            figures/ F1-F4 (600 dpi TIFF for submission + PNG previews)
docs/       Protocol v1.0 (docx), search_strategies.md
```

## Raw database exports

Raw exports from Web of Science, Scopus and PubMed are not redistributed in this repository because their licenses do not permit public redistribution of full records. They are fully regenerable with the documented strategies and dates, and are available from the corresponding author for verification purposes.

## Key descriptive results

Annual production grew at a compound rate of 27.3 percent (2022 to 2025); 2026 is partial at the search date. Leading countries: USA, United Kingdom, Canada, Australia, Switzerland. The most frequent non-generic author keywords (lsd, ketamine, mdma, psychedelic-assisted therapy, psychotherapy) locate the corpus within the comparative psychedelic therapeutics literature.

## Reproducibility

Python 3.12 with pandas and matplotlib for the executed pipeline; R (>= 4.3) with bibliometrix for replication and network analyses. See scripts for details.

## License and citation

Code under MIT license; documents and derived data under CC-BY 4.0. Cite using `CITATION.cff` or the Zenodo DOI of this deposit.
