"""
Prepara os datasets para o pipeline SQL.

- Valida e normaliza o CSV em dados/
- Opcionalmente reconverte a partir de dados/Dados_Filtrados_2021_a_2023.xlsx
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import (  # noqa: E402
    COLUMN_MAP,
    DADOS_DIR,
    FILTERED_CSV,
    OPTIONAL_XLSX,
    OUTPUTS_DIR,
    RAW_CSV,
)


def load_filtered_dataframe() -> pd.DataFrame:
    if OPTIONAL_XLSX.exists():
        print(f"Excel encontrado em {OPTIONAL_XLSX}, convertendo...")
        df = pd.read_excel(OPTIONAL_XLSX).rename(columns=COLUMN_MAP)
    elif FILTERED_CSV.exists():
        print(f"Carregando {FILTERED_CSV}...")
        df = pd.read_csv(FILTERED_CSV)
        if "municipio" not in df.columns:
            df = df.rename(columns=COLUMN_MAP)
    else:
        raise FileNotFoundError(
            f"Nenhum dado encontrado. Coloque {FILTERED_CSV.name} em dados/ "
            f"ou {OPTIONAL_XLSX.name} para conversão."
        )

    df = df.reset_index(drop=True)
    df.insert(0, "id", np.arange(1, len(df) + 1, dtype=np.int32))

    df["data_ocorrencia"] = pd.to_datetime(df["data_ocorrencia"], errors="coerce").dt.date
    df["hora_ocorrencia"] = pd.to_datetime(
        df["hora_ocorrencia"].astype(str), format="%H:%M:%S", errors="coerce"
    ).dt.time

    if "idade_vitima_raw" in df.columns:
        idade = pd.to_numeric(df["idade_vitima_raw"], errors="coerce")
        df["idade_vitima"] = idade.where(idade.between(0, 120), np.nan).astype("Int64")
        df = df.drop(columns=["idade_vitima_raw"])
    else:
        df["idade_vitima"] = pd.to_numeric(df["idade_vitima"], errors="coerce").astype("Int64")

    for col in ["municipio", "ais", "natureza", "dia_semana", "meio_empregado", "genero", "escolaridade", "raca"]:
        df[col] = df[col].astype(str).str.strip()

    return df[
        [
            "id", "municipio", "ais", "natureza", "data_ocorrencia", "hora_ocorrencia",
            "dia_semana", "meio_empregado", "genero", "idade_vitima", "escolaridade", "raca",
        ]
    ]


def validate_dataframe(df: pd.DataFrame) -> dict:
    report: dict = {
        "total_registros": int(len(df)),
        "periodo": {
            "inicio": str(df["data_ocorrencia"].min()),
            "fim": str(df["data_ocorrencia"].max()),
        },
        "nulos_por_coluna": {k: int(v) for k, v in df.isnull().sum().items()},
        "municipios_unicos": int(df["municipio"].nunique()),
        "naturezas": df["natureza"].value_counts().to_dict(),
        "anos": df.assign(ano=pd.to_datetime(df["data_ocorrencia"]).dt.year)["ano"].value_counts().sort_index().to_dict(),
        "genero": df["genero"].value_counts().to_dict(),
        "meio_empregado": df["meio_empregado"].value_counts().to_dict(),
        "idade_media": float(df["idade_vitima"].mean(skipna=True)),
        "idade_mediana": float(df["idade_vitima"].median(skipna=True)),
        "idade_nao_informada": int(df["idade_vitima"].isna().sum()),
        "raca_nao_informada_pct": round(
            (df["raca"].eq("Não Informada").sum() / len(df)) * 100, 1
        ),
    }
    invalid_dates = int(df["data_ocorrencia"].isna().sum())
    if invalid_dates:
        report["alertas"] = [f"{invalid_dates} registros com data inválida"]
    return report


def main() -> None:
    DADOS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    if not RAW_CSV.exists():
        print(f"Aviso: CSV bruto não encontrado em {RAW_CSV}")

    df = load_filtered_dataframe()

    print(f"Salvando CSV tratado em {FILTERED_CSV}")
    df.to_csv(FILTERED_CSV, index=False, encoding="utf-8")

    report = validate_dataframe(df)
    report_path = OUTPUTS_DIR / "validacao_dados.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\n=== Validação concluída ===")
    print(f"Registros: {report['total_registros']:,}")
    print(f"Período: {report['periodo']['inicio']} a {report['periodo']['fim']}")
    print(f"Municípios: {report['municipios_unicos']}")
    print(f"Idade média: {report['idade_media']:.1f} anos")
    print(f"Raça não informada: {report['raca_nao_informada_pct']}%")
    print(f"Relatório salvo em {report_path}")


if __name__ == "__main__":
    main()
