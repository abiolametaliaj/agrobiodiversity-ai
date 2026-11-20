"""Ekzekuton queries.sql mbi databazën dhe shfaq rezultatet (prova leximi, Java 2).

Përdorim:
    python src/db/run_queries.py --db data/observations_demo.db --out docs/sql_read_tests.txt
"""
import argparse
import re
import sqlite3
from pathlib import Path


def render(columns, rows):
    table = [list(columns)] + [["" if v is None else str(v) for v in r] for r in rows]
    widths = [max(len(r[i]) for r in table) for i in range(len(columns))]
    lines = []
    for idx, r in enumerate(table):
        lines.append(" | ".join(v.ljust(widths[i]) for i, v in enumerate(r)))
        if idx == 0:
            lines.append("-+-".join("-" * w for w in widths))
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", required=True)
    parser.add_argument("--queries", default=str(Path(__file__).with_name("queries.sql")))
    parser.add_argument("--out", help="skedar teksti për rezultatet (UTF-8)")
    args = parser.parse_args()

    text = Path(args.queries).read_text(encoding="utf-8")
    blocks = re.split(r"^-- (Q\d+: .*)$", text, flags=re.MULTILINE)[1:]
    conn = sqlite3.connect(args.db)
    output = []
    for title, sql in zip(blocks[0::2], blocks[1::2]):
        cur = conn.execute(sql.strip())
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description]
        output.append(f"== {title} ({len(rows)} rreshta) ==\n{render(cols, rows)}\n")
    conn.close()

    result = "\n".join(output)
    print(result)
    if args.out:
        Path(args.out).write_text(result, encoding="utf-8")


if __name__ == "__main__":
    main()
