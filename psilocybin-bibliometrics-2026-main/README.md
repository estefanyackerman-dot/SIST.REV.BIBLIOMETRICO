# Psilocybin for Depressive and Anxiety Disorders (2022-2026): Bibliometric Arm

Hybrid bibliometric analysis and systematic review with meta-analysis of randomized controlled trials. This repository contains the complete bibliometric arm: search documentation, deduplication pipeline, derived corpus, tables and figures.

**Companion protocol:** `docs/Protocol_Psilocybin_Depression_Anxiety_v1.0.docx` (PRISMA-P structure, PRISMA-S search documentation). The meta-analytic arm is registered in PROSPERO (registration number to be inserted upon confirmation).

## Search summary (all searches run 5 September 2026)

| Database | Records | Unique contribution |
|---|---|---|
| Web of Science Core Collection | 277 | 277 |
| Scopus | 1,053 | 1,053 |
| PubMed | 932 | 932 |
| **Unique tri-database corpus** | **3,822 source records** | **2,128** |

Deduplication priority: WoS > Scopus > PubMed, matched first by normalized DOI and then by normalized title. Two retracted articles (DOI 10.1177/02698811241234247 and 10.3389/fnins.2023.1168911) were excluded from the analytical corpus and are declared in Methods.

Full search strategies for every database are in `docs/search_strategies.md` and in the protocol.

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

In the updated tri-database corpus, annual production was 178 documents in 2022,
215 in 2023, 232 in 2024, 340 in 2025 and 280 in 2026. The year 2026 is partial
at the search date. The full dual analysis, including the 2,283-document
all-sources corpus and VOSviewer files, is maintained in
`../results/vosviewer_dual/`.

## Reproducibility

Python 3.12 with pandas and matplotlib for the executed pipeline; R (>= 4.3) with bibliometrix for replication and network analyses. See scripts for details.

## License and citation

Code under MIT license; documents and derived data under CC-BY 4.0. Cite using `CITATION.cff` or the Zenodo DOI of this deposit.
