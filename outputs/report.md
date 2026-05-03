# Informe estadístico reproducible - Hiperplasia condilar

Servicio de Cirugía Oral y Maxilofacial, Hospital Universitario Miguel Servet.

## Alcance y enfoque

Se analizaron 41 registros del Excel original. La unidad de análisis se considera un registro paciente/intervención. El análisis es descriptivo y comparativo exploratorio por tipo de abordaje quirúrgico; no hay endpoint primario predefinido.

En sencillo: esta salida resume la base y compara abordaje intraoral frente a preauricular, pero no demuestra causalidad.

## Auditoría de datos

- Distribución por abordaje: {'Preauricular': 23, 'Intraoral': 18}.
- Duplicados por `ID Paciente`: 0. Los identificadores se excluyen de outputs públicos.
- Columnas con algún dato ausente/no interpretable: 9.
- Distribución de `Sexo` tras corrección de codificación: {'Mujer': 32, 'Hombre': 9}.
- `Recidiva` contiene 5 valores `?`; no se estima tasa definitiva de recidiva.
- `Oclusión` es constante en esta base y no se contrasta inferencialmente.

En sencillo: hay resultados útiles, pero varias columnas necesitan confirmación de codificación antes de una lectura clínica definitiva.

## Resultados principales por abordaje

- Tiempo Quirúrgico (min): mediana 41.0 en Intraoral frente a 60.0 en Preauricular; diferencia de medianas -19.0 (IC95% -33.0 a -7.5); U de Mann-Whitney, p=<0.001.
  En sencillo: el signo de la diferencia indica si el primer grupo tuvo valores menores o mayores; interprételo con el tamaño muestral y la dispersión.
- Sangrado Postop (ml): mediana 0.0 en Intraoral frente a 10.0 en Preauricular; diferencia de medianas -10.0 (IC95% -10.0 a -5.0); U de Mann-Whitney, p=<0.001.
  En sencillo: el signo de la diferencia indica si el primer grupo tuvo valores menores o mayores; interprételo con el tamaño muestral y la dispersión.
- Dolor Postoperatorio (0–10): mediana 0.0 en Intraoral frente a 3.0 en Preauricular; diferencia de medianas -3.0 (IC95% -4.0 a -1.0); U de Mann-Whitney, p=0.008.
  En sencillo: el signo de la diferencia indica si el primer grupo tuvo valores menores o mayores; interprételo con el tamaño muestral y la dispersión.
- Recuperación Funcional (días): mediana 6.0 en Intraoral frente a 7.0 en Preauricular; diferencia de medianas -1.0 (IC95% -2.0 a 0.0); U de Mann-Whitney, p=0.042.
  En sencillo: el signo de la diferencia indica si el primer grupo tuvo valores menores o mayores; interprételo con el tamaño muestral y la dispersión.
- Lesión Nervio Facial (Sí=1/No=0): eventos 0/18 frente a 9/23; diferencia de riesgos -39.1 puntos porcentuales (IC95% -59.2 a -4.6); Fisher exacta, p=0.002.
  En sencillo: el resultado compara proporciones entre abordajes; con eventos escasos, el intervalo suele ser ancho.
- Sangrado postoperatorio >0 ml: eventos 0/18 frente a 21/23; diferencia de riesgos -91.3 puntos porcentuales (IC95% -97.6 a -55.6); Fisher exacta, p=<0.001.
  En sencillo: el resultado compara proporciones entre abordajes; con eventos escasos, el intervalo suele ser ancho.
- Cicatriz Visible (Sí: 1/No: 0): eventos 0/18 frente a 23/23; diferencia de riesgos -100.0 puntos porcentuales (IC95% -100.0 a -68.1); Fisher exacta, p=<0.001.
  En sencillo: el resultado compara proporciones entre abordajes; con eventos escasos, el intervalo suele ser ancho.
- Resultado Funcional a 6m (Bueno:1 / Malo:0): eventos 18/18 frente a 22/23; diferencia de riesgos 4.3 puntos porcentuales (IC95% -16.8 a 21.0); Fisher exacta, p=1.000.
  En sencillo: el resultado compara proporciones entre abordajes; con eventos escasos, el intervalo suele ser ancho.
- Complicaciones: SI: 1 /NO: 0): eventos 3/18 frente a 10/22; diferencia de riesgos -28.8 puntos porcentuales (IC95% -59.5 a 12.3); Fisher exacta, p=0.090.
  En sencillo: el resultado compara proporciones entre abordajes; con eventos escasos, el intervalo suele ser ancho.
- Necesidad ortognática binaria: eventos 15/18 frente a 17/21; diferencia de riesgos 2.4 puntos porcentuales (IC95% -31.6 a 34.2); Fisher exacta, p=1.000.
  En sencillo: el resultado compara proporciones entre abordajes; con eventos escasos, el intervalo suele ser ancho.

## Variables no contrastadas

- Resultado Estético numérico: No hay exactamente dos grupos con datos analizables.
- Oclusión (Normal: 1/Alterada:0): La variable no tiene dos niveles observados tras excluir perdidos.
- Recidiva binaria: La variable no tiene dos niveles observados tras excluir perdidos.
- TIPO DE COMPLICACIÓN: Categoría RxC muy dispersa; se informa descriptiva por abordaje sin contraste.

## Revisión del DOCX previo

- El DOCX se usa como borrador contextual, no como fuente de verdad; los resultados se recalculan desde el Excel.
- Incluye valores p expresados como 0.000; se deben reportar con precisión razonable, no como cero.
- Incluye fragmentos de código con datos introducidos manualmente; esto dificulta auditoría y reproducibilidad.
- Se apoya mucho en Shapiro-Wilk para decidir normalidad; en muestra pequeña conviene usar resúmenes robustos, gráficos y pruebas no paramétricas justificadas.
- No documenta de forma suficiente los datos ausentes/no interpretables, valores `?`/`no aplica` ni denominadores exactos; la variable `Sexo` se corrige en la base reproducible.
- No reporta de forma sistemática tamaños de efecto ni intervalos de confianza, por lo que puede sobredimensionar conclusiones basadas solo en p-valores.
- La elección de Mann-Whitney para tiempos quirúrgicos es razonable, pero requiere acompañarse de tamaño de efecto e IC.
- Las referencias a t-test deben justificarse con supuestos; por defecto se evita para estos desenlaces pequeños/sesgados.

En sencillo: el documento previo orienta qué preguntas se querían contestar, pero el informe actual recalcula todo desde la base y añade trazabilidad.

## Métodos

- Variables cuantitativas/ordinales: mediana [IQR] y media (DE) cuando ayuda a contextualizar.
- Comparaciones cuantitativas entre dos abordajes: U de Mann-Whitney, correlación rank-biserial y diferencia de medianas con IC95% por bootstrap reproducible.
- Variables binarias: Fisher exacta, diferencia de riesgos con IC95% aproximado Newcombe-Wilson y odds ratio como efecto secundario.
- No se imputa ningún dato perdido. `?`, `no aplica` y textos no numéricos se documentan y se excluyen del análisis correspondiente.

## Limitaciones

- Muestra pequeña, observacional y con múltiples comparaciones exploratorias.
- La codificación de recidiva y tiempo de recidiva requiere aclaración antes de inferencias definitivas.
- Algunas asociaciones son estructurales por el propio abordaje, como cicatriz visible, y no deben leerse como efecto causal aislado.