"""
graficos_estaticos.py
Gráficos estáticos para o relatório — Criminalidade no Ceará
Gera imagens PNG prontas para inserir no relatório ou apresentação

Como rodar:
    pip install psycopg2-binary pandas matplotlib seaborn
    python graficos_estaticos.py

Os arquivos PNG serão salvos na mesma pasta do script.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
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

# Estilo visual
sns.set_theme(style="darkgrid", palette="muted")
plt.rcParams["figure.dpi"] = 150
plt.rcParams["font.family"] = "sans-serif"
AZUL  = "#2563EB"
VERDE = "#16A34A"
VERM  = "#DC2626"

def conectar():
    return psycopg2.connect(**DB_CONFIG)

def salvar(fig, nome):
    fig.savefig(nome, bbox_inches="tight")
    plt.close(fig)
    print(f"✅ Salvo: {nome}")


# ============================================================
# GRÁFICO 1 — Evolução anual de CVLIs e CVPs
# ============================================================
def grafico_evolucao_anual():
    with conectar() as conn:
        cvli = pd.read_sql("SELECT ano, COUNT(*) AS total FROM cvli GROUP BY ano ORDER BY ano", conn)
        cvp  = pd.read_sql("SELECT ano, COUNT(*) AS total FROM cvp  GROUP BY ano ORDER BY ano", conn)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Evolução Anual de Crimes no Ceará (2021–2023)", fontsize=14, fontweight="bold")

    axes[0].bar(cvli["ano"].astype(str), cvli["total"], color=VERM)
    axes[0].set_title("CVLI — Crimes Violentos Letais")
    axes[0].set_ylabel("Número de casos")
    for i, v in enumerate(cvli["total"]):
        axes[0].text(i, v + 20, str(v), ha="center", fontweight="bold")

    axes[1].bar(cvp["ano"].astype(str), cvp["total"], color=AZUL)
    axes[1].set_title("CVP — Crimes contra o Patrimônio")
    axes[1].set_ylabel("Número de casos")
    for i, v in enumerate(cvp["total"]):
        axes[1].text(i, v + 200, str(v), ha="center", fontweight="bold")

    salvar(fig, "grafico1_evolucao_anual.png")


# ============================================================
# GRÁFICO 2 — Top 10 municípios com mais CVLIs
# ============================================================
def grafico_top_municipios():
    with conectar() as conn:
        df = pd.read_sql("""
            SELECT municipio, COUNT(*) AS total
            FROM cvli
            GROUP BY municipio
            ORDER BY total DESC
            LIMIT 10
        """, conn)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=df, y="municipio", x="total", palette="Reds_r", ax=ax)
    ax.set_title("Top 10 Municípios com Mais CVLIs (2021–2023)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Número de casos")
    ax.set_ylabel("")
    for i, v in enumerate(df["total"]):
        ax.text(v + 5, i, str(v), va="center")

    salvar(fig, "grafico2_top_municipios.png")


# ============================================================
# GRÁFICO 3 — Perfil das vítimas por gênero e raça
# ============================================================
def grafico_perfil_vitimas():
    with conectar() as conn:
        genero = pd.read_sql("""
            SELECT genero, COUNT(*) AS total
            FROM cvli
            GROUP BY genero ORDER BY total DESC
        """, conn)
        raca = pd.read_sql("""
            SELECT raca_vitima, COUNT(*) AS total
            FROM cvli
            GROUP BY raca_vitima ORDER BY total DESC
            LIMIT 6
        """, conn)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Perfil das Vítimas de CVLI (2021–2023)", fontsize=14, fontweight="bold")

    axes[0].pie(genero["total"], labels=genero["genero"],
                autopct="%1.1f%%", colors=["#2563EB","#F59E0B","#9CA3AF"],
                startangle=90, wedgeprops={"edgecolor":"white","linewidth":1.5})
    axes[0].set_title("Por Gênero")

    sns.barplot(data=raca, y="raca_vitima", x="total", palette="Blues_r", ax=axes[1])
    axes[1].set_title("Por Raça/Cor")
    axes[1].set_xlabel("Número de casos")
    axes[1].set_ylabel("")

    salvar(fig, "grafico3_perfil_vitimas.png")


# ============================================================
# GRÁFICO 4 — Sazonalidade mensal (CVLI e CVP)
# ============================================================
def grafico_sazonalidade():
    meses = ["Jan","Fev","Mar","Abr","Mai","Jun",
             "Jul","Ago","Set","Out","Nov","Dez"]

    with conectar() as conn:
        cvli = pd.read_sql("SELECT mes, COUNT(*) AS total FROM cvli GROUP BY mes ORDER BY mes", conn)
        cvp  = pd.read_sql("SELECT mes, COUNT(*) AS total FROM cvp  GROUP BY mes ORDER BY mes", conn)

    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    fig.suptitle("Sazonalidade Mensal de Crimes no Ceará (2021–2023)", fontsize=13, fontweight="bold")

    axes[0].plot(cvli["mes"], cvli["total"], marker="o", color=VERM, linewidth=2)
    axes[0].fill_between(cvli["mes"], cvli["total"], alpha=0.2, color=VERM)
    axes[0].set_title("CVLI")
    axes[0].set_ylabel("Casos")
    axes[0].set_xticks(range(1, 13))
    axes[0].set_xticklabels(meses)

    axes[1].plot(cvp["mes"], cvp["total"], marker="o", color=AZUL, linewidth=2)
    axes[1].fill_between(cvp["mes"], cvp["total"], alpha=0.2, color=AZUL)
    axes[1].set_title("CVP")
    axes[1].set_ylabel("Casos")

    salvar(fig, "grafico4_sazonalidade.png")


# ============================================================
# GRÁFICO 5 — Tipo de natureza dos CVLIs
# ============================================================
def grafico_natureza():
    with conectar() as conn:
        df = pd.read_sql("""
            SELECT natureza, COUNT(*) AS total
            FROM cvli
            GROUP BY natureza ORDER BY total DESC
        """, conn)

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=df, x="natureza", y="total", palette="Oranges_r", ax=ax)
    ax.set_title("Tipos de CVLI no Ceará (2021–2023)", fontsize=13, fontweight="bold")
    ax.set_ylabel("Número de casos")
    ax.set_xlabel("")
    plt.xticks(rotation=20, ha="right")
    for i, v in enumerate(df["total"]):
        ax.text(i, v + 20, str(v), ha="center", fontsize=9)

    salvar(fig, "grafico5_natureza_cvli.png")


# ============================================================
# RODAR TUDO
# ============================================================
if __name__ == "__main__":
    print("🔄 Gerando gráficos...\n")
    grafico_evolucao_anual()
    grafico_top_municipios()
    grafico_perfil_vitimas()
    grafico_sazonalidade()
    grafico_natureza()
    print("\n✅ Todos os gráficos gerados com sucesso!")
    print("📁 Arquivos salvos na pasta atual.")
