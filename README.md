# Hiperplasia condilar - análisis reproducible

Repositorio de análisis clínico reproducible para el estudio de hiperplasia condilar del Servicio de Cirugía Oral y Maxilofacial del Hospital Universitario Miguel Servet.

La web pública está disponible en:

<https://guallar7.github.io/estadistica-maxilo/>

## Qué contiene

Este proyecto incluye:

- Pipeline reproducible de limpieza, auditoría, descriptiva, estadística inferencial exploratoria y generación de resultados.
- Dashboard local en Streamlit.
- Web estática pública con datos agregados para GitHub Pages.
- Informe editable para presentación interna del servicio.
- Figuras estadísticas exportadas en PNG.
- Tablas CSV auditables con calidad de datos, codebook, descriptiva y resultados.

## Privacidad

Los archivos clínicos originales no se publican en GitHub:

- `Base_Estudio_Hiperplasia_Condilar ( registro entero).xlsx`
- `ANALISIS DE DATOS HIPERPLASIA CONDILO.docx`
- copias de seguridad del Excel
- outputs fila a fila o derivados con potencial sensibilidad

La web desplegada usa resultados agregados y no incluye `ID Paciente`.

## Corrección de codificación

La variable `Sexo` fue corregida por error de creación de la base:

- `M` y `F` se unificaron como `Mujer`
- `H` se recodificó como `Hombre`

Conteo final validado: `Mujer = 32`, `Hombre = 9`.

## Archivos definitivos

El inventario completo está en:

- `ENTREGABLES_DEFINITIVOS.md`

Los entregables principales para el servicio son:

- `outputs/informe_servicio_maxilofacial.docx`
- `outputs/informe_servicio_maxilofacial.md`
- `outputs/figures_png/`
- `outputs/statistical_results.csv`
- `outputs/descriptive_continuous.csv`
- `outputs/descriptive_categorical.csv`
- `outputs/data_quality.csv`
- `outputs/codebook.csv`

## Figuras PNG

La carpeta definitiva de figuras estáticas es:

- `outputs/figures_png/`

Incluye boxplots, barras por abordaje, forest plot de tamaños de efecto y gráfico de datos ausentes/no interpretables. Estas figuras se regeneran automáticamente al ejecutar `analysis_pipeline.py`.

## Ejecución local

Crear entorno virtual e instalar dependencias:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Ejecutar el análisis completo:

```powershell
.\.venv\Scripts\python.exe analysis_pipeline.py --data "Base_Estudio_Hiperplasia_Condilar ( registro entero).xlsx" --docx "ANALISIS DE DATOS HIPERPLASIA CONDILO.docx"
.\.venv\Scripts\python.exe tools\build_service_report.py
.\.venv\Scripts\python.exe tools\build_static_site_data.py
```

Arrancar el dashboard local:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## Estructura

- `analysis_pipeline.py`: pipeline principal reproducible.
- `app.py`: dashboard local Streamlit.
- `tools/build_service_report.py`: genera el informe Word y Markdown para el servicio.
- `tools/build_static_site_data.py`: prepara el JSON agregado para la web pública.
- `docs/`: web estática para GitHub Pages.
- `outputs/`: resultados reproducibles locales.
- `outputs/figures_png/`: figuras definitivas en PNG.

## Interpretación

El análisis es descriptivo y comparativo exploratorio. Las comparaciones por abordaje deben leerse como asociaciones observacionales, no como causalidad. Recidiva y tiempo de recidiva permanecen pendientes de aclaración por codificación insuficiente.
