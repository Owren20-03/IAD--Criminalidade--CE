"""Utilitários compartilhados do projeto IAD."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DADOS_DIR = ROOT / "dados"
RAW_DIR = DADOS_DIR / "raw"
SQL_DIR = ROOT / "sql"
DUMP_DIR = ROOT / "dump"
OUTPUTS_DIR = ROOT / "outputs"
DB_PATH = DUMP_DIR / "criminalidade_ce.duckdb"

FILTERED_CSV = DADOS_DIR / "dados_filtrados_2021_a_2023.csv"
RAW_CSV = RAW_DIR / "CVP_2021_a_2023.csv"
OPTIONAL_XLSX = DADOS_DIR / "Dados_Filtrados_2021_a_2023.xlsx"

RM_MUNICIPIOS = (
    "Fortaleza", "Caucaia", "Maracanaú", "Maranguape", "Pacatuba",
    "Aquiraz", "Horizonte", "Eusébio", "Pacajus", "Cascavel",
    "Guaiúba", "Itaitinga", "Pindoretama", "São Gonçalo do Amarante",
)

COLUMN_MAP = {
    "Município": "municipio",
    "AIS": "ais",
    "Natureza": "natureza",
    "Data": "data_ocorrencia",
    "Hora": "hora_ocorrencia",
    "Dia da Semana": "dia_semana",
    "Meio Empregado": "meio_empregado",
    "Gênero": "genero",
    "Idade da Vítima": "idade_vitima_raw",
    "Escolaridade da Vítima": "escolaridade",
    "Raça da Vítima": "raca",
}

DIA_SEMANA_ORDEM = {
    "Segunda": 1,
    "Terça": 2,
    "Quarta": 3,
    "Quinta": 4,
    "Sexta": 5,
    "Sábado": 6,
    "Domingo": 7,
}
