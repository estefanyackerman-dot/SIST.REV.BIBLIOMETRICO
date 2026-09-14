#!/usr/bin/env python3
"""Deduplicate the supplied Web of Science, Ovid and PubMed exports.

Input files are the exports currently in this project directory:
  savedrecs (3).ris                 Web of Science RIS export
  ris (3).ris                       Ovid RIS export
  abstract-psilocybTi-set (1).txt  PubMed plain-text export replacing the old CSV

Records are kept in source-priority order (Web of Science, Ovid, PubMed).
DOIs are matched first; records without a DOI are matched by normalized title.
The result is written to data/corpus_unique_tridatabase.csv.
"""

from pathlib import Path
import re
import unicodedata

import pandas as pd


ROOT = Path(__file__).resolve().parent
INPUTS = (
    ("WOS", ROOT / "savedrecs (3).ris"),
    ("OVID", ROOT / "ris (3).ris"),
    ("PUBMED", ROOT / "abstract-psilocybTi-set (1).txt"),
)
RETRACTED = {"10.1177/02698811241234247", "10.3389/fnins.2023.1168911"}


def norm_doi(value):
    if pd.isna(value) or not str(value).strip():
        return None
    doi = str(value).strip().lower()
    doi = re.sub(r"^(?:https?://)?(?:dx\.)?doi\.org/", "", doi)
    doi = re.sub(r"^doi:\s*", "", doi)
    return doi.rstrip(" .;") or None


def norm_title(value):
    if pd.isna(value) or not str(value).strip():
        return None
    title = unicodedata.normalize("NFKD", str(value))
    title = title.encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]", "", title) or None


def parse_ris(path, source=None):
    """Parse the fields needed for deduplication from a RIS export.

    The parser keeps title, DOI, year, document type, and abstract. It accepts
    both the Web of Science/WoS style AB field and the Ovid-style N2 field.
    The source tag is passed explicitly by the file caller to keep provenance
    consistent across Ovid, WoS, and PubMed.
    """
    records, current = [], {}
    with path.open(encoding="utf-8-sig", errors="replace") as handle:
        for raw_line in handle:
            line = raw_line.rstrip("\r\n")
            if line == "ER  -":
                if current:
                    current["source"] = source if source else current.get("source")
                    records.append(current)
                current = {}
                continue
            match = re.match(r"^([A-Z0-9]{2})\s+-\s+(.*)$", line)
            if not match:
                continue
            tag, value = match.groups()
            if tag in {"TI", "T1"}:
                current["title"] = value
            elif tag == "DO":
                current["doi"] = value
            elif tag in {"PY", "Y1"}:
                current["year"] = value.split("/", 1)[0]
            elif tag in {"PT", "TY"}:
                current["document_type"] = value
            elif tag == "AB":
                current["abstract"] = value
            elif tag == "N2":
                current["abstract"] = value
    if current:
        current["source"] = source if source else current.get("source")
        records.append(current)
    return pd.DataFrame(records)


def parse_pubmed_text(path, source=None):
    """Parse a PubMed plain-text export that stores citation, DOI, title,
    and an abstract-like summary encoded from the MEDLINE block.

    The supplied file is a plain-text, article-per-record export that starts
    each record with a numeric reference line and a DOI-bearing citation line.
    The parser scans those blocks and recovers the title before the
    `Author information:` marker, plus an abstract field from the clinical
    summary lines (`IMPORTANCE:`, `BACKGROUND:`, `OBJECTIVE:`, etc.) until
    the DOI / PMCID / PMID record metadata appears.
    """
    lines = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
    records = []

    author_line_re = re.compile(
        r"^[A-Z][a-zA-Z-]+\s+[A-Z]{1,4}\(\d+\)(?:,|\.)",
        flags=re.I,
    )

    # Identify every PubMed block by the line that starts with the numbered
    # citation and carries the DOI. All records are separated this way.
    block_starts = [
        idx
        for idx, line in enumerate(lines)
        if re.match(r"^\d+\.\s+.*doi:\s*10\.\S+", line, flags=re.I)
    ]

    for idx, start in enumerate(block_starts):
        end = block_starts[idx + 1] if idx + 1 < len(block_starts) else len(lines)
        block = lines[start:end]
        if not block:
            continue

        header = block[0]
        doi_match = re.search(r"doi:\s*(10\.\S+)", header, flags=re.I)
        if not doi_match:
            continue
        doi = norm_doi(doi_match.group(1))
        if not doi:
            continue

        # publish year is on the same citation line; capture only the first 4 digit year.
        year_match = re.search(r"\b(19|20)\d{2}\b", header)
        year = year_match.group(0) if year_match else None

        # Extract title lines from the block, up to `Author information:` or an
        # author-like line. Title and authors are stored before the author section.
        title_lines = []
        j = 1
        while j < len(block):
            current = block[j].strip()
            if not current:
                j += 1
                continue
            if current.startswith("Author information:"):
                break
            if author_line_re.match(current):
                break
            if current.startswith(("Erratum in", "Comment in")):
                j += 1
                continue
            # Skip the journal citation line repeated as a block header.
            if j == 1:
                j += 1
                continue
            title_lines.append(current)
            j += 1

        title = " ".join(title_lines).strip(" .")
        title = re.sub(r"\s+", " ", title)
        if not title:
            continue

        # Abstract-like summary is encoded by the MEDLINE-like fields that come
        # after the author list. Pull lines from the first known abstract field
        # marker (`IMPORTANCE:`, `BACKGROUND:`, `OBJECTIVE:`, `DESIGN...`, etc.)
        # until the DOI/PMCID/PMID metadata lines that terminate the citation.
        abstract_lines = []
        in_abstract = False
        for line in block:
            stripped = line.strip()
            if not stripped:
                continue
            if re.match(r"^DOI\s*:", stripped, flags=re.I):
                break
            if re.match(r"^PMCID\s*:", stripped, flags=re.I):
                break
            if re.match(r"^PMID\s*:", stripped, flags=re.I):
                break
            if re.match(r"^Conflict of interest statement", stripped, flags=re.I):
                break

            match = re.match(
                r"^(IMPORTANCE|BACKGROUND|OBJECTIVE|DESIGN,\s*SETTING,\s*AND\s*PARTICIPANTS|"
                r"DESIGN|INTERVENTIONS|MAIN\s+OUTCOMES\s+AND\s+MEASURES|METHODS|RESULTS|"
                r"CONCLUSIONS\s+AND\s+RELEVANCE|CONCLUSIONS|TRIAL\s+REGISTRATION|METHOD|"
                r"AIMS|RESULT|STUDY\s+DESIGN|SUMMARY|INTRODUCTION|CASE\s+REPORT|FINDINGS):",
                stripped,
                flags=re.I,
            )
            if match:
                in_abstract = True
                abstract_lines.append(stripped)
                continue

            if in_abstract:
                abstract_lines.append(stripped)

        abstract = " ".join(abstract_lines).strip()
        abstract = re.sub(r"\s+", " ", abstract)
        if not abstract:
            abstract = pd.NA

        records.append(
            {
                "title": title,
                "doi": doi,
                "year": year,
                "document_type": None,
                "abstract": abstract,
            }
        )

    out = pd.DataFrame(records)
    if out.empty:
        raise ValueError(f"No PubMed records could be parsed from {path.name}")
    if source:
        out.insert(0, "source", source)
    return out


def parse_pubmed_csv(path, source=None):
    frame = pd.read_csv(path, dtype=str)
    required = {"Title", "DOI"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"{path.name} is missing columns: {', '.join(sorted(missing))}")
    abstract_col = "Abstract" if "Abstract" in frame.columns else None
    out = pd.DataFrame(
        {
            "title": frame["Title"],
            "doi": frame["DOI"],
            "year": frame.get("Publication Year"),
            "document_type": None,
            "abstract": frame[abstract_col] if abstract_col else pd.NA,
        }
    )
    if source:
        out.insert(0, "source", source)
    return out


def load_source(source, path):
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    if source == "PUBMED":
        if path.suffix.lower() == ".csv":
            return parse_pubmed_csv(path, source)
        return parse_pubmed_text(path, source)
    return parse_ris(path, source)


def main():
    unique_records = []
    seen_dois, seen_titles = set(), set()
    source_counts = []
    total_identified = 0
    total_retracted = 0
    total_duplicates = 0

    for source, path in INPUTS:
        records = load_source(source, path)
        identified = len(records)
        records["doi"] = records["doi"].apply(norm_doi)
        records["title_key"] = records["title"].apply(norm_title)
        retracted = int(records["doi"].isin(RETRACTED).sum())
        records = records[~records["doi"].isin(RETRACTED)]

        keep = []
        for _, record in records.iterrows():
            doi, title = record["doi"], record["title_key"]
            duplicate = (doi and doi in seen_dois) or (title and title in seen_titles)
            if duplicate:
                continue
            keep.append(record)
            if doi:
                seen_dois.add(doi)
            if title:
                seen_titles.add(title)

        unique_count = len(keep)
        source_counts.append(
            {
                "source": source,
                "records_identified": identified,
                "retracted_records_removed": retracted,
                "duplicates_removed": len(records) - unique_count,
                "records_after_deduplication": unique_count,
            }
        )
        total_identified += identified
        total_retracted += retracted
        total_duplicates += len(records) - unique_count
        unique_records.extend(
            {
                "source": source,
                "title": record["title"],
                "year": record.get("year"),
                "doi": record["doi"],
                "document_type": record.get("document_type"),
                "abstract": record.get("abstract"),
            }
            for record in keep
        )

    output = ROOT / "data" / "corpus_unique_tridatabase.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(unique_records).to_csv(output, index=False)

    pd.DataFrame(source_counts).to_csv(
        ROOT / "data" / "prisma_2020_source_counts.csv", index=False
    )
    corpus_frame = pd.DataFrame(unique_records)
    report = (
        corpus_frame.groupby("source", dropna=False)
        .agg(
            records=("title", "size"),
            missing_title=("title", lambda column: int(column.isna().sum())),
            missing_doi=("doi", lambda column: int(column.isna().sum())),
            year_min=("year", "min"),
            year_max=("year", "max"),
        )
        .reset_index()
    )
    report["doi_coverage_percent"] = (
        (1 - report["missing_doi"] / report["records"]) * 100
    ).round(2)
    report["title_coverage_percent"] = (
        (1 - report["missing_title"] / report["records"]) * 100
    ).round(2)
    report.to_csv(ROOT / "data" / "pandas_corpus_report.csv", index=False)

    corpus_frame["year"] = pd.to_numeric(corpus_frame["year"], errors="coerce")
    year_report = (
        corpus_frame.groupby(["year", "source"], dropna=False)
        .size()
        .reset_index(name="records")
        .sort_values(["year", "source"], na_position="last")
    )
    year_report.to_csv(ROOT / "data" / "pandas_year_report.csv", index=False)

    flow = pd.DataFrame(
        [
            {"prisma_stage": "Records identified from databases", "value": total_identified},
            {"prisma_stage": "Duplicate records removed", "value": total_duplicates},
            {"prisma_stage": "Retracted records removed", "value": total_retracted},
            {
                "prisma_stage": "Records screened after deduplication",
                "value": len(unique_records),
            },
            {"prisma_stage": "Records excluded during screening", "value": "NR"},
            {"prisma_stage": "Reports sought for retrieval", "value": "NR"},
            {"prisma_stage": "Reports not retrieved", "value": "NR"},
            {"prisma_stage": "Reports assessed for eligibility", "value": "NR"},
            {"prisma_stage": "Reports excluded with reasons", "value": "NR"},
            {"prisma_stage": "Studies included in review", "value": "NR"},
        ]
    )
    flow.to_csv(ROOT / "data" / "prisma_2020_flow_counts.csv", index=False)

    summary = " | ".join(
        f"{row['source']} unique {row['records_after_deduplication']}"
        for row in source_counts
    )
    print(f"{summary} | Total {len(unique_records)}")


if __name__ == "__main__":
    main()
