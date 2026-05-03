# Entregables definitivos

Fecha de preparación: 2026-05-03.

## Entrega principal para el Servicio de Cirugía Oral y Maxilofacial

Estos son los archivos que deben considerarse definitivos para presentación y revisión interna:

| Archivo/carpeta | Uso |
|---|---|
| `outputs/informe_servicio_maxilofacial.docx` | Informe editable en Word para Juan Antonio y el servicio. |
| `outputs/informe_servicio_maxilofacial.md` | Mismo informe en Markdown, útil para revisión y control de cambios. |
| `outputs/figures_png/` | Carpeta con todas las figuras estadísticas estáticas en PNG. |
| `outputs/statistical_results.csv` | Tabla principal de comparaciones, efectos, IC95% y p-valores. |
| `outputs/descriptive_continuous.csv` | Descriptiva de variables continuas/ordinales global y por abordaje. |
| `outputs/descriptive_categorical.csv` | Descriptiva de variables categóricas global y por abordaje. |
| `outputs/data_quality.csv` | Auditoría de calidad, datos ausentes/no interpretables, valores sospechosos y ejemplos. |
| `outputs/codebook.csv` | Diccionario de variables, codificaciones y transformaciones. |
| `outputs/transformations.json` | Registro reproducible de transformaciones aplicadas. |
| `outputs/report.md` | Informe técnico reproducible con revisión metodológica. |

## Figuras estadísticas en PNG

Carpeta:

- `outputs/figures_png/`

Contenido:

| Figura | Uso |
|---|---|
| `distribucion_por_abordaje.png` | Tamaño muestral por abordaje. |
| `edad_box.png` | Distribución de edad por abordaje. |
| `sexo_bar.png` | Distribución de sexo corregido por abordaje. |
| `lado_afectado_bar.png` | Lado afectado por abordaje. |
| `tiempo_quir_rgico_min_box.png` | Tiempo quirúrgico por abordaje. |
| `sangrado_postop_ml_box.png` | Volumen de sangrado postoperatorio por abordaje. |
| `sangrado_postoperatorio_0_ml_bar.png` | Presencia de sangrado postoperatorio por abordaje. |
| `dolor_postoperatorio_0_10_box.png` | Dolor postoperatorio por abordaje. |
| `recuperaci_n_funcional_d_as_box.png` | Recuperación funcional en días por abordaje. |
| `resultado_est_tico_num_rico_box.png` | Resultado estético numérico por abordaje, cuando aplica. |
| `lesi_n_nervio_facial_s_1_no_0_bar.png` | Lesión de nervio facial por abordaje. |
| `cicatriz_visible_s_1_no_0_bar.png` | Cicatriz visible por abordaje. |
| `resultado_funcional_a_6m_bueno_1_malo_0_bar.png` | Resultado funcional a 6 meses por abordaje. |
| `complicaciones_si_1_no_0_bar.png` | Complicaciones por abordaje. |
| `necesidad_ortogn_tica_binaria_bar.png` | Necesidad posterior de ortognática por abordaje. |
| `forest_tamanos_efecto.png` | Resumen de tamaños de efecto con IC95%. |
| `datos_ausentes_no_interpretables.png` | Columnas con datos ausentes o no interpretables. |

## Web y dashboard

| Archivo/recurso | Uso |
|---|---|
| `app.py` | Dashboard local en Streamlit. |
| `docs/index.html` | Web estática pública. |
| `docs/data/dashboard_data.json` | Datos agregados usados por la web pública. |
| <https://guallar7.github.io/estadistica-maxilo/> | Versión online desplegada. |

## Reproducibilidad

| Archivo | Uso |
|---|---|
| `requirements.txt` | Dependencias Python. |
| `analysis_pipeline.py` | Pipeline principal de lectura, limpieza, análisis y figuras. |
| `tools/build_service_report.py` | Generación del informe Word/Markdown para el servicio. |
| `tools/build_static_site_data.py` | Generación del payload agregado de GitHub Pages. |
| `outputs/analysis_manifest.json` | Manifiesto de salidas generadas por el pipeline. |

## Archivos que no son entrega pública

No se consideran entregables públicos ni deben subirse al repositorio:

- `Base_Estudio_Hiperplasia_Condilar ( registro entero).xlsx`
- `Base_Estudio_Hiperplasia_Condilar ( registro entero).backup_sexo_original.xlsx`
- `ANALISIS DE DATOS HIPERPLASIA CONDILO.docx`
- `.venv/`
- `__pycache__/`
- `outputs/clean_public_data.csv`
- `outputs/clean_public_data.parquet`
- `outputs/docx_extracted_text.txt`
- `outputs/figures/` con figuras interactivas HTML locales

## Nota de interpretación

El análisis es exploratorio y observacional. Los resultados comparan abordaje intraoral frente a preauricular en esta muestra, pero no demuestran causalidad. Recidiva y tiempo de recidiva quedan pendientes de aclaración de codificación.
