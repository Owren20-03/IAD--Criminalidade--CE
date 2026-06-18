# iad-criminalidade-ce-equipe-flavio

Análise de mortes violentas no Ceará (2021–2023) a partir de dados públicos da SSPDS/CEO.

## Integrantes

- Flávio Victor
- Henrique Gabriel
- Kaio Vitor
- Paulo Henrique

## Tema

**Opção B — Criminalidade no Ceará**

Investigação sobre homicídios dolosos, feminicídios, latrocínios e outras mortes violentas registradas no estado, com foco em padrões temporais, geográficos e perfil das vítimas.

## Stack

| Camada | Ferramenta |
|--------|------------|
| ETL e validação | pandas, numpy |
| SQL analítico | DuckDB (motor SQL embarcado) |
| Dashboard | Plotly Dash |

### Por que DuckDB em vez de PostgreSQL?

O enunciado sugere PostgreSQL, mas o fluxo exigido — **coletar → importar → tratar com SQL → consultar → visualizar** — foi mantido integralmente:

| Exigência do enunciado | Como atendemos |
|------------------------|----------------|
| Scripts `.sql` numerados (01–04) | `sql/01_criacao.sql` … `04_consultas.sql` |
| Criação de tabelas com tipos e chaves | `municipios` + `mortes_violentas` com FK |
| Tratamento e consultas em SQL | Views, CTEs, JOINs, window functions |
| Dump do banco | `dump/criminalidade_ce.duckdb` + `dump/criminalidade_ce.sql` |
| Reprodutibilidade | `python scripts/run_pipeline.py` recria tudo |

**DuckDB** executa SQL ANSI padrão (PostgreSQL-compatible em grande parte) sem servidor externo: ideal para versionar o projeto, rodar em qualquer máquina da equipe e demonstrar na apresentação sem depender de DBeaver/PostgreSQL instalado.

## Estrutura

```
├── dados/          # CSVs originais e tratados (autossuficiente para clonar o repo)
├── sql/            # Scripts SQL (criação, importação, tratamento, consultas)
├── scripts/        # Pipeline Python
├── dashboard/      # Aplicação Plotly Dash
├── dump/           # Banco DuckDB + dump SQL restaurável + CSVs
├── outputs/        # Resultados das consultas analíticas
└── relatorio/      # Relatório em Markdown e PDF
```

## Como rodar

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Preparar os dados

Os CSVs já estão em `dados/`. Para revalidar ou reconverter a partir do Excel da equipe, coloque `Dados_Filtrados_2021_a_2023.xlsx` em `dados/` e execute:

```bash
python scripts/prepare_data.py
```

### 3. Executar o pipeline SQL

```bash
python scripts/run_pipeline.py
```

Cria as tabelas, importa os dados, aplica tratamentos e executa as consultas analíticas.

### 4. Gerar o dump do banco

```bash
python scripts/export_dump.py
```

Gera `dump/criminalidade_ce.duckdb`, `dump/criminalidade_ce.sql` e CSVs em `dump/csv/`.

### 5. Abrir o dashboard

```bash
python dashboard/app.py
```

Acesse [http://127.0.0.1:8050](http://127.0.0.1:8050) no navegador.

### 6. Gerar PDF do relatório

```bash
python scripts/export_relatorio_pdf.py
```

## Fonte dos dados

- **SSPDS/CEO** — Secretaria da Segurança Pública e Defesa Social do Ceará
- Período: janeiro/2021 a dezembro/2023
- Dataset principal: `dados/dados_filtrados_2021_a_2023.csv` (9.239 registros de mortes violentas)
- Dataset bruto de referência: `dados/raw/CVP_2021_a_2023.csv`

## Relatório

- Markdown: [`relatorio/relatorio.md`](relatorio/relatorio.md)
- PDF: [`relatorio/relatorio.pdf`](relatorio/relatorio.pdf) (gerado via `export_relatorio_pdf.py`)

## Restaurar o banco a partir do dump

```bash
# Opção A — pipeline completo (recomendado)
python scripts/run_pipeline.py

# Opção B — dump SQL + CSVs em dump/
duckdb dump/criminalidade_ce.duckdb < dump/criminalidade_ce.sql
# depois executar sql/03_tratamento.sql e sql/04_consultas.sql
```
