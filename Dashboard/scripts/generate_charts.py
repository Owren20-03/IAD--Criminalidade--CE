"""
Gera imagens estáticas dos gráficos para o relatório.
"""

from __future__ import annotations

import sys
from pathlib import Path

import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from config import DB_PATH, DIA_SEMANA_ORDEM  # noqa: E402

IMG_DIR = ROOT / "relatorio" / "imagens"


def save_fig(fig: go.Figure, name: str) -> None:
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    out = IMG_DIR / f"{name}.png"
    try:
        fig.write_image(str(out), width=1200, height=700, scale=2)
        print(f"Salvo: {out}")
    except Exception:
        html_out = IMG_DIR / f"{name}.html"
        fig.write_html(str(html_out))
        print(f"Kaleido indisponível. HTML salvo: {html_out}")


def main() -> None:
    con = duckdb.connect(str(DB_PATH), read_only=True)
    df = con.execute("SELECT * FROM vw_mortes_limpa").df()
    con.close()

    template = dict(
        paper_bgcolor="#1a1d27",
        plot_bgcolor="#1a1d27",
        font=dict(color="#f1f1f1"),
    )

    evol = df.assign(ref=pd.to_datetime(df["data_ocorrencia"]).dt.to_period("M").dt.to_timestamp())
    evol = evol.groupby("ref").size().reset_index(name="total")
    fig1 = px.line(evol, x="ref", y="total", markers=True, title="Evolução mensal de mortes violentas")
    fig1.update_layout(**template)
    save_fig(fig1, "01_evolucao_mensal")

    top = df["municipio"].value_counts().head(10).reset_index()
    top.columns = ["municipio", "total"]
    fig2 = px.bar(top, x="total", y="municipio", orientation="h", title="Top 10 municípios")
    fig2.update_layout(**template)
    save_fig(fig2, "02_top_municipios")

    genero = df["genero"].value_counts().reset_index()
    genero.columns = ["genero", "total"]
    fig3 = px.pie(genero, names="genero", values="total", title="Distribuição por gênero", hole=0.4)
    fig3.update_layout(**template)
    save_fig(fig3, "03_genero")

    heat = df.dropna(subset=["hora_int"]).groupby(["dia_semana", "hora_int"]).size().reset_index(name="total")
    heat["ord"] = heat["dia_semana"].map(DIA_SEMANA_ORDEM)
    heat = heat.sort_values(["ord", "hora_int"])
    pivot = heat.pivot(index="dia_semana", columns="hora_int", values="total").fillna(0)
    ordem = sorted(DIA_SEMANA_ORDEM, key=DIA_SEMANA_ORDEM.get)
    pivot = pivot.reindex([d for d in ordem if d in pivot.index])
    fig4 = px.imshow(pivot, title="Heatmap dia da semana × hora", color_continuous_scale="Reds", aspect="auto")
    fig4.update_layout(**template)
    save_fig(fig4, "04_heatmap_temporal")

    meio = df.groupby(["ano", "meio_empregado"]).size().reset_index(name="total")
    fig5 = px.bar(meio, x="ano", y="total", color="meio_empregado", barmode="stack", title="Meio empregado por ano")
    fig5.update_layout(**template)
    save_fig(fig5, "05_meio_empregado")

    esc = df["escolaridade"].value_counts().head(6).reset_index()
    esc.columns = ["escolaridade", "total"]
    fig6 = px.bar(esc, x="escolaridade", y="total", title="Escolaridade das vítimas (top 6)")
    fig6.update_layout(**template)
    save_fig(fig6, "06_escolaridade")


if __name__ == "__main__":
    main()
