from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
from docx import Document
from scipy import stats
from statsmodels.stats.contingency_tables import Table2x2


RAW_COLUMNS = {
    "id": "ID Paciente",
    "age": "Edad",
    "sex": "Sexo",
    "side": "Lado Afectado",
    "approach": "Abordaje",
    "surgery_time": "Tiempo Quirúrgico (min)",
    "facial_nerve": "Lesión Nervio Facial (Sí=1/No=0)",
    "bleeding_ml": "Sangrado Postop (ml)",
    "scar": "Cicatriz Visible (Sí: 1/No: 0)",
    "pain": "Dolor Postoperatorio (0–10)",
    "occlusion": "Oclusión (Normal: 1/Alterada:0)",
    "recovery_days": "Recuperación Funcional (días)",
    "esthetic": "Resultado Estético (1–10)",
    "recurrence": "Recidiva (Sí/No)",
    "recurrence_time": "Tiempo Recidiva (meses)",
    "functional_6m": "Resultado Funcional a 6m (Bueno:1 / Malo:0)",
    "orthognathic_need": "Necesidad de ortognatica posteriormente",
    "complications": "Complicaciones: SI: 1 /NO: 0)",
    "complication_type": "TIPO DE COMPLICACIÓN",
}

DERIVED_COLUMNS = {
    "esthetic_num": "Resultado Estético numérico",
    "recurrence_time_num": "Tiempo Recidiva numérico (meses)",
    "recurrence_bin": "Recidiva binaria",
    "orthognathic_bin": "Necesidad ortognática binaria",
    "bleeding_any": "Sangrado postoperatorio >0 ml",
}

GROUP_ORDER = ["Intraoral", "Preauricular"]
UNKNOWN_TOKENS = {"?", "NO APLICA", "NO APLICABLE", "DESCONOCIDO", "UNKNOWN"}


def normalize_text(value: object) -> object:
    if pd.isna(value):
        return pd.NA
    text = str(value).replace("\u200b", "").strip()
    if not text:
        return pd.NA
    return text


def normalize_yes_no(value: object) -> object:
    text = normalize_text(value)
    if pd.isna(text):
        return pd.NA
    upper = str(text).upper().strip()
    if upper in {"SI", "SÍ", "1", "YES", "Y"}:
        return 1
    if upper in {"NO", "0", "N"}:
        return 0
    if upper in UNKNOWN_TOKENS:
        return pd.NA
    return pd.NA


def normalize_binary_numeric(series: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce")
    return numeric.where(numeric.isin([0, 1])).astype("Float64")


def clean_data(df: pd.DataFrame) -> tuple[pd.DataFrame, list[dict]]:
    clean = df.copy()
    transformations: list[dict] = []

    for col in clean.columns:
        if clean[col].dtype == "object":
            clean[col] = clean[col].map(normalize_text)

    sex_col = RAW_COLUMNS["sex"]
    if sex_col in clean:
        mapping = {
            "M": "Mujer",
            "F": "Mujer",
            "MUJER": "Mujer",
            "FEMENINO": "Mujer",
            "H": "Hombre",
            "HOMBRE": "Hombre",
            "MASCULINO": "Hombre",
        }
        clean[sex_col] = clean[sex_col].map(
            lambda x: mapping.get(str(x).strip().upper(), x) if pd.notna(x) else x
        )
        transformations.append({
            "column": sex_col,
            "transformation": "Recodificación corregida: M/F -> Mujer; H -> Hombre.",
        })

    side_col = RAW_COLUMNS["side"]
    if side_col in clean:
        mapping = {
            "DERECHO": "Derecho",
            "DERECHA": "Derecho",
            "IZQUIERDO": "Izquierdo",
            "IZQUIERDA": "Izquierdo",
        }
        clean[side_col] = clean[side_col].map(
            lambda x: mapping.get(str(x).strip().upper(), x) if pd.notna(x) else x
        )
        transformations.append({
            "column": side_col,
            "transformation": "Normalización conservadora de mayúsculas y variantes Derecho/Izquierdo.",
        })

    approach_col = RAW_COLUMNS["approach"]
    if approach_col in clean:
        clean[approach_col] = clean[approach_col].map(
            lambda x: "Preauricular" if str(x).strip().upper() == "PREAURICULAR" else x
        )
        clean[approach_col] = clean[approach_col].map(
            lambda x: "Intraoral" if str(x).strip().upper() == "INTRAORAL" else x
        )
        transformations.append({
            "column": approach_col,
            "transformation": "Estandarización de etiquetas de abordaje: Intraoral y Preauricular.",
        })

    complication_col = RAW_COLUMNS["complication_type"]
    if complication_col in clean:
        mapping = {
            "PARALISIS": "Parálisis",
            "PARÁLISIS": "Parálisis",
            "HEMATOMA": "Hematoma",
            "DEHISCENCIA": "Dehiscencia",
            "INFECCION": "Infección",
            "INFECCIÓN": "Infección",
        }
        clean[complication_col] = clean[complication_col].map(
            lambda x: mapping.get(str(x).strip().upper(), x) if pd.notna(x) else x
        )
        transformations.append({
            "column": complication_col,
            "transformation": "Normalización de acentos y capitalización de tipos de complicación.",
        })

    for key in ["facial_nerve", "scar", "occlusion", "functional_6m", "complications"]:
        col = RAW_COLUMNS[key]
        if col in clean:
            clean[col] = normalize_binary_numeric(clean[col])
            transformations.append({
                "column": col,
                "transformation": "Conversión a binaria 0/1; otros valores quedan como perdidos.",
            })

    esthetic_col = RAW_COLUMNS["esthetic"]
    if esthetic_col in clean:
        clean[DERIVED_COLUMNS["esthetic_num"]] = pd.to_numeric(
            clean[esthetic_col].replace({"no aplica": np.nan, "No aplica": np.nan, "?": np.nan}),
            errors="coerce",
        )
        transformations.append({
            "column": DERIVED_COLUMNS["esthetic_num"],
            "transformation": "Columna derivada numérica; `no aplica` y `?` se tratan como no analizables.",
        })

    recurrence_time_col = RAW_COLUMNS["recurrence_time"]
    if recurrence_time_col in clean:
        clean[DERIVED_COLUMNS["recurrence_time_num"]] = pd.to_numeric(
            clean[recurrence_time_col].replace({"No": np.nan, "no": np.nan, "?": np.nan}),
            errors="coerce",
        )
        transformations.append({
            "column": DERIVED_COLUMNS["recurrence_time_num"],
            "transformation": "Columna derivada numérica; `No` no se interpreta como meses.",
        })

    recurrence_col = RAW_COLUMNS["recurrence"]
    if recurrence_col in clean:
        clean[DERIVED_COLUMNS["recurrence_bin"]] = clean[recurrence_col].map(normalize_yes_no).astype("Float64")
        transformations.append({
            "column": DERIVED_COLUMNS["recurrence_bin"],
            "transformation": "Recodificación SI/NO a 1/0; `?` queda como desconocido.",
        })

    orthognathic_col = RAW_COLUMNS["orthognathic_need"]
    if orthognathic_col in clean:
        clean[DERIVED_COLUMNS["orthognathic_bin"]] = clean[orthognathic_col].map(normalize_yes_no).astype("Float64")
        transformations.append({
            "column": DERIVED_COLUMNS["orthognathic_bin"],
            "transformation": "Recodificación SI/NO a 1/0; `?` queda como desconocido.",
        })

    bleeding_col = RAW_COLUMNS["bleeding_ml"]
    if bleeding_col in clean:
        bleeding = pd.to_numeric(clean[bleeding_col], errors="coerce")
        clean[DERIVED_COLUMNS["bleeding_any"]] = (bleeding > 0).where(bleeding.notna()).astype("Float64")
        transformations.append({
            "column": DERIVED_COLUMNS["bleeding_any"],
            "transformation": "Indicador derivado de cualquier sangrado postoperatorio (>0 ml).",
        })

    return clean, transformations


def infer_unit(col: str) -> str:
    if "min" in col:
        return "minutos"
    if "ml" in col.lower():
        return "ml"
    if "días" in col or "dias" in col:
        return "días"
    if "0–10" in col or "1–10" in col or "0-10" in col or "1-10" in col:
        return "escala"
    if "Edad" in col:
        return "años"
    if "meses" in col:
        return "meses"
    return ""


def infer_role(col: str, values: pd.Series) -> str:
    if col == RAW_COLUMNS["id"]:
        return "identificador sensible"
    if col in {RAW_COLUMNS["approach"]}:
        return "exposición/grupo principal"
    if pd.api.types.is_numeric_dtype(values):
        nonmissing = values.dropna().unique()
        if set(nonmissing).issubset({0, 1, 0.0, 1.0}):
            return "binaria"
        return "cuantitativa/ordinal"
    return "categórica"


def data_quality(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for col in df.columns:
        values = df[col]
        text_values = values.dropna().astype(str).str.strip()
        suspicious = sorted(
            set(v for v in text_values if v.upper() in UNKNOWN_TOKENS or v.lower() in {"no aplica", "no"})
        )
        rows.append({
            "column": col,
            "inferred_role": infer_role(col, values),
            "unit_or_scale": infer_unit(col),
            "dtype": str(values.dtype),
            "n_rows": int(len(values)),
            "missing_n": int(values.isna().sum()),
            "missing_pct": round(float(values.isna().mean() * 100), 2),
            "unique_n": int(values.nunique(dropna=True)),
            "constant_or_near_constant": bool(values.nunique(dropna=True) <= 1),
            "suspicious_values": "; ".join(suspicious),
            "examples": "" if col == RAW_COLUMNS["id"] else "; ".join(text_values.drop_duplicates().head(8).tolist()),
        })
    return pd.DataFrame(rows)


def codebook(df: pd.DataFrame, transformations: list[dict]) -> pd.DataFrame:
    transform_map = {x["column"]: x["transformation"] for x in transformations}
    rows = []
    for col in df.columns:
        rows.append({
            "column": col,
            "role": infer_role(col, df[col]),
            "unit_or_scale": infer_unit(col),
            "public_output": "no" if col == RAW_COLUMNS["id"] else "yes",
            "coding_or_values": ""
            if col == RAW_COLUMNS["id"]
            else "; ".join(df[col].dropna().astype(str).drop_duplicates().head(12).tolist()),
            "transformation_or_note": transform_map.get(col, ""),
        })
    return pd.DataFrame(rows)


def group_pairs(df: pd.DataFrame, group_col: str) -> list[str]:
    present = [g for g in GROUP_ORDER if g in set(df[group_col].dropna())]
    extra = sorted([g for g in df[group_col].dropna().unique() if g not in present])
    return present + extra


def summarize_continuous(df: pd.DataFrame, columns: list[str], group: str | None = None) -> pd.DataFrame:
    rows = []
    groups = [("Global", df)] if group is None else [(str(k), v) for k, v in df.groupby(group, dropna=False)]
    for group_value, sub in groups:
        for col in columns:
            x = pd.to_numeric(sub[col], errors="coerce").dropna()
            rows.append({
                "group": group_value,
                "variable": col,
                "n": int(x.size),
                "missing_n": int(pd.to_numeric(sub[col], errors="coerce").isna().sum()),
                "mean": round(float(x.mean()), 3) if x.size else np.nan,
                "sd": round(float(x.std(ddof=1)), 3) if x.size > 1 else np.nan,
                "median": round(float(x.median()), 3) if x.size else np.nan,
                "q1": round(float(x.quantile(0.25)), 3) if x.size else np.nan,
                "q3": round(float(x.quantile(0.75)), 3) if x.size else np.nan,
                "min": round(float(x.min()), 3) if x.size else np.nan,
                "max": round(float(x.max()), 3) if x.size else np.nan,
            })
    return pd.DataFrame(rows)


def summarize_categorical(df: pd.DataFrame, columns: list[str], group: str | None = None) -> pd.DataFrame:
    rows = []
    groups = [("Global", df)] if group is None else [(str(k), v) for k, v in df.groupby(group, dropna=False)]
    for group_value, sub in groups:
        total = len(sub)
        for col in columns:
            denom_nonmissing = int(sub[col].notna().sum())
            counts = sub[col].value_counts(dropna=False)
            for level, count in counts.items():
                rows.append({
                    "group": group_value,
                    "variable": col,
                    "level": "Missing" if pd.isna(level) else str(level),
                    "n": int(count),
                    "denominator_records": total,
                    "denominator_nonmissing": denom_nonmissing,
                    "pct_records": round(float(count / total * 100), 2) if total else np.nan,
                    "pct_nonmissing": round(float(count / denom_nonmissing * 100), 2)
                    if denom_nonmissing and pd.notna(level)
                    else np.nan,
                })
    return pd.DataFrame(rows)


def bootstrap_median_diff_ci(x: pd.Series, y: pd.Series, reps: int = 5000) -> tuple[float, float, float]:
    rng = np.random.default_rng(20260503)
    xa = x.to_numpy(dtype=float)
    ya = y.to_numpy(dtype=float)
    observed = float(np.median(xa) - np.median(ya))
    boot = np.empty(reps)
    for i in range(reps):
        boot[i] = np.median(rng.choice(xa, size=len(xa), replace=True)) - np.median(
            rng.choice(ya, size=len(ya), replace=True)
        )
    low, high = np.quantile(boot, [0.025, 0.975])
    return observed, float(low), float(high)


def rank_biserial_from_u(u: float, n1: int, n2: int) -> float:
    return (2 * u / (n1 * n2)) - 1


def compare_continuous(df: pd.DataFrame, group_col: str, outcome: str) -> dict:
    sub = df[[group_col, outcome]].copy()
    sub[outcome] = pd.to_numeric(sub[outcome], errors="coerce")
    sub = sub.dropna()
    levels = group_pairs(sub, group_col)
    if len(levels) != 2:
        return skipped_result(outcome, "No testado", "No hay exactamente dos grupos con datos analizables.")
    x = sub.loc[sub[group_col] == levels[0], outcome]
    y = sub.loc[sub[group_col] == levels[1], outcome]
    if len(x) < 2 or len(y) < 2:
        return skipped_result(outcome, "No testado", "Algún grupo tiene menos de dos observaciones no perdidas.")
    if x.nunique() <= 1 and y.nunique() <= 1 and x.iloc[0] == y.iloc[0]:
        return skipped_result(outcome, "No testado", "Variable constante en los grupos analizables.")
    u, p = stats.mannwhitneyu(x, y, alternative="two-sided", method="auto")
    diff, ci_low, ci_high = bootstrap_median_diff_ci(x, y)
    return {
        "analysis_status": "Testado",
        "outcome": outcome,
        "outcome_type": "cuantitativa/ordinal",
        "comparison": f"{levels[0]} vs {levels[1]}",
        "test": "U de Mann-Whitney",
        "n_group_1": int(len(x)),
        "n_group_2": int(len(y)),
        "median_group_1": round(float(x.median()), 3),
        "median_group_2": round(float(y.median()), 3),
        "effect": "diferencia de medianas (grupo 1 - grupo 2)",
        "effect_value": round(diff, 3),
        "ci95_low": round(ci_low, 3),
        "ci95_high": round(ci_high, 3),
        "secondary_effect": "correlación rank-biserial",
        "secondary_effect_value": round(float(rank_biserial_from_u(u, len(x), len(y))), 3),
        "statistic": round(float(u), 3),
        "p_value": round(float(p), 6),
        "interpretation_note": "Comparación exploratoria; IC por bootstrap con semilla fija.",
    }


def wilson_ci(events: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if n == 0:
        return math.nan, math.nan
    p = events / n
    denom = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    half = z * math.sqrt((p * (1 - p) + z**2 / (4 * n)) / n) / denom
    return max(0.0, center - half), min(1.0, center + half)


def compare_binary(df: pd.DataFrame, group_col: str, outcome: str) -> dict:
    sub = df[[group_col, outcome]].dropna().copy()
    levels = group_pairs(sub, group_col)
    vals = sorted([v for v in sub[outcome].dropna().unique()])
    if len(levels) != 2:
        return skipped_result(outcome, "No testado", "No hay exactamente dos grupos con datos analizables.")
    if len(vals) != 2:
        return skipped_result(outcome, "No testado", "La variable no tiene dos niveles observados tras excluir perdidos.")
    tab = pd.crosstab(sub[group_col], sub[outcome]).reindex(index=levels, columns=[0.0, 1.0], fill_value=0)
    oddsratio, p = stats.fisher_exact(tab.values)
    try:
        table = Table2x2(tab.values.astype(float) + 0.5)
        or_ci_low, or_ci_high = table.oddsratio_confint()
    except Exception:
        or_ci_low, or_ci_high = (math.nan, math.nan)
    n1 = int(tab.loc[levels[0]].sum())
    n2 = int(tab.loc[levels[1]].sum())
    e1 = int(tab.loc[levels[0], 1.0])
    e2 = int(tab.loc[levels[1], 1.0])
    risk1 = e1 / n1 if n1 else math.nan
    risk2 = e2 / n2 if n2 else math.nan
    l1, h1 = wilson_ci(e1, n1)
    l2, h2 = wilson_ci(e2, n2)
    rd = risk1 - risk2
    rd_low = l1 - h2
    rd_high = h1 - l2
    return {
        "analysis_status": "Testado",
        "outcome": outcome,
        "outcome_type": "binaria",
        "comparison": f"{levels[0]} vs {levels[1]}",
        "test": "Fisher exacta",
        "n_group_1": n1,
        "n_group_2": n2,
        "events_group_1": e1,
        "events_group_2": e2,
        "risk_group_1": round(float(risk1), 4),
        "risk_group_2": round(float(risk2), 4),
        "effect": "diferencia de riesgos (grupo 1 - grupo 2)",
        "effect_value": round(float(rd), 4),
        "ci95_low": round(float(rd_low), 4),
        "ci95_high": round(float(rd_high), 4),
        "secondary_effect": "odds ratio",
        "secondary_effect_value": round(float(oddsratio), 4) if np.isfinite(oddsratio) else np.nan,
        "secondary_ci95_low": round(float(or_ci_low), 4) if np.isfinite(or_ci_low) else np.nan,
        "secondary_ci95_high": round(float(or_ci_high), 4) if np.isfinite(or_ci_high) else np.nan,
        "p_value": round(float(p), 6),
        "interpretation_note": "IC de diferencia de riesgos por Newcombe-Wilson aproximado; OR con corrección 0,5 si aplica.",
    }


def skipped_result(outcome: str, status: str, reason: str) -> dict:
    return {
        "analysis_status": status,
        "outcome": outcome,
        "outcome_type": "",
        "comparison": "Intraoral vs Preauricular",
        "test": "",
        "p_value": np.nan,
        "interpretation_note": reason,
    }


def extract_docx_review(docx_path: Path | None, outdir: Path) -> dict:
    if not docx_path or not docx_path.exists():
        review = {
            "available": False,
            "findings": ["No se proporcionó DOCX previo o no se encontró el archivo."],
            "paragraphs_nonempty": 0,
            "tables": 0,
        }
        (outdir / "docx_review.md").write_text(render_docx_review(review), encoding="utf-8")
        return review

    document = Document(docx_path)
    paragraphs = [p.text.replace("\u200b", "").strip() for p in document.paragraphs if p.text.strip()]
    text = "\n\n".join(paragraphs)
    (outdir / "docx_extracted_text.txt").write_text(text, encoding="utf-8")

    findings = [
        "El DOCX se usa como borrador contextual, no como fuente de verdad; los resultados se recalculan desde el Excel.",
        "Incluye valores p expresados como 0.000; se deben reportar con precisión razonable, no como cero.",
        "Incluye fragmentos de código con datos introducidos manualmente; esto dificulta auditoría y reproducibilidad.",
        "Se apoya mucho en Shapiro-Wilk para decidir normalidad; en muestra pequeña conviene usar resúmenes robustos, gráficos y pruebas no paramétricas justificadas.",
        "No documenta de forma suficiente missingness, valores `?`/`no aplica` ni denominadores exactos; la variable `Sexo` se corrige en la base reproducible.",
        "No reporta de forma sistemática tamaños de efecto ni intervalos de confianza, por lo que puede sobredimensionar conclusiones basadas solo en p-valores.",
    ]
    if "ID Paciente" in text:
        findings.append("El borrador menciona o conserva identificadores; los outputs públicos deben excluir `ID Paciente`.")
    if "Mann-Whitney" in text:
        findings.append("La elección de Mann-Whitney para tiempos quirúrgicos es razonable, pero requiere acompañarse de tamaño de efecto e IC.")
    if "T-test" in text or "t-test" in text:
        findings.append("Las referencias a t-test deben justificarse con supuestos; por defecto se evita para estos desenlaces pequeños/sesgados.")

    review = {
        "available": True,
        "source": str(docx_path),
        "paragraphs_nonempty": len(paragraphs),
        "tables": len(document.tables),
        "key_terms": {
            "shapiro_mentions": len(re.findall(r"shapiro", text, flags=re.I)),
            "mann_whitney_mentions": len(re.findall(r"mann[\s-]?whitney", text, flags=re.I)),
            "p_zero_mentions": len(re.findall(r"p[:=\s]+0\.000|valor p[:=\s]+0\.000", text, flags=re.I)),
            "confidence_interval_mentions": len(re.findall(r"intervalo de confianza|IC 95", text, flags=re.I)),
        },
        "findings": findings,
    }
    (outdir / "docx_review.json").write_text(json.dumps(review, ensure_ascii=False, indent=2), encoding="utf-8")
    (outdir / "docx_review.md").write_text(render_docx_review(review), encoding="utf-8")
    return review


def render_docx_review(review: dict) -> str:
    lines = [
        "# Revisión crítica del DOCX previo",
        "",
        f"Disponible: {'sí' if review.get('available') else 'no'}",
        f"Párrafos no vacíos: {review.get('paragraphs_nonempty', 0)}",
        f"Tablas: {review.get('tables', 0)}",
        "",
        "## Hallazgos",
        "",
    ]
    lines.extend(f"- {finding}" for finding in review.get("findings", []))
    return "\n".join(lines)


def create_figures(outdir: Path, df_public: pd.DataFrame) -> None:
    figures = outdir / "figures"
    figures.mkdir(exist_ok=True)
    approach = RAW_COLUMNS["approach"]
    palette = {"Intraoral": "#2563EB", "Preauricular": "#B45309"}

    continuous = [
        RAW_COLUMNS["surgery_time"],
        RAW_COLUMNS["bleeding_ml"],
        RAW_COLUMNS["pain"],
        RAW_COLUMNS["recovery_days"],
        DERIVED_COLUMNS["esthetic_num"],
    ]
    for col in [c for c in continuous if c in df_public.columns]:
        fig = px.box(
            df_public,
            x=approach,
            y=col,
            color=approach,
            points="all",
            color_discrete_map=palette,
            template="plotly_white",
            labels={approach: "Abordaje"},
            title=f"{col} por abordaje",
        )
        fig.update_layout(showlegend=False, margin=dict(l=40, r=20, t=60, b=40))
        fig.write_html(figures / f"{safe_name(col)}_box.html", include_plotlyjs="cdn")

    categorical = [
        RAW_COLUMNS["facial_nerve"],
        RAW_COLUMNS["scar"],
        DERIVED_COLUMNS["bleeding_any"],
        RAW_COLUMNS["functional_6m"],
        RAW_COLUMNS["complications"],
        DERIVED_COLUMNS["orthognathic_bin"],
    ]
    for col in [c for c in categorical if c in df_public.columns]:
        plot_df = (
            df_public.groupby([approach, col], dropna=False)
            .size()
            .reset_index(name="n")
            .assign(level=lambda x: x[col].astype(str))
        )
        fig = px.bar(
            plot_df,
            x=approach,
            y="n",
            color="level",
            barmode="stack",
            template="plotly_white",
            title=f"{col} por abordaje",
        )
        fig.update_layout(margin=dict(l=40, r=20, t=60, b=40))
        fig.write_html(figures / f"{safe_name(col)}_bar.html", include_plotlyjs="cdn")


def safe_name(name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_")
    return cleaned[:80].lower()


def fmt_p(value: object) -> str:
    if pd.isna(value):
        return "no aplicable"
    value = float(value)
    if value < 0.001:
        return "<0.001"
    return f"{value:.3f}"


def fmt_num(value: object, digits: int = 1) -> str:
    if pd.isna(value):
        return "NA"
    return f"{float(value):.{digits}f}"


def write_report(
    outdir: Path,
    df: pd.DataFrame,
    df_public: pd.DataFrame,
    results: pd.DataFrame,
    quality: pd.DataFrame,
    docx_review: dict,
) -> None:
    n = len(df)
    approach_col = RAW_COLUMNS["approach"]
    counts = df[approach_col].value_counts(dropna=False).to_dict()
    duplicate_ids = int(df[RAW_COLUMNS["id"]].duplicated().sum()) if RAW_COLUMNS["id"] in df else 0
    sex_counts = df[RAW_COLUMNS["sex"]].value_counts(dropna=False).to_dict()
    unknown_recurrence = int((df[RAW_COLUMNS["recurrence"]].astype(str).str.strip() == "?").sum())
    missing_cols = int((quality["missing_n"] > 0).sum())

    lines = [
        "# Informe estadístico reproducible - Hiperplasia condilar",
        "",
        "Servicio de Cirugía Oral y Maxilofacial, Hospital Universitario Miguel Servet.",
        "",
        "## Alcance y enfoque",
        "",
        (
            f"Se analizaron {n} registros del Excel original. La unidad de análisis se considera un registro "
            "paciente/intervención. El análisis es descriptivo y comparativo exploratorio por tipo de abordaje "
            "quirúrgico; no hay endpoint primario predefinido."
        ),
        "",
        "En sencillo: esta salida resume la base y compara abordaje intraoral frente a preauricular, pero no demuestra causalidad.",
        "",
        "## Auditoría de datos",
        "",
        f"- Distribución por abordaje: {counts}.",
        f"- Duplicados por `ID Paciente`: {duplicate_ids}. Los identificadores se excluyen de outputs públicos.",
        f"- Columnas con algún dato ausente/no interpretable: {missing_cols}.",
        f"- Distribución de `Sexo` tras corrección de codificación: {sex_counts}.",
        f"- `Recidiva` contiene {unknown_recurrence} valores `?`; no se estima tasa definitiva de recidiva.",
        "- `Oclusión` es constante en esta base y no se contrasta inferencialmente.",
        "",
        "En sencillo: hay resultados útiles, pero varias columnas necesitan confirmación de codificación antes de una lectura clínica definitiva.",
        "",
        "## Resultados principales por abordaje",
        "",
    ]

    tested = results[results["analysis_status"] == "Testado"].copy() if not results.empty else pd.DataFrame()
    if tested.empty:
        lines.append("No se generaron contrastes inferenciales válidos con las reglas predefinidas.")
    else:
        for _, row in tested.iterrows():
            if row["outcome_type"] == "cuantitativa/ordinal":
                lines.append(
                    (
                        f"- {row['outcome']}: mediana {row['median_group_1']} en {row['comparison'].split(' vs ')[0]} "
                        f"frente a {row['median_group_2']} en {row['comparison'].split(' vs ')[1]}; "
                        f"diferencia de medianas {fmt_num(row['effect_value'])} "
                        f"(IC95% {fmt_num(row['ci95_low'])} a {fmt_num(row['ci95_high'])}); "
                        f"{row['test']}, p={fmt_p(row['p_value'])}."
                    )
                )
                lines.append(
                    "  En sencillo: el signo de la diferencia indica si el primer grupo tuvo valores menores o mayores; interprételo con el tamaño muestral y la dispersión."
                )
            elif row["outcome_type"] == "binaria":
                lines.append(
                    (
                        f"- {row['outcome']}: eventos {int(row['events_group_1'])}/{int(row['n_group_1'])} "
                        f"frente a {int(row['events_group_2'])}/{int(row['n_group_2'])}; "
                        f"diferencia de riesgos {fmt_num(100 * row['effect_value'], 1)} puntos porcentuales "
                        f"(IC95% {fmt_num(100 * row['ci95_low'], 1)} a {fmt_num(100 * row['ci95_high'], 1)}); "
                        f"{row['test']}, p={fmt_p(row['p_value'])}."
                    )
                )
                lines.append(
                    "  En sencillo: el resultado compara proporciones entre abordajes; con eventos escasos, el intervalo suele ser ancho."
                )

    skipped = results[results["analysis_status"] != "Testado"].copy() if not results.empty else pd.DataFrame()
    if not skipped.empty:
        lines.extend(["", "## Variables no contrastadas", ""])
        for _, row in skipped.iterrows():
            lines.append(f"- {row['outcome']}: {row['interpretation_note']}")

    lines.extend([
        "",
        "## Revisión del DOCX previo",
        "",
    ])
    lines.extend(f"- {finding}" for finding in docx_review.get("findings", []))
    lines.extend([
        "",
        "En sencillo: el documento previo orienta qué preguntas se querían contestar, pero el informe actual recalcula todo desde la base y añade trazabilidad.",
        "",
        "## Métodos",
        "",
        "- Variables cuantitativas/ordinales: mediana [IQR] y media (DE) cuando ayuda a contextualizar.",
        "- Comparaciones cuantitativas entre dos abordajes: U de Mann-Whitney, correlación rank-biserial y diferencia de medianas con IC95% por bootstrap reproducible.",
        "- Variables binarias: Fisher exacta, diferencia de riesgos con IC95% aproximado Newcombe-Wilson y odds ratio como efecto secundario.",
        "- No se imputa ningún dato perdido. `?`, `no aplica` y textos no numéricos se documentan y se excluyen del análisis correspondiente.",
        "",
        "## Limitaciones",
        "",
        "- Muestra pequeña, observacional y con múltiples comparaciones exploratorias.",
        "- La codificación de recidiva y tiempo de recidiva requiere aclaración antes de inferencias definitivas.",
        "- Algunas asociaciones son estructurales por el propio abordaje, como cicatriz visible, y no deben leerse como efecto causal aislado.",
    ])
    (outdir / "report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, help="Ruta del Excel/CSV original")
    parser.add_argument("--docx", default=None, help="Ruta opcional del DOCX de análisis previo")
    parser.add_argument("--outdir", default="outputs", help="Directorio de salidas")
    args = parser.parse_args()

    data_path = Path(args.data)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    raw = pd.read_excel(data_path) if data_path.suffix.lower() in {".xlsx", ".xls"} else pd.read_csv(data_path)
    clean, transformations = clean_data(raw)
    clean_public = clean.drop(columns=[RAW_COLUMNS["id"]], errors="ignore")
    clean_public.to_csv(outdir / "clean_public_data.csv", index=False)
    clean_public.to_parquet(outdir / "clean_public_data.parquet", index=False)

    quality = data_quality(clean)
    quality.to_csv(outdir / "data_quality.csv", index=False)
    cb = codebook(clean, transformations)
    cb.to_csv(outdir / "codebook.csv", index=False)
    (outdir / "transformations.json").write_text(json.dumps(transformations, ensure_ascii=False, indent=2), encoding="utf-8")

    continuous = [
        RAW_COLUMNS["age"],
        RAW_COLUMNS["surgery_time"],
        RAW_COLUMNS["bleeding_ml"],
        RAW_COLUMNS["pain"],
        RAW_COLUMNS["recovery_days"],
        DERIVED_COLUMNS["esthetic_num"],
    ]
    continuous = [c for c in continuous if c in clean]
    categorical = [
        RAW_COLUMNS["sex"],
        RAW_COLUMNS["side"],
        RAW_COLUMNS["approach"],
        RAW_COLUMNS["facial_nerve"],
        RAW_COLUMNS["scar"],
        RAW_COLUMNS["occlusion"],
        RAW_COLUMNS["recurrence"],
        RAW_COLUMNS["functional_6m"],
        RAW_COLUMNS["orthognathic_need"],
        RAW_COLUMNS["complications"],
        RAW_COLUMNS["complication_type"],
        DERIVED_COLUMNS["recurrence_bin"],
        DERIVED_COLUMNS["orthognathic_bin"],
        DERIVED_COLUMNS["bleeding_any"],
    ]
    categorical = [c for c in categorical if c in clean_public]

    group_col = RAW_COLUMNS["approach"]
    desc_cont = pd.concat(
        [summarize_continuous(clean, continuous), summarize_continuous(clean, continuous, group=group_col)],
        ignore_index=True,
    )
    desc_cat = pd.concat(
        [summarize_categorical(clean_public, categorical), summarize_categorical(clean_public, categorical, group=group_col)],
        ignore_index=True,
    )
    desc_cont.to_csv(outdir / "descriptive_continuous.csv", index=False)
    desc_cat.to_csv(outdir / "descriptive_categorical.csv", index=False)

    results = []
    for outcome in [
        RAW_COLUMNS["surgery_time"],
        RAW_COLUMNS["bleeding_ml"],
        RAW_COLUMNS["pain"],
        RAW_COLUMNS["recovery_days"],
        DERIVED_COLUMNS["esthetic_num"],
    ]:
        if outcome in clean:
            results.append(compare_continuous(clean, group_col, outcome))
    for outcome in [
        RAW_COLUMNS["facial_nerve"],
        DERIVED_COLUMNS["bleeding_any"],
        RAW_COLUMNS["scar"],
        RAW_COLUMNS["occlusion"],
        RAW_COLUMNS["functional_6m"],
        RAW_COLUMNS["complications"],
        DERIVED_COLUMNS["orthognathic_bin"],
        DERIVED_COLUMNS["recurrence_bin"],
    ]:
        if outcome in clean:
            results.append(compare_binary(clean, group_col, outcome))
    results.append(skipped_result(RAW_COLUMNS["complication_type"], "Descriptivo", "Categoría RxC muy dispersa; se informa descriptiva por abordaje sin contraste."))
    results_df = pd.DataFrame(results)
    results_df.to_csv(outdir / "statistical_results.csv", index=False)

    docx_review = extract_docx_review(Path(args.docx) if args.docx else None, outdir)
    create_figures(outdir, clean_public)
    write_report(outdir, clean, clean_public, results_df, quality, docx_review)

    manifest = {
        "data_source": str(data_path),
        "docx_source": args.docx,
        "n_rows": int(len(clean)),
        "n_columns_raw": int(raw.shape[1]),
        "outputs": sorted([str(p.relative_to(outdir)) for p in outdir.rglob("*") if p.is_file()]),
    }
    (outdir / "analysis_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Analysis complete. Outputs written to: {outdir.resolve()}")


if __name__ == "__main__":
    main()
