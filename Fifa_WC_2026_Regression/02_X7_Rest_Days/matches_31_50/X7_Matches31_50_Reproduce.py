"""Reproduce X7 (Rest Days Difference), FIFA World Cup 2026 match IDs 31–50.

ACADEMIC INTEGRITY / HISTORICAL RESEARCH PROVENANCE
---------------------------------------------------
* The match extract was copied read-only from the team's original master workbook.
* Previous-match dates, opponents and links were selected WITH AI ASSISTANCE
  from the existing earlier World Cup fixtures in the master dataset and
  researched, match-specific FIFA/national-FA/confederation records.
* Historical source details are in X7_Matches31_50_Previous_Matches.csv.
  Their inclusion does not mean this Python script has independently verified
  the original web content or exhaustive completeness of team schedules.
* Every team's immediately preceding fixture in this batch is an earlier
  completed World Cup match, not a pre-tournament friendly.
* 'source_url' links to one MATCH-SPECIFIC source; 'chronology_url' is a
  GENERAL FIFA tournament results page. Reuse of a link is NOT an independent
  confirmation. Both sides of the same previous match intentionally reuse
  the SAME original match-specific record (one document, not two sources).
* Rest days = (current local calendar date - previous fixture local calendar
  date).days. Example: 19 June - 13 June = 6, NOT 5 intervening days.
* X7 = Team A rest days - Team B rest days, preserving master ordering.
* Blank/unverified previous-match dates are NOT converted to zero: the
  corresponding rest days and X7 stay blank and are flagged.
* This script does not modify, import or write the Excel master dataset.

Place these inputs alongside this script:
    X7_Matches31_50_Master_Extract.csv
    X7_Matches31_50_Previous_Matches.csv

Run: python X7_Matches31_50_Reproduce.py
No third-party packages required; output is X7_Matches31_50_Calculated_Results.csv.
"""
from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

BASE = Path(__file__).resolve().parent
MATCH_FILE = BASE / "X7_Matches31_50_Master_Extract.csv"
PREVIOUS_FILE = BASE / "X7_Matches31_50_Previous_Matches.csv"
OUTPUT_FILE = BASE / "X7_Matches31_50_Calculated_Results.csv"

OUTPUT_COLUMNS = [
    "match_id", "match_date", "team_a", "team_b",
    "team_a_previous_date", "team_a_previous_opponent", "team_a_rest_days",
    "team_b_previous_date", "team_b_previous_opponent", "team_b_rest_days",
    "x7_rest_days_difference", "team_a_source_url", "team_b_source_url",
    "team_a_chronology_url", "team_b_chronology_url", "validation_notes"
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def date_and_rest(previous: str, current: date, label: str) -> tuple[date | None, int | None]:
    if not previous.strip():
        return None, None
    prior = date.fromisoformat(previous)
    if prior >= current:
        raise ValueError(f"Invalid previous fixture date (not earlier) for {label}: {prior}")
    return prior, (current - prior).days


def main() -> None:
    matches = read_csv(MATCH_FILE)
    history = read_csv(PREVIOUS_FILE)
    ids = [int(m["match_id"]) for m in matches]
    if ids != list(range(31, 51)):
        raise ValueError(f"Expected match IDs 31-50 exactly, in order; got {ids}")
    if len(history) != 40:
        raise ValueError(f"Expected 40 (20 x 2) team records; got {len(history)}")

    by_key: dict[tuple[str, str], dict[str, str]] = {}
    for record in history:
        key = (record["match_id"], record["side"])
        if record["side"] not in {"A", "B"} or key in by_key:
            raise ValueError(f"Invalid/duplicate team observation {key}")
        # Check that source details have not been silently omitted. Do NOT
        # pretend two URLs are two independent pieces of evidence.
        if record["previous_match_date"].strip():
            if not record["source_url"].startswith("https://"):
                raise ValueError(f"Missing source URL for {key}")
            if not record["chronology_url"].startswith("https://"):
                raise ValueError(f"Missing general chronology URL for {key}")
        by_key[key] = record

    output: list[dict[str, object]] = []
    for match in matches:
        mid = match["match_id"]
        current = date.fromisoformat(match["match_date"])
        a = by_key.get((mid, "A"))
        b = by_key.get((mid, "B"))
        if a is None or b is None:
            raise ValueError(f"Team A/B observation missing at match {mid}")
        if a["team"] != match["team_a"] or b["team"] != match["team_b"]:
            raise ValueError(f"Team ordering or spelling mismatch at match {mid}")

        prev_a, rest_a = date_and_rest(a["previous_match_date"], current, f"{mid} A")
        prev_b, rest_b = date_and_rest(b["previous_match_date"], current, f"{mid} B")
        x7: int | str = rest_a - rest_b if rest_a is not None and rest_b is not None else ""
        issues: list[str] = []
        if prev_a is None:
            issues.append("UNVERIFIED Team A previous fixture: date missing")
        if prev_b is None:
            issues.append("UNVERIFIED Team B previous fixture: date missing")
        if not a["previous_opponent"].strip() or not b["previous_opponent"].strip():
            x7 = ""
            issues.append("UNVERIFIED previous opponent missing")
        if a["source_url"] == b["source_url"] and a["source_url"]:
            issues.append("SAME URL for both sides: shared fixture evidence, not two independent sources")
        notes = " | ".join(n for n in [a.get("notes", ""), b.get("notes", ""), *issues] if n)

        output.append({
            "match_id": mid, "match_date": current.isoformat(),
            "team_a": match["team_a"], "team_b": match["team_b"],
            "team_a_previous_date": prev_a.isoformat() if prev_a else "",
            "team_a_previous_opponent": a["previous_opponent"],
            "team_a_rest_days": rest_a if rest_a is not None else "",
            "team_b_previous_date": prev_b.isoformat() if prev_b else "",
            "team_b_previous_opponent": b["previous_opponent"],
            "team_b_rest_days": rest_b if rest_b is not None else "",
            "x7_rest_days_difference": x7,
            "team_a_source_url": a["source_url"],
            "team_b_source_url": b["source_url"],
            "team_a_chronology_url": a["chronology_url"],
            "team_b_chronology_url": b["chronology_url"],
            "validation_notes": notes,
        })

    with OUTPUT_FILE.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(output)

    print("ID | Team A         | Team B         | A rest | B rest | X7")
    print("---+----------------+----------------+--------+--------+----")
    for row in output:
        x = row["x7_rest_days_difference"]
        result = f"{x:+d}" if isinstance(x, int) else "UNVERIFIED"
        print(f"{int(row['match_id']):>2} | {row['team_a']:<14} | {row['team_b']:<14} | "
              f"{str(row['team_a_rest_days']):>6} | {str(row['team_b_rest_days']):>6} | {result}")
    print(f"Processed {len(output)} matches; wrote {OUTPUT_FILE.name}")


if __name__ == "__main__":
    main()
