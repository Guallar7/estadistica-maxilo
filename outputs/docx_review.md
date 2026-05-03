# Revisión crítica del DOCX previo

Disponible: sí
Párrafos no vacíos: 752
Tablas: 3

## Hallazgos

- El DOCX se usa como borrador contextual, no como fuente de verdad; los resultados se recalculan desde el Excel.
- Incluye valores p expresados como 0.000; se deben reportar con precisión razonable, no como cero.
- Incluye fragmentos de código con datos introducidos manualmente; esto dificulta auditoría y reproducibilidad.
- Se apoya mucho en Shapiro-Wilk para decidir normalidad; en muestra pequeña conviene usar resúmenes robustos, gráficos y pruebas no paramétricas justificadas.
- No documenta de forma suficiente missingness, valores `?`/`no aplica` ni denominadores exactos; la variable `Sexo` se corrige en la base reproducible.
- No reporta de forma sistemática tamaños de efecto ni intervalos de confianza, por lo que puede sobredimensionar conclusiones basadas solo en p-valores.
- La elección de Mann-Whitney para tiempos quirúrgicos es razonable, pero requiere acompañarse de tamaño de efecto e IC.
- Las referencias a t-test deben justificarse con supuestos; por defecto se evita para estos desenlaces pequeños/sesgados.