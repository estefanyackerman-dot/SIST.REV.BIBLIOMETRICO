# Marco teórico

El marco teórico está dividido en archivos para facilitar la revisión,
edición y ensamblaje del manuscrito:

1. `01_fundamentos_conceptuales.md`
2. `02_bases_farmacologicas.md`
3. `03_evidencia_clinica.md`
4. `04_contexto_psicoterapeutico_regulatorio.md`
5. `05_integracion_metodologica.md`
6. `06_antecedentes_historicos.md`
7. `07_legislacion_y_regulacion.md`

Las citas usan la sintaxis de Pandoc (`[@clave]`) y las claves se encuentran
en [`../ref.bib`](../ref.bib). La bibliografía fue consolidada a partir de las
exportaciones RIS de Zotero ubicadas en:

`../../.psilo/PRISMA_2020_unified_publication/references/zotero/`

## Ensamblaje con Pandoc

Desde la carpeta `1 Planeación`, ejecutar:

```powershell
pandoc "Marco teorico\01_fundamentos_conceptuales.md" `
  "Marco teorico\02_bases_farmacologicas.md" `
  "Marco teorico\03_evidencia_clinica.md" `
  "Marco teorico\04_contexto_psicoterapeutico_regulatorio.md" `
  "Marco teorico\05_integracion_metodologica.md" `
  "Marco teorico\06_antecedentes_historicos.md" `
  "Marco teorico\07_legislacion_y_regulacion.md" `
  --from markdown `
  --citeproc `
  --bibliography "ref.bib" `
  --csl "ieee.csl" `
  -o "Marco teorico\marco_teorico.docx"
```

Las referencias deben verificarse en Zotero antes del envío: algunas
exportaciones RIS contienen registros incompletos o duplicados, y el artículo
de 2026 debe considerarse evidencia reciente sujeta a actualización.
