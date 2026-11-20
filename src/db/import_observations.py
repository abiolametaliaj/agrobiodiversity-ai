"""Importon vëzhgime nga CSV në SQLite (Java 2, Task 2.3).

Përdorim (nga rrënja e repo-s):
    python src/db/import_observations.py --csv data/sample_observations.csv --db data/observations_demo.db

Vetëm biblioteka standarde të Python-it. Rreshtat me gabim nuk ndalojnë importin:
shënohen në import_errors.log dhe raportohen në fund.
"""
import argparse
import csv
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

REQUIRED = [
    "observation_id", "image_path", "label_status", "data_origin", "date_time",
    "source_name", "license", "consent_status",
]
OBS_OPTIONAL = [
    "image_hash", "class_label", "expert_review", "group_id", "plot_id",
    "crop_type", "phenophase", "device", "observation_method",
]
SOURCE_OPTIONAL = ["source_url", "author"]

ENUMS = {
    "label_status": {"demo", "unverified", "community_verified", "expert_confirmed", "rejected"},
    "expert_review": {"pending", "approved", "rejected", "not_applicable"},
    "data_origin": {"demo", "public_platform", "own_photo"},
    "consent_status": {"own", "cc_open", "permission_granted", "demo", "unverified"},
}
DATE_FORMATS = ("%Y-%m-%d", "%Y-%m-%d %H:%M")


def clean(row):
    """Heq hapësirat; vlerat e zbrazëta bëhen None (NULL në databazë)."""
    out = {}
    for key, value in row.items():
        if key is None:
            continue
        value = (value or "").strip()
        out[key.strip()] = value if value else None
    return out


def parse_date(text):
    for fmt in DATE_FORMATS:
        try:
            datetime.strptime(text, fmt)
            return True
        except ValueError:
            pass
    return False


def validate(row):
    errors = []
    for field in REQUIRED:
        if not row.get(field):
            errors.append(f"fusha e detyrueshme mungon: {field}")
    for field, allowed in ENUMS.items():
        value = row.get(field)
        if value and value not in allowed:
            errors.append(f"vlerë e pavlefshme për {field}: '{value}'")
    if row.get("date_time") and not parse_date(row["date_time"]):
        errors.append(f"format i gabuar i datës: '{row['date_time']}' (pritet YYYY-MM-DD ose YYYY-MM-DD HH:MM)")
    return errors


def get_or_create_source(conn, row):
    params = (row["source_name"], row.get("source_url"), row.get("author"), row["license"])
    found = conn.execute(
        "SELECT source_id FROM image_sources "
        "WHERE source_name IS ? AND source_url IS ? AND author IS ? AND license IS ?",
        params,
    ).fetchone()
    if found:
        return found[0]
    cur = conn.execute(
        "INSERT INTO image_sources (source_name, source_url, author, license, consent_status) "
        "VALUES (?, ?, ?, ?, ?)",
        params + (row["consent_status"],),
    )
    return cur.lastrowid


def insert_observation(conn, row, source_id):
    conn.execute(
        """INSERT INTO observations
           (observation_id, image_path, image_hash, class_label, label_status, expert_review,
            data_origin, group_id, plot_id, date_time, crop_type, phenophase, device,
            observation_method, source_id)
           VALUES (?, ?, ?, ?, ?, COALESCE(?, 'pending'), ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            row["observation_id"], row["image_path"], row.get("image_hash"), row.get("class_label"),
            row["label_status"], row.get("expert_review"), row["data_origin"], row.get("group_id"),
            row.get("plot_id"), row["date_time"], row.get("crop_type"), row.get("phenophase"),
            row.get("device"), row.get("observation_method"), source_id,
        ),
    )


def main():
    parser = argparse.ArgumentParser(description="Import vëzhgimesh nga CSV në SQLite")
    parser.add_argument("--csv", required=True, help="skedari CSV me vëzhgime")
    parser.add_argument("--db", required=True, help="skedari SQLite (krijohet nëse mungon)")
    parser.add_argument("--schema", default=str(Path(__file__).with_name("schema.sql")))
    parser.add_argument("--log", default="import_errors.log", help="skedari i gabimeve")
    args = parser.parse_args()

    Path(args.db).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(args.db)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(Path(args.schema).read_text(encoding="utf-8"))

    imported, errors = 0, []
    with open(args.csv, newline="", encoding="utf-8-sig") as f:
        for line_no, raw in enumerate(csv.DictReader(f), start=2):  # rreshti 1 = titujt
            row = clean(raw)
            problems = validate(row)
            if problems:
                errors.append((line_no, row.get("observation_id"), "; ".join(problems)))
                continue
            try:
                with conn:  # transaksion për çdo rresht
                    source_id = get_or_create_source(conn, row)
                    insert_observation(conn, row, source_id)
                imported += 1
            except sqlite3.IntegrityError as exc:
                errors.append((line_no, row.get("observation_id"), f"gabim databaze: {exc}"))
    conn.close()

    print(f"U importuan {imported} regjistrime. Gabime: {len(errors)}.")
    if errors:
        with open(args.log, "w", encoding="utf-8") as log:
            for line_no, obs_id, msg in errors:
                line = f"rreshti {line_no} ({obs_id}): {msg}"
                print("  " + line)
                log.write(line + "\n")
        print(f"Gabimet u shkruan te {args.log}")
        sys.exit(1)


if __name__ == "__main__":
    main()
