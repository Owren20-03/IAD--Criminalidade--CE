"""
dashboard_interativo.py
Dashboard interativo — Criminalidade no Ceará (2021–2023)
Roda no navegador em http://localhost:8050

Como rodar:
    pip install psycopg2-binary pandas plotly dash
    python dashboard_interativo.py

Depois abra o navegador em: http://localhost:8050
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import psycopg2

# ============================================================
# CONFIGURAÇÃO — ajuste se necessário
# ============================================================
DB_CONFIG = {
    "host":     "localhost",
    "port":     5432,
    "dbname":   "criminalidade_ce",
    "user":     "postgres",
    "password": "123",   # ← troque pela sua senha
    "options":  "-c search_path=criminalidade"
}

MESES = {1:"Jan",2:"Fev",3:"Mar",4:"Abr",5:"Mai",6:"Jun",
         7:"Jul",8:"Ago",9:"Set",10:"Out",11:"Nov",12:"Dez"}

# ============================================================
# CARREGAR DADOS DO BANCO
# ============================================================
def carregar_dados():
    with psycopg2.connect(**DB_CONFIG) as conn:
        cvli = pd.read_sql("SELECT * FROM cvli", conn)
        cvp  = pd.read_sql("SELECT ano, mes, municipio, ais FROM cvp", conn)
        ip   = pd.read_sql("SELECT * FROM intervencao_policial", conn)
    cvli["data"] = pd.to_datetime(cvli["data"])
    ip["data"]   = pd.to_datetime(ip["data"])
    return cvli, cvp, ip

print("🔄 Carregando dados do banco...")
cvli, cvp, ip = carregar_dados()
anos = sorted(cvli["ano"].dropna().unique().tolist())
print(f"✅ Dados carregados: {len(cvli)} CVLIs | {len(cvp)} CVPs | {len(ip)} Intervenções")

# ============================================================
# APP DASH
# ============================================================
app = Dash(__name__)
app.title = "Criminalidade no Ceará — IAD"

CORES = {"fundo": "#0F172A", "card": "#1E293B", "texto": "#F1F5F9",
         "azul": "#3B82F6", "vermelho": "#EF4444", "verde": "#22C55E",
         "amarelo": "#F59E0B"}

estilo_card = {
    "backgroundColor": CORES["card"],
    "borderRadius": "12px",
    "padding": "20px",
    "marginBottom": "20px",
    "boxShadow": "0 4px 6px rgba(0,0,0,0.3)"
}

estilo_kpi = {**estilo_card, "textAlign": "center", "flex": "1", "margin": "0 10px"}

app.layout = html.Div(style={"backgroundColor": CORES["fundo"], "minHeight": "100vh",
                              "padding": "30px", "fontFamily": "sans-serif"}, children=[

    # Cabeçalho
    html.Div(style={"textAlign": "center", "marginBottom": "30px"}, children=[
        html.H1("🔍 Criminalidade no Ceará", style={"color": CORES["texto"], "fontSize": "2rem"}),
        html.P("Análise de Dados — SSPDS-CE | 2021–2023",
               style={"color": "#94A3B8", "fontSize": "1rem"}),
    ]),

    # Filtro de ano
    html.Div(style={**estilo_card, "marginBottom": "25px"}, children=[
        html.Label("Filtrar por ano:", style={"color": CORES["texto"], "fontWeight": "bold"}),
        dcc.Checklist(
            id="filtro-ano",
            options=[{"label": f"  {a}", "value": a} for a in anos],
            value=anos,
            inline=True,
            style={"color": CORES["texto"], "marginTop": "10px", "fontSize": "1.1rem"}
        )
    ]),

    # KPIs
    html.Div(style={"display": "flex", "marginBottom": "20px"}, children=[
        html.Div(id="kpi-cvli", style=estilo_kpi),
        html.Div(id="kpi-cvp",  style=estilo_kpi),
        html.Div(id="kpi-ip",   style=estilo_kpi),
    ]),

    # Linha 1: evolução + natureza
    html.Div(style={"display": "flex", "gap": "20px", "marginBottom": "20px"}, children=[
        html.Div(style={**estilo_card, "flex": "1"}, children=[dcc.Graph(id="grafico-evolucao")]),
        html.Div(style={**estilo_card, "flex": "1"}, children=[dcc.Graph(id="grafico-natureza")]),
    ]),

    # Linha 2: top municípios + sazonalidade
    html.Div(style={"display": "flex", "gap": "20px", "marginBottom": "20px"}, children=[
        html.Div(style={**estilo_card, "flex": "1"}, children=[dcc.Graph(id="grafico-municipios")]),
        html.Div(style={**estilo_card, "flex": "1"}, children=[dcc.Graph(id="grafico-sazonalidade")]),
    ]),

    # Linha 3: perfil vítimas
    html.Div(style={"display": "flex", "gap": "20px"}, children=[
        html.Div(style={**estilo_card, "flex": "1"}, children=[dcc.Graph(id="grafico-genero")]),
        html.Div(style={**estilo_card, "flex": "1"}, children=[dcc.Graph(id="grafico-raca")]),
    ]),
])

# ============================================================
# CALLBACKS
# ============================================================
@app.callback(
    Output("kpi-cvli",            "children"),
    Output("kpi-cvp",             "children"),
    Output("kpi-ip",              "children"),
    Output("grafico-evolucao",    "figure"),
    Output("grafico-natureza",    "figure"),
    Output("grafico-municipios",  "figure"),
    Output("grafico-sazonalidade","figure"),
    Output("grafico-genero",      "figure"),
    Output("grafico-raca",        "figure"),
    Input("filtro-ano", "value"),
)
def atualizar(anos_sel):
    c = cvli[cvli["ano"].isin(anos_sel)]
    p = cvp[cvp["ano"].isin(anos_sel)]
    i = ip[ip["ano"].isin(anos_sel)]

    def kpi(label, valor, cor):
        return [
            html.P(label, style={"color": "#94A3B8", "margin": 0, "fontSize": "0.9rem"}),
            html.H2(f"{valor:,}".replace(",", "."), style={"color": cor, "margin": "5px 0", "fontSize": "2rem"}),
            html.P("ocorrências", style={"color": "#64748B", "margin": 0, "fontSize": "0.8rem"}),
        ]

    kpi_cvli = kpi("CVLI", len(c), CORES["vermelho"])
    kpi_cvp  = kpi("CVP",  len(p), CORES["azul"])
    kpi_ip   = kpi("Intervenção Policial", len(i), CORES["amarelo"])

    # Evolução anual
    ev_c = c.groupby("ano").size().reset_index(name="CVLI")
    ev_p = p.groupby("ano").size().reset_index(name="CVP")
    ev = ev_c.merge(ev_p, on="ano", how="outer").fillna(0)
    fig_ev = go.Figure()
    fig_ev.add_bar(x=ev["ano"].astype(str), y=ev["CVLI"], name="CVLI", marker_color=CORES["vermelho"])
    fig_ev.add_bar(x=ev["ano"].astype(str), y=ev["CVP"],  name="CVP",  marker_color=CORES["azul"])
    fig_ev.update_layout(title="Evolução Anual", barmode="group",
                         plot_bgcolor=CORES["card"], paper_bgcolor=CORES["card"],
                         font_color=CORES["texto"], legend_bgcolor=CORES["card"])

    # Natureza
    nat = c.groupby("natureza").size().reset_index(name="total").sort_values("total", ascending=False)
    fig_nat = px.bar(nat, x="natureza", y="total", title="Tipos de CVLI",
                     color="total", color_continuous_scale="Reds")
    fig_nat.update_layout(plot_bgcolor=CORES["card"], paper_bgcolor=CORES["card"],
                          font_color=CORES["texto"], coloraxis_showscale=False,
                          xaxis_tickangle=-20)

    # Top municípios
    mun = c.groupby("municipio").size().reset_index(name="total").sort_values("total", ascending=False).head(10)
    fig_mun = px.bar(mun, x="total", y="municipio", orientation="h",
                     title="Top 10 Municípios — CVLI", color="total",
                     color_continuous_scale="Reds")
    fig_mun.update_layout(plot_bgcolor=CORES["card"], paper_bgcolor=CORES["card"],
                          font_color=CORES["texto"], coloraxis_showscale=False,
                          yaxis={"categoryorder": "total ascending"})

    # Sazonalidade
    saz_c = c.groupby("mes").size().reset_index(name="CVLI")
    saz_p = p.groupby("mes").size().reset_index(name="CVP")
    saz = saz_c.merge(saz_p, on="mes", how="outer").fillna(0).sort_values("mes")
    saz["mes_nome"] = saz["mes"].map(MESES)
    fig_saz = go.Figure()
    fig_saz.add_scatter(x=saz["mes_nome"], y=saz["CVLI"], name="CVLI",
                        mode="lines+markers", line=dict(color=CORES["vermelho"], width=2))
    fig_saz.add_scatter(x=saz["mes_nome"], y=saz["CVP"], name="CVP",
                        mode="lines+markers", line=dict(color=CORES["azul"], width=2))
    fig_saz.update_layout(title="Sazonalidade Mensal",
                          plot_bgcolor=CORES["card"], paper_bgcolor=CORES["card"],
                          font_color=CORES["texto"], legend_bgcolor=CORES["card"])

    # Gênero
    gen = c.groupby("genero").size().reset_index(name="total")
    fig_gen = px.pie(gen, names="genero", values="total", title="Vítimas por Gênero",
                     color_discrete_sequence=px.colors.qualitative.Set2, hole=0.4)
    fig_gen.update_layout(plot_bgcolor=CORES["card"], paper_bgcolor=CORES["card"],
                          font_color=CORES["texto"], legend_bgcolor=CORES["card"])

    # Raça
    raca = c.groupby("raca_vitima").size().reset_index(name="total").sort_values("total", ascending=False).head(6)
    fig_raca = px.bar(raca, x="raca_vitima", y="total", title="Vítimas por Raça/Cor",
                      color="total", color_continuous_scale="Blues")
    fig_raca.update_layout(plot_bgcolor=CORES["card"], paper_bgcolor=CORES["card"],
                           font_color=CORES["texto"], coloraxis_showscale=False,
                           xaxis_tickangle=-15)

    return (kpi_cvli, kpi_cvp, kpi_ip,
            fig_ev, fig_nat, fig_mun, fig_saz, fig_gen, fig_raca)


# ============================================================
if __name__ == "__main__":
    print("\n🚀 Dashboard rodando em: http://localhost:8050")
    print("   Pressione Ctrl+C para parar.\n")
    app.run(debug=False)
