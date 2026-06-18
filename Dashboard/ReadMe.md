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
