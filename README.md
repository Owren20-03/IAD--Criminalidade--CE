## IAD--Criminalidade--CE
Trabalho Final — Análise de Dados com SQL
Disciplina: Introdução à Análise de Dados

## Integrantes
- Flávio Victor
- Henrique Gabriel
- Kaio Victor
- Paulo Henrique

## Tema
Análise de ocorrências criminais no estado do Ceará com base nos dados públicos da Superintendência de Pesquisa e Estratégia de Segurança Pública (SUPESP/SSPDS-CE).

---
## Estrutura do Repositório
```
iad-criminalidade-ce/
├── README.md
├── dados/
│   └── INSTRUCOES_DOWNLOAD.md   # Como baixar os CSVs
├── sql/
│   ├── 01_criacao.sql           # Criação das tabelas
│   ├── 02_importacao.sql        # Carga dos dados
│   ├── 03_tratamento.sql        # Limpeza e transformações
│   └── 04_consultas.sql         # Consultas analíticas finais
├── dump/
│   └── (dump do banco após importação)
└── relatorio/
    └── relatorio.md             # Relatório completo
```

---
## Como Rodar
Pré-requisitos

**1. PostgreSQL 14+** 

**2. DBeaver (recomendado) ou psql**

## Passo a passo

Baixe os dados seguindo as instruções em dados/INSTRUCOES_DOWNLOAD.md

Crie o banco de dados:
```
sql
CREATE DATABASE criminalidade_ce;
```

Execute os scripts SQL na ordem:
```
bashpsql -d criminalidade_ce -f sql/01_criacao.sql
psql -d criminalidade_ce -f sql/02_importacao.sql
psql -d criminalidade_ce -f sql/03_tratamento.sql
psql -d criminalidade_ce -f sql/04_consultas.sql
```

---
## Fonte dos Dados

SSPDS-CE / SUPESP: https://www.sspds.ce.gov.br/estatisticas-2/

Painel estático: https://www.supesp.ce.gov.br/estatistica-sspds/

Período coberto: 2021–2023

Tipos de crime: CVLI (Crimes Violentos Letais e Intencionais) e CVP (Crimes Violentos contra o Patrimônio)
