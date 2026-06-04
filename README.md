# 🔍 IAD — Criminalidade no Ceará (SSPDS-CE)

Trabalho Final — Análise de Dados com SQL  
Disciplina: Introdução à Análise de Dados

## 👥 Integrantes

- Flávio Victor
- Henrique Gabriel
- Kaio Vitor
- Paulo Henrique

## 📌 Tema

Análise de ocorrências criminais no estado do Ceará com base nos dados públicos da **Superintendência de Pesquisa e Estratégia de Segurança Pública (SUPESP/SSPDS-CE)**.

## 📂 Estrutura do Repositório

```
iad-criminalidade-ce/
├── README.md
├── dados/
│   ├── INSTRUCOES_DOWNLOAD.md        # Como baixar os CSVs
│   ├── cvli_2021/2022/2023.csv       # Crimes Violentos Letais
│   ├── cvp_2021/2022/2023.csv        # Crimes contra o Patrimônio
│   └── intervencao_policial_2021/2022/2023.csv
├── sql/
│   ├── 01_criacao.sql                # Criação das tabelas
│   ├── 02_importacao.sql             # Tutorial de importação via DBeaver
│   ├── 03_tratamento.sql             # Limpeza e transformações
│   └── 04_consultas.sql              # Consultas analíticas finais
├── dashboard/
│   ├── graficos_estaticos.py         # Gráficos PNG com Matplotlib/Seaborn
│   └── dashboard_interativo.py       # Dashboard interativo com Plotly/Dash
├── dump/
│   └── dump_criminalidade_ce.sql     # Dump completo do banco
└── relatorio/
    └── relatorio.md                  # Relatório completo
```

## 🚀 Como Rodar

### Pré-requisitos
- PostgreSQL 14+ (via Docker ou instalação local)
- DBeaver
- Python 3.x com as bibliotecas: `psycopg2-binary`, `pandas`, `plotly`, `dash`, `matplotlib`, `seaborn`

### Passo a passo

**1. Crie o banco de dados no DBeaver:**
- Ative "Show all databases" nas configurações da conexão PostgreSQL
- Clique com botão direito em Databases → Create New Database
- Nome: `criminalidade_ce` | Encoding: `UTF8`

**2. Execute o script de criação das tabelas:**
- Abra `sql/01_criacao.sql` no DBeaver e execute (F5)

**3. Importe os CSVs:**
- Siga o tutorial detalhado em `sql/02_importacao.sql`
- Em resumo: botão direito na tabela → Import Data → CSV → delimitador `;` → mapear colunas → Proceed
- Importe os 9 arquivos CSV na ordem: cvli (3), cvp (3), intervencao_policial (3)

**4. Execute o tratamento e as consultas:**
- Abra e execute `sql/03_tratamento.sql`
- Abra e execute `sql/04_consultas.sql`

**5. Rode o dashboard:**
```bash
pip install psycopg2-binary pandas plotly dash matplotlib seaborn
python dashboard/dashboard_interativo.py
```
Acesse em: http://localhost:8050

## 🗂️ Fonte dos Dados

- **SSPDS-CE / SUPESP:** https://www.sspds.ce.gov.br/estatisticas-2/
- **Período coberto:** 2021–2023
- **Tipos de crime:** CVLI (Crimes Violentos Letais e Intencionais), CVP (Crimes Violentos contra o Patrimônio) e Intervenção Policial
