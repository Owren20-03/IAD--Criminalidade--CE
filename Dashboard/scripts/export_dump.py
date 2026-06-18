"""
Exporta o banco DuckDB, dump SQL restaurável e CSVs auxiliares.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

import duckdb

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import DB_PATH, DUMP_DIR, FILTERED_CSV, SQL_DIR  # noqa: E402
from run_pipeline import run_pipeline  # noqa: E402


def _sql_literal(value) -> str:
    if value is None:
        return "NULL"
    if isinstance(value, (int, float)):
        return str(value)
    escaped = str(value).replace("'", "''")
    return f"'{escaped}'"


def export_full_sql(con: duckdb.DuckDBPyConnection, out_path: Path, csv_dir: Path) -> None:
    csv_dir.mkdir(parents=True, exist_ok=True)

    con.execute(f"COPY municipios TO '{(csv_dir / 'municipios.csv').as_posix()}' (HEADER, DELIMITER ',')")
    con.execute(f"COPY mortes_violentas TO '{(csv_dir / 'mortes_violentas.csv').as_posix()}' (HEADER, DELIMITER ',')")

    lines = [
        "-- Dump SQL completo — IAD Criminalidade CE",
        f"-- Gerado a partir de {FILTERED_CSV.name}",
        "-- Restauração (DuckDB):",
        "--   duckdb dump/criminalidade_ce.duckdb < dump/criminalidade_ce.sql",
        "-- Ou execute os scripts sql/01 a 04 via run_pipeline.py",
        "",
    ]

    criacao = (SQL_DIR / "01_criacao.sql").read_text(encoding="utf-8")
    lines.append(criacao)
    lines.append("")

    # municipios via INSERT (tabela pequena)
    mun_rows = con.execute("SELECT id, nome, regiao FROM municipios ORDER BY id").fetchall()
    lines.append(f"-- municipios: {len(mun_rows)} registros")
    for row in mun_rows:
        lines.append(
            f"INSERT INTO municipios (id, nome, regiao) VALUES "
            f"({_sql_literal(row[0])}, {_sql_literal(row[1])}, {_sql_literal(row[2])});"
        )
    lines.append("")

    mortes_count = con.execute("SELECT COUNT(*) FROM mortes_violentas").fetchone()[0]
    lines.append(f"-- mortes_violentas: {mortes_count:,} registros")
    lines.append("-- Carga via CSV (mais eficiente que 9k INSERTs):")
    lines.append(
        f"COPY mortes_violentas FROM '{(csv_dir / 'mortes_violentas.csv').as_posix()}' "
        "(HEADER, DELIMITER ',');"
    )
    lines.append("")
    lines.append("-- Após restaurar tabelas base, execute sql/03_tratamento.sql e sql/04_consultas.sql")

    out_path.write_text("\n".join(lines), encoding="utf-8")


def export_schema_summary(con: duckdb.DuckDBPyConnection, out_path: Path) -> None:
    lines = [
        "-- Resumo do schema e contagens",
        f"-- Fonte: {FILTERED_CSV.name}",
        "",
    ]
    tables = con.execute(
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'main' AND table_type = 'BASE TABLE'
        ORDER BY table_name
        """
    ).fetchall()
    for (table,) in tables:
        count = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        lines.append(f"-- {table}: {count:,} registros")

    views = con.execute(
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'main' AND table_type = 'VIEW'
        ORDER BY table_name
        """
    ).fetchall()
    lines.append("")
    lines.append("-- Views analíticas:")
    for (view,) in views:
        lines.append(f"--   {view}")

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    DUMP_DIR.mkdir(parents=True, exist_ok=True)
    csv_dir = DUMP_DIR / "csv"

    if not DB_PATH.exists():
        print("Banco não encontrado. Executando pipeline...")
        con = run_pipeline()
    else:
        con = duckdb.connect(str(DB_PATH))

    export_full_sql(con, DUMP_DIR / "criminalidade_ce.sql", csv_dir)
    export_schema_summary(con, DUMP_DIR / "schema_reference.sql")
    con.close()

    backup = DUMP_DIR / "criminalidade_ce_backup.duckdb"
    if DB_PATH.exists():
        shutil.copy2(DB_PATH, backup)

    print(f"Dump DuckDB: {DB_PATH}")
    print(f"Dump SQL:    {DUMP_DIR / 'criminalidade_ce.sql'}")
    print(f"CSVs:        {csv_dir}")
    print(f"Schema:      {DUMP_DIR / 'schema_reference.sql'}")


if __name__ == "__main__":
    main()
