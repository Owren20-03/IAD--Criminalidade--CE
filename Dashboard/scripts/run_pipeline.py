"""
Executa o pipeline SQL completo via DuckDB.
"""

from __future__ import annotations

import sys
from pathlib import Path

import duckdb

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import DB_PATH, DUMP_DIR, FILTERED_CSV, OUTPUTS_DIR, SQL_DIR  # noqa: E402


def _read_sql(path: Path, **replacements: str) -> str:
    content = path.read_text(encoding="utf-8")
    for key, value in replacements.items():
        content = content.replace(f"{{{{{key}}}}}", value)
    return content


def _export_table(con: duckdb.DuckDBPyConnection, table: str, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    out = output_dir / f"{table}.csv"
    con.execute(f"COPY {table} TO '{out.as_posix()}' (HEADER, DELIMITER ',')")


def run_pipeline(db_path: Path | None = None) -> duckdb.DuckDBPyConnection:
    db_path = db_path or DB_PATH
    DUMP_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    if not FILTERED_CSV.exists():
        raise FileNotFoundError(
            f"CSV não encontrado em {FILTERED_CSV}. Execute prepare_data.py primeiro."
        )

    if db_path.exists():
        db_path.unlink()

    con = duckdb.connect(str(db_path))

    scripts = [
        SQL_DIR / "01_criacao.sql",
        SQL_DIR / "02_importacao.sql",
        SQL_DIR / "03_tratamento.sql",
        SQL_DIR / "04_consultas.sql",
    ]

    for script in scripts:
        print(f"Executando {script.name}...")
        sql = _read_sql(script, CSV_PATH=FILTERED_CSV.as_posix())
        con.execute(sql)

    total = con.execute("SELECT COUNT(*) FROM mortes_violentas").fetchone()[0]
    print(f"\nRegistros importados: {total:,}")

    result_tables = [
        row[0]
        for row in con.execute(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'main'
              AND table_name LIKE 'resultado_%'
            ORDER BY table_name
            """
        ).fetchall()
    ]

    print(f"Exportando {len(result_tables)} tabelas de resultado...")
    for table in result_tables:
        _export_table(con, table, OUTPUTS_DIR)
        print(f"  - {table}")

    # Sanity checks
    anos = con.execute(
        "SELECT ano, COUNT(*) FROM vw_mortes_limpa GROUP BY ano ORDER BY ano"
    ).fetchall()
    print("\nDistribuição por ano:")
    for ano, qtd in anos:
        print(f"  {ano}: {qtd:,}")

    return con


def main() -> None:
    con = run_pipeline()
    con.close()
    print(f"\nPipeline concluído. Banco em {DB_PATH}")


if __name__ == "__main__":
    main()
