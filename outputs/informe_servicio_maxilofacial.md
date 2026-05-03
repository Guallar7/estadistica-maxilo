# Informe para presentación de resultados - Estudio de hiperplasia condilar

Servicio de Cirugía Oral y Maxilofacial, Hospital Universitario Miguel Servet.

Preparado para Juan Antonio, residente del Servicio de Cirugía Oral y Maxilofacial.

## Resumen ejecutivo

Se analizaron 41 registros del estudio. La unidad de análisis se considera un registro paciente/intervención. El análisis es descriptivo y comparativo exploratorio por tipo de abordaje quirúrgico: intraoral frente a preauricular.

En sencillo: este documento resume los resultados principales para que Juan Antonio pueda presentarlos al servicio. No debe interpretarse como prueba causal, sino como una descripción comparativa de esta muestra.

## Traducción rápida para presentar

- En esta muestra, el abordaje intraoral se comportó mejor en varias variables de carga postoperatoria: menor tiempo quirúrgico, menor sangrado, menos dolor y recuperación algo más rápida.
- Las diferencias más claras aparecen en sangrado, cicatriz visible y lesión del nervio facial, siempre a favor del grupo intraoral en estos datos.
- El resultado funcional a 6 meses fue bueno en casi todos los casos y no mostró una diferencia relevante entre abordajes.
- Las complicaciones fueron más frecuentes en el grupo preauricular, pero la incertidumbre es amplia y el resultado debe presentarse como tendencia exploratoria.
- Hay que remarcar que la muestra es pequeña y observacional: los resultados orientan, pero no demuestran causalidad.

En una frase: en esta serie, el abordaje intraoral parece asociarse con menor carga quirúrgica y postoperatoria, aunque la interpretación debe ser prudente por el tamaño muestral y la naturaleza retrospectiva del estudio.

## Muestra y calidad de datos

| Indicador | Resultado |
|---|---:|
| Registros analizados | 41 |
| Columnas auditadas | 24 |
| Columnas con algún dato ausente/no interpretable | 9 |
| Valores observados en Sexo | Mujer, Hombre |
| Abordaje Intraoral | 18 |
| Abordaje Preauricular | 23 |

Advertencias de calidad relevantes:

- La variable Sexo se corrigió por error de creación de la base: M/F se unificaron como Mujer y H como Hombre.
- Recidiva contiene valores ?; no se estima una tasa definitiva de recidiva.
- Tiempo Recidiva (meses) contiene valores no numéricos y no es analizable como tiempo hasta recodificar.
- Oclusión es constante en esta base, por lo que no se contrasta inferencialmente.
- Los identificadores de paciente se usaron solo para control interno de duplicados y no se incluyen en este informe.

En sencillo: la base permite responder varias preguntas comparativas, pero algunas columnas necesitan aclaración antes de cerrar conclusiones definitivas.

## Datos del Excel original que conviene revisar

Esta es la revisión de mayor rendimiento antes de repetir o ampliar el análisis. No implica rehacer todo el Excel, sino corregir las columnas que más limitan la interpretación clínica.

| Campo del Excel | Qué revisar | Qué valor aportaría al análisis |
|---|---|---|
| Recidiva (Sí/No) | Sustituir cada ? por Sí, No o Desconocido, usando un criterio clínico único. | Permitirá estimar tasa de recidiva y comparar recidiva por abordaje con denominadores claros. |
| Tiempo Recidiva (meses) | Dejar valores numéricos solo en pacientes con recidiva confirmada; en no recidiva, registrar seguimiento/censura en una columna separada. | Permitirá analizar tiempo hasta recidiva o, al menos, describir seguimiento mínimo de forma interpretable. |
| Oclusión (Normal: 1/Alterada:0) | Confirmar si 0 significa normal, alterada o ausencia de alteración. Ahora la columna es constante y no se puede contrastar. | Evitará una conclusión errónea sobre oclusión y permitirá evaluar si hubo diferencias entre abordajes. |
| Resultado Estético (1-10) | Distinguir no aplica de dato perdido; definir cuándo aplica y quién lo valoró. | Permitirá comparar resultado estético solo en pacientes evaluables y con denominador honesto. |
| Complicaciones: SI: 1 /NO: 0) | Resolver el registro ausente y confirmar que 1/0 significan siempre sí/no. | Mejorará la comparación de seguridad y evitará excluir registros innecesariamente. |
| TIPO DE COMPLICACIÓN | Separar explícitamente sin complicación de dato no registrado y normalizar categorías: parálisis, hematoma, dehiscencia, infección, otras. | Permitirá resumir el perfil de complicaciones por abordaje y no solo la variable binaria. |
| Necesidad de ortognática posteriormente | Resolver valores ? y estandarizar Sí/No. | Permitirá valorar con más precisión la necesidad posterior de cirugía ortognática. |
| Seguimiento | Añadir si es posible fecha de cirugía, fecha de última revisión y meses de seguimiento. | Aportará contexto temporal a recidiva, resultado funcional y complicaciones tardías. |

En sencillo: si el servicio corrige especialmente recidiva, tiempo de recidiva, oclusión y complicaciones, el análisis ganará valor porque podrá responder preguntas clínicas que ahora solo pueden dejarse como pendientes.

## Resultados comparativos principales

| Desenlace | Denominador | Resultado | Efecto (IC95%) | Prueba | p | Lectura sencilla |
|---|---:|---|---|---|---:|---|
| Tiempo Quirúrgico (min) | 18 vs 23 | Mediana 41.0 vs 60.0 | -19.0 (-33.0 a -7.5) | U de Mann-Whitney | <0,001 | El abordaje intraoral presentó valores menores si el efecto es negativo. |
| Sangrado Postop (ml) | 18 vs 23 | Mediana 0.0 vs 10.0 | -10.0 (-10.0 a -5.0) | U de Mann-Whitney | <0,001 | El abordaje intraoral presentó valores menores si el efecto es negativo. |
| Dolor Postoperatorio (0–10) | 18 vs 23 | Mediana 0.0 vs 3.0 | -3.0 (-4.0 a -1.0) | U de Mann-Whitney | 0,008 | El abordaje intraoral presentó valores menores si el efecto es negativo. |
| Recuperación Funcional (días) | 18 vs 22 | Mediana 6.0 vs 7.0 | -1.0 (-2.0 a 0.0) | U de Mann-Whitney | 0,042 | El abordaje intraoral presentó valores menores si el efecto es negativo. |
| Lesión Nervio Facial (Sí=1/No=0) | 18 vs 23 | Eventos 0/18 vs 9/23 | -39,1 pp (-59,2 a -4,6 pp) | Fisher exacta | 0,002 | Compara proporciones; los intervalos pueden ser amplios por eventos escasos. |
| Sangrado postoperatorio >0 ml | 18 vs 23 | Eventos 0/18 vs 21/23 | -91,3 pp (-97,6 a -55,6 pp) | Fisher exacta | <0,001 | Compara proporciones; los intervalos pueden ser amplios por eventos escasos. |
| Cicatriz Visible (Sí: 1/No: 0) | 18 vs 23 | Eventos 0/18 vs 23/23 | -100,0 pp (-100,0 a -68,1 pp) | Fisher exacta | <0,001 | Compara proporciones; los intervalos pueden ser amplios por eventos escasos. |
| Resultado Funcional a 6m (Bueno:1 / Malo:0) | 18 vs 23 | Eventos 18/18 vs 22/23 | 4,3 pp (-16,8 a 21,0 pp) | Fisher exacta | 1,000 | Compara proporciones; los intervalos pueden ser amplios por eventos escasos. |
| Complicaciones: SI: 1 /NO: 0) | 18 vs 22 | Eventos 3/18 vs 10/22 | -28,8 pp (-59,5 a 12,3 pp) | Fisher exacta | 0,090 | Compara proporciones; los intervalos pueden ser amplios por eventos escasos. |
| Necesidad ortognática binaria | 18 vs 21 | Eventos 15/18 vs 17/21 | 2,4 pp (-31,6 a 34,2 pp) | Fisher exacta | 1,000 | Compara proporciones; los intervalos pueden ser amplios por eventos escasos. |

## Variables no contrastadas

- **Resultado Estético numérico**: No hay exactamente dos grupos con datos analizables.
- **Oclusión (Normal: 1/Alterada:0)**: La variable no tiene dos niveles observados tras excluir perdidos.
- **Recidiva binaria**: La variable no tiene dos niveles observados tras excluir perdidos.
- **TIPO DE COMPLICACIÓN**: Categoría RxC muy dispersa; se informa descriptiva por abordaje sin contraste.

## Interpretación clínica prudente

En esta muestra, el abordaje intraoral se asoció con menor tiempo quirúrgico, menor sangrado postoperatorio, menor dolor postoperatorio y una recuperación funcional ligeramente más corta que el abordaje preauricular. También se observaron menos lesiones de nervio facial y menos cicatrices visibles en el grupo intraoral.

En sencillo: los datos favorecen al abordaje intraoral en varios resultados de carga quirúrgica y postoperatoria, pero la muestra es pequeña y observacional.

La cicatriz visible debe interpretarse con especial cautela porque está muy ligada a la propia naturaleza del abordaje. No debe presentarse como efecto causal aislado sin contextualizar la técnica quirúrgica.

## Métodos estadísticos

- Variables cuantitativas u ordinales: mediana, IQR, media y desviación estándar como descriptiva.
- Comparaciones cuantitativas entre abordajes: U de Mann-Whitney, correlación rank-biserial y diferencia de medianas con IC95% por bootstrap reproducible.
- Variables binarias: prueba exacta de Fisher, diferencia de riesgos con IC95% aproximado Newcombe-Wilson y odds ratio como efecto secundario.
- No se imputaron datos perdidos. Los valores ? / no aplica y textos no numéricos se documentaron y se excluyeron del análisis correspondiente.

## Limitaciones

- Muestra pequeña y observacional.
- Múltiples comparaciones exploratorias sin endpoint primario predefinido.
- Recidiva y tiempo de recidiva pendientes de aclaración.
- Algunas asociaciones pueden estar condicionadas por la indicación quirúrgica y la selección de abordaje.

## Archivos reproducibles asociados

- `analysis_pipeline.py`
- `outputs/data_quality.csv`
- `outputs/codebook.csv`
- `outputs/descriptive_continuous.csv`
- `outputs/descriptive_categorical.csv`
- `outputs/statistical_results.csv`
