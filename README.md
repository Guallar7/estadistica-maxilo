# Hiperplasia condilar - análisis reproducible

Análisis clínico reproducible y dashboard para el estudio de hiperplasia condilar.

## Privacidad

Este repositorio no debe incluir archivos clínicos originales ni identificadores de paciente. El Excel y el DOCX fuente se mantienen fuera de git mediante `.gitignore`. La web desplegada usa solo resultados agregados.

## Ejecución local

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe analysis_pipeline.py --data "Base_Estudio_Hiperplasia_Condilar ( registro entero).xlsx" --docx "ANALISIS DE DATOS HIPERPLASIA CONDILO.docx"
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## Salidas

- `outputs/data_quality.csv`
- `outputs/codebook.csv`
- `outputs/descriptive_continuous.csv`
- `outputs/descriptive_categorical.csv`
- `outputs/statistical_results.csv`
- `outputs/report.md`

## Web estática

La carpeta `docs/` contiene una versión agregada para GitHub Pages. Para regenerar su payload:

```powershell
.\.venv\Scripts\python.exe tools\build_static_site_data.py
```
