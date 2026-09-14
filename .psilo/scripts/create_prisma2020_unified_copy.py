from pathlib import Path
import shutil
import csv
from datetime import datetime

src_root = Path(r"c:\Users\estef\OneDrive\.psilo")
out_root = src_root / "PRISMA_2020_unified_publication"

# Rebuild clean output
if out_root.exists():
    shutil.rmtree(out_root)
out_root.mkdir(parents=True)

# Section structure inspired by the PRISMA 2020 review process already present in the workspace
sections = [
    "1 Planeación",
    "2 Protocolo",
    "3 Estrategia de búsqueda",
    "4 Búsqueda bibliográfica",
    "5 Selección de estudios",
    "6 Extracción de datos",
    "7 Evaluación de calidad",
    "8 Síntesis",
    "9 Redacción",
    "10 Revisión final",
]

for section in sections:
    (out_root / section).mkdir(parents=True, exist_ok=True)

# Reference and results folders
(out_root / "references" / "zotero").mkdir(parents=True, exist_ok=True)
(out_root / "results" / "tables").mkdir(parents=True, exist_ok=True)
(out_root / "results" / "figures").mkdir(parents=True, exist_ok=True)
(out_root / "results" / "flow").mkdir(parents=True, exist_ok=True)

# File copy helper

def copy_file(file_path: Path, destination: Path):
    if file_path.exists():
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file_path, destination)

# 1 Planeación
planeacion_candidates = [
    src_root / "formulacion de la pregunta pico S.pdf",
    src_root / "PROSPERO ANDY.docx",
    src_root / "PROSPERO DEL PROFE TREJO.pdf",
    src_root / "PROSPERO DEL PROFE TREJO ENG.pdf",
]
for f in planeacion_candidates:
    if f.exists():
        copy_file(f, out_root / "1 Planeación" / f.name)

# 2 Protocolo
protocol_candidates = [
    src_root / "scripts" / "psilocybin-bibliometrics-2026-v1.2.1" / "estefanyackerman-dot-psilocybin-bibliometrics-2026-975fb64" / "README.md",
    src_root / "scripts" / "psilocybin-bibliometrics-2026-v1.2.1" / "estefanyackerman-dot-psilocybin-bibliometrics-2026-975fb64" / "docs" / "search_strategies.md",
    src_root / "scripts" / "psilocybin-bibliometrics-2026-v1.2.1" / "estefanyackerman-dot-psilocybin-bibliometrics-2026-975fb64" / "CITATION.cff",
]
for f in protocol_candidates:
    if f.exists():
        copy_file(f, out_root / "2 Protocolo" / f.name)

# 3 Estrategia de búsqueda
search_candidates = [
    src_root / "scripts" / "psilocybin-bibliometrics-2026-v1.2.1" / "estefanyackerman-dot-psilocybin-bibliometrics-2026-975fb64" / "docs" / "search_strategies.md",
    src_root / "pubmed-15NOT19-set.txt",
    src_root / "WOS search-history (2) MODIFICADO.xlsx",
    src_root / "CUINIBUSQUEDA" / "CUINIBUSQUEDA.ris",
]
for f in search_candidates:
    if f.exists():
        copy_file(f, out_root / "3 Estrategia de búsqueda" / f.name)

# 4 Búsqueda bibliográfica
search_records_candidates = [
    src_root / "cuiniespuerkos.ris",
    src_root / "CUINIBUSQUEDA" / "CUINIBUSQUEDA.ris",
    src_root / "scripts" / "psilocybin-bibliometrics-2026-RAMA-REVISION-SISTEMATICA" / "ris (3).ris",
    src_root / "scripts" / "psilocybin-bibliometrics-2026-RAMA-REVISION-SISTEMATICA" / "savedrecs (3).ris",
    src_root / "scripts" / "psilocybin-bibliometrics-2026-RAMA-REVISION-SISTEMATICA" / "csv-psilocybTi-set.csv",
]
for f in search_records_candidates:
    if f.exists():
        copy_file(f, out_root / "4 Búsqueda bibliográfica" / f.name)

# 5 Selección de estudios
selection_src = src_root / "scripts" / "psilocybin-bibliometrics-2026-RAMA-REVISION-SISTEMATICA" / "r" / "results" / "review"
if selection_src.exists():
    for f in sorted(selection_src.glob("*.csv")):
        copy_file(f, out_root / "5 Selección de estudios" / f.name)

# 6 Extracción de datos
extraction_candidates = [
    src_root / "scripts" / "psilocybin-bibliometrics-2026-v1.2.1" / "estefanyackerman-dot-psilocybin-bibliometrics-2026-975fb64" / "data" / "corpus_unique_tridatabase.csv",
    src_root / "scripts" / "psilocybin-bibliometrics-2026-RAMA-REVISION-SISTEMATICA" / "data" / "corpus_unique_tridatabase.csv",
    src_root / "scripts" / "psilocybin-bibliometrics-2026-RAMA-REVISION-SISTEMATICA" / "data" / "pandas_corpus_report.csv",
    src_root / "scripts" / "psilocybin-bibliometrics-2026-RAMA-REVISION-SISTEMATICA" / "data" / "pandas_year_report.csv",
]
for f in extraction_candidates:
    if f.exists():
        copy_file(f, out_root / "6 Extracción de datos" / f.name)

# 7 Evaluación de calidad
quality_candidates = [
    src_root / "scripts" / "psilocybin-bibliometrics-2026-RAMA-REVISION-SISTEMATICA" / "r" / "results" / "review" / "R1_cobertura_abstract.csv",
    src_root / "scripts" / "psilocybin-bibliometrics-2026-RAMA-REVISION-SISTEMATICA" / "r" / "results" / "review" / "R2_calidad_titulo.csv",
    src_root / "scripts" / "psilocybin-bibliometrics-2026-RAMA-REVISION-SISTEMATICA" / "r" / "results" / "review" / "R3_titulo_normalizado_duplicado_exacto.csv",
    src_root / "scripts" / "psilocybin-bibliometrics-2026-RAMA-REVISION-SISTEMATICA" / "r" / "results" / "review" / "R3b_titulo_normalizado_casi_duplicado.csv",
    src_root / "scripts" / "psilocybin-bibliometrics-2026-RAMA-REVISION-SISTEMATICA" / "r" / "results" / "review" / "R4_discrepancia_titulo_corpus_vs_crudo.csv",
]
for f in quality_candidates:
    if f.exists():
        copy_file(f, out_root / "7 Evaluación de calidad" / f.name)

# 8 Síntesis
synthesis_src = src_root / "scripts" / "psilocybin-bibliometrics-2026-v1.2.1" / "estefanyackerman-dot-psilocybin-bibliometrics-2026-975fb64" / "results" / "tables"
if synthesis_src.exists():
    for f in sorted(synthesis_src.glob("*.csv")):
        copy_file(f, out_root / "8 Síntesis" / f.name)

# 9 Redacción
redaccion_candidates = [
    src_root / "scripts" / "psilocybin-bibliometrics-2026-v1.2.1" / "estefanyackerman-dot-psilocybin-bibliometrics-2026-975fb64" / "README.md",
    src_root / "scripts" / "psilocybin-bibliometrics-2026-v1.2.1" / "estefanyackerman-dot-psilocybin-bibliometrics-2026-975fb64" / "README (1).md",
]
for f in redaccion_candidates:
    if f.exists():
        copy_file(f, out_root / "9 Redacción" / f.name)

# 10 Revisión final
copy_file(src_root / "scripts" / "psilocybin-bibliometrics-2026-v1.2.1" / "estefanyackerman-dot-psilocybin-bibliometrics-2026-975fb64" / "LICENSE", out_root / "10 Revisión final" / "LICENSE")

# Zotero references dotted
zotero_candidates = [src_root / "cuiniespuerkos.ris", src_root / "CUINIBUSQUEDA" / "CUINIBUSQUEDA.ris"]
for f in zotero_candidates:
    if f.exists():
        copy_file(f, out_root / "references" / "zotero" / f.name)

# Placeholder for results in process
(out_root / "results" / "tables" / "PLACEHOLDER_results_in_process.txt").write_text(
    "Resultados en proceso de integración. Se mantienen los resultados bibliométricos y de revisión en preparación según el flujo PRISMA 2020.\n",
    encoding="utf-8",
)

# Top-level readme
(out_root / "README.md").write_text(
    "# PRISMA 2020 unified publication copy\n\n"
    "Esta carpeta es una copia unificada y ordenada del material relacionado con psilocibina, depresión y ansiedad,\n"
    "dando prioridad a las versiones y archivos más recientes del workspace.\n\n"
    "Estructura de revisión: PRISMA 2020, con secciones de Planeación, Protocolo, Búsqueda, Selección,\n"
    "Extracción, Evaluación de calidad, Síntesis, Redacción y Revisión final.\n\n"
    "Se incluyen referencias bibliográficas de entrada en formato RIS conservando la relación con Zotero.\n",
    encoding="utf-8",
)

print(f"Unified publication copy created: {out_root}")
