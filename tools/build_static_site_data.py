from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
DOCS_DATA = ROOT / "docs" / "data"


def records(name: str) -> list[dict]:
    path = OUT / name
    if not path.exists():
        return []
    df = pd.read_csv(path)
    return json.loads(df.where(pd.notna(df), None).to_json(orient="records", force_ascii=False))


def main() -> None:
    DOCS_DATA.mkdir(parents=True, exist_ok=True)
    service_report_path = OUT / "informe_servicio_maxilofacial.md"
    report_path = service_report_path if service_report_path.exists() else OUT / "report.md"
    payload = {
        "report": report_path.read_text(encoding="utf-8") if report_path.exists() else "",
        "quality": records("data_quality.csv"),
        "codebook": records("codebook.csv"),
        "descriptiveContinuous": records("descriptive_continuous.csv"),
        "descriptiveCategorical": records("descriptive_categorical.csv"),
        "results": records("statistical_results.csv"),
    }
    (DOCS_DATA / "dashboard_data.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(DOCS_DATA / "dashboard_data.json")


if __name__ == "__main__":
    main()
