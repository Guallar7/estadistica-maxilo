from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


OUT = Path("outputs")
DATA = OUT / "clean_public_data.parquet"
APPROACH = "Abordaje"

st.set_page_config(
    page_title="Hiperplasia condilar | Informe clínico",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .block-container {padding-top: 1.4rem; padding-bottom: 2rem;}
    h1, h2, h3 {letter-spacing: 0;}
    div[data-testid="stMetric"] {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 14px 16px;
    }
    div[data-testid="stMetricLabel"] p {font-size: 0.86rem; color: #475569;}
    .clinical-note {
        border-left: 4px solid #0F766E;
        background: #F0FDFA;
        padding: 0.8rem 1rem;
        border-radius: 0 6px 6px 0;
        color: #134E4A;
        margin: 0.6rem 0 1rem 0;
    }
    .warn-note {
        border-left: 4px solid #B45309;
        background: #FFFBEB;
        padding: 0.8rem 1rem;
        border-radius: 0 6px 6px 0;
        color: #78350F;
        margin: 0.6rem 0 1rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner=False)
def load_outputs() -> dict[str, pd.DataFrame | str]:
    if not DATA.exists():
        return {}
    return {
        "df": pd.read_parquet(DATA),
        "quality": pd.read_csv(OUT / "data_quality.csv"),
        "codebook": pd.read_csv(OUT / "codebook.csv"),
        "results": pd.read_csv(OUT / "statistical_results.csv"),
        "desc_cont": pd.read_csv(OUT / "descriptive_continuous.csv"),
        "desc_cat": pd.read_csv(OUT / "descriptive_categorical.csv"),
        "report": (OUT / "report.md").read_text(encoding="utf-8") if (OUT / "report.md").exists() else "",
        "docx_review": (OUT / "docx_review.md").read_text(encoding="utf-8") if (OUT / "docx_review.md").exists() else "",
    }


def metric_value(series: pd.Series | None) -> int:
    if series is None:
        return 0
    return int(pd.to_numeric(series, errors="coerce").fillna(0).sum())


data = load_outputs()

st.title("Hiperplasia condilar")
st.caption("Servicio de Cirugía Oral y Maxilofacial · Hospital Universitario Miguel Servet")

if not data:
    st.error("No encuentro `outputs/clean_public_data.parquet`. Ejecuta primero el pipeline reproducible.")
    st.code(
        '.\\.venv\\Scripts\\python.exe analysis_pipeline.py --data "Base_Estudio_Hiperplasia_Condilar ( registro entero).xlsx" --docx "ANALISIS DE DATOS HIPERPLASIA CONDILO.docx"',
        language="powershell",
    )
    st.stop()

df = data["df"].copy()
quality = data["quality"].copy()
results = data["results"].copy()
desc_cont = data["desc_cont"].copy()
desc_cat = data["desc_cat"].copy()
codebook = data["codebook"].copy()

st.sidebar.header("Filtros")
approaches = sorted(df[APPROACH].dropna().unique().tolist()) if APPROACH in df else []
selected_approach = st.sidebar.multiselect("Abordaje", approaches, default=approaches)

side_col = "Lado Afectado"
side_values = sorted(df[side_col].dropna().unique().tolist()) if side_col in df else []
selected_side = st.sidebar.multiselect("Lado afectado", side_values, default=side_values)

sex_col = "Sexo"
sex_values = sorted(df[sex_col].dropna().unique().tolist()) if sex_col in df else []
selected_sex = st.sidebar.multiselect("Sexo", sex_values, default=sex_values)

view = df.copy()
if selected_approach and APPROACH in view:
    view = view[view[APPROACH].isin(selected_approach)]
if selected_side and side_col in view:
    view = view[view[side_col].isin(selected_side)]
if selected_sex and sex_col in view:
    view = view[view[sex_col].isin(selected_sex)]

st.markdown(
    "<div class='clinical-note'>Análisis descriptivo y comparativo exploratorio. Los identificadores de paciente no se muestran.</div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='warn-note'>La variable Sexo ya está corregida como Mujer/Hombre. Mantener cautela con recidiva y valores `?` antes de usar conclusiones definitivas.</div>",
    unsafe_allow_html=True,
)

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Registros filtrados", len(view))
k2.metric("Abordajes", view[APPROACH].nunique() if APPROACH in view else 0)
k3.metric("Complicaciones", metric_value(view.get("Complicaciones: SI: 1 /NO: 0)")))
k4.metric("Lesión nervio facial", metric_value(view.get("Lesión Nervio Facial (Sí=1/No=0)")))
k5.metric("Columnas con missing", int((quality["missing_n"] > 0).sum()))

tab_summary, tab_quality, tab_desc, tab_compare, tab_docx, tab_methods = st.tabs(
    ["Resumen", "Calidad", "Descriptiva", "Comparaciones", "DOCX previo", "Métodos"]
)

with tab_summary:
    left, right = st.columns([1.2, 1])
    with left:
        numeric_options = [
            c for c in view.columns if pd.api.types.is_numeric_dtype(view[c]) and c not in {"ID Paciente"}
        ]
        default = "Tiempo Quirúrgico (min)" if "Tiempo Quirúrgico (min)" in numeric_options else numeric_options[0]
        selected_y = st.selectbox("Variable cuantitativa", numeric_options, index=numeric_options.index(default))
        fig = px.box(
            view,
            x=APPROACH,
            y=selected_y,
            color=APPROACH,
            points="all",
            template="plotly_white",
            color_discrete_map={"Intraoral": "#2563EB", "Preauricular": "#B45309"},
        )
        fig.update_layout(showlegend=False, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, width="stretch")
    with right:
        cat = st.selectbox(
            "Variable categórica",
            [
                c
                for c in [
                    "Lesión Nervio Facial (Sí=1/No=0)",
                    "Cicatriz Visible (Sí: 1/No: 0)",
                    "Sangrado postoperatorio >0 ml",
                    "Complicaciones: SI: 1 /NO: 0)",
                    "Necesidad ortognática binaria",
                    "TIPO DE COMPLICACIÓN",
                ]
                if c in view.columns
            ],
        )
        plot_df = view.groupby([APPROACH, cat], dropna=False).size().reset_index(name="n")
        plot_df[cat] = plot_df[cat].astype(str)
        fig = px.bar(plot_df, x=APPROACH, y="n", color=cat, barmode="stack", template="plotly_white")
        fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, width="stretch")

with tab_quality:
    st.subheader("Auditoría de variables")
    st.dataframe(quality, width="stretch", hide_index=True)
    missing = quality[quality["missing_n"] > 0].sort_values("missing_pct", ascending=False)
    if not missing.empty:
        fig = px.bar(
            missing,
            x="missing_pct",
            y="column",
            orientation="h",
            template="plotly_white",
            labels={"missing_pct": "% missing", "column": ""},
        )
        fig.update_layout(height=420, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, width="stretch")
    st.subheader("Codebook")
    st.dataframe(codebook, width="stretch", hide_index=True)

with tab_desc:
    st.subheader("Variables cuantitativas")
    st.dataframe(desc_cont, width="stretch", hide_index=True)
    st.subheader("Variables categóricas")
    st.dataframe(desc_cat, width="stretch", hide_index=True)

with tab_compare:
    st.subheader("Contrastes exploratorios por abordaje")
    tested = results[results["analysis_status"] == "Testado"].copy()
    skipped = results[results["analysis_status"] != "Testado"].copy()
    st.dataframe(results, width="stretch", hide_index=True)
    if not tested.empty:
        plot = tested.dropna(subset=["effect_value"]).copy()
        plot["effect_label"] = plot["outcome"].str.slice(0, 52)
        fig = px.scatter(
            plot,
            x="effect_value",
            y="effect_label",
            color="outcome_type",
            hover_data=["test", "p_value", "ci95_low", "ci95_high"],
            template="plotly_white",
        )
        fig.add_vline(x=0, line_dash="dash", line_color="#64748B")
        fig.update_layout(yaxis_title="", xaxis_title="Tamaño de efecto", margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, width="stretch")
    if not skipped.empty:
        st.subheader("No testadas")
        st.dataframe(skipped[["outcome", "analysis_status", "interpretation_note"]], width="stretch", hide_index=True)

with tab_docx:
    st.markdown(data["docx_review"])

with tab_methods:
    st.markdown(data["report"])
