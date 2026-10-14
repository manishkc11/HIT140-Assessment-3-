"""Reproduce X7 rest-day calculations for FIFA World Cup 2026 match IDs 1-10.

Inputs (both included alongside this script):
    X7_First10_Master_Extract.csv  -- match IDs/dates/team ordering copied from
                                     the user's master workbook, WITHOUT edits
    X7_First10_Previous_Matches.csv -- manually researched historical match
                                      details and source URLs (not AI estimates)

Run:
    python X7_First10_Reproduce.py

No third-party Python packages are required. This script does NOT edit the master.
"""
from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

BASE = Path(__file__).resolve().parent
MATCH_FILE = BASE / "X7_First10_Master_Extract.csv"
PREVIOUS_FILE = BASE / "X7_First10_Previous_Matches.csv"
OUTPUT_FILE = BASE / "X7_First10_Calculated_Results.csv"


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as infile:
        return list(csv.DictReader(infile))


def parse_date(value: str) -> date:
    # ISO 8601 dates are used everywhere, preventing DD/MM vs MM/DD confusion.
    return date.fromisoformat(value)


def main() -> None:
    matches = load_csv(MATCH_FILE)
    history = load_csv(PREVIOUS_FILE)

    ids = [int(row["match_id"]) for row in matches]
    assert ids == list(range(1, 11)), f"Expected IDs 1-10 in order; got {ids}"

    previous_by_key: dict[tuple[str, str], dict[str, str]] = {}
    for record in history:
        key = (record["match_id"], record["side"])
        if key in previous_by_key:
            raise ValueError(f"Duplicate previous-match record for {key}")
        assert record["side"] in ("A", "B"), key
        assert record["previous_opponent"].strip(), key
        assert record["source_url"].startswith("https://"), key
        assert record["chronology_url"].startswith("https://"), key
        previous_by_key[key] = record

    assert len(previous_by_key) == 20, "Expected exactly 20 previous-match records"

    out: list[dict[str, object]] = []
    for m in matches:
        mid = m["match_id"]
        current_date = parse_date(m["match_date"])
        a = previous_by_key[(mid, "A")]
        b = previous_by_key[(mid, "B")]

        # Exact team spelling and Team A/B ordering must match the master.
        if a["team"] != m["team_a"] or b["team"] != m["team_b"]:
            raise ValueError(f"Team mismatch for match_id {mid}")

        date_a = parse_date(a["previous_match_date"])
        date_b = parse_date(b["previous_match_date"])
        if date_a >= current_date or date_b >= current_date:
            raise ValueError(f"Future/same-day previous match for ID {mid}")

        # Calendar DATE subtraction, not 'full days off'.
        rest_a = (current_date - date_a).days
        rest_b = (current_date - date_b).days
        x7 = rest_a - rest_b

        out.append({
            "match_id": mid,
            "match_date": current_date.isoformat(),
            "team_a": m["team_a"],
            "team_b": m["team_b"],
            "team_a_previous_date": date_a.isoformat(),
            "team_a_previous_opponent": a["previous_opponent"],
            "team_a_rest_days": rest_a,
            "team_b_previous_date": date_b.isoformat(),
            "team_b_previous_opponent": b["previous_opponent"],
            "team_b_rest_days": rest_b,
            "x7_rest_days_difference": x7,
            "team_a_source_url": a["source_url"],
            "team_b_source_url": b["source_url"],
            "team_a_chronology_url": a["chronology_url"],
            "team_b_chronology_url": b["chronology_url"],
            "validation_notes": " | ".join(x for x in [a.get("notes", ""), b.get("notes", "")] if x),
        })

    with OUTPUT_FILE.open("w", encoding="utf-8-sig", newline="") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=list(out[0]))
        writer.writeheader()
        writer.writerows(out)

    print("Match ID | Team A rest | Team B rest | X7")
    print("---------+-------------+-------------+----")
    for row in out:
        print(f"{row['match_id']:>8} | {row['team_a_rest_days']:>11} | "
              f"{row['team_b_rest_days']:>11} | {row['x7_rest_days_difference']:+d}")
    print(f"Wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
