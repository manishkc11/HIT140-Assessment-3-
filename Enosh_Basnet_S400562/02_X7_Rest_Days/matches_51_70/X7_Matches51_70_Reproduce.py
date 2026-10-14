"""Reproduce FIFA 2026 X7 for match IDs 51-70 from the two exported CSV inputs.

ACADEMIC INTEGRITY / AI ASSISTANCE
---------------------------------
This script, and the selection of fixture/source records in Previous_Matches.csv,
were prepared with AI assistance. The original 104-match master Excel dataset
was read without modification to identify each team's earlier World Cup
fixtures. FIFA's public results chronology and match-specific reports/videos
were used for source review; this script does not fetch webpages, independently
authenticate URLs or prove exhaustive absence of unrelated international fixtures.

The 'source_url' field in the historical CSV may be a match-specific FIFA
article/video/feature, or (for prior match 44) a FIFA matchday-wide article
containing a specific Jordan-Algeria section. 'chronology_url' is a GENERAL
FIFA fixture-results page. The same source URL for both sides of a previous
match is ONE evidence document, never two independent sources.

Calendar convention: (target local calendar date - previous match local
calendar date).days. It does not use the number of intervening date labels.
X7 = Team A rest days - Team B rest days.

Checks:
- IDs are 51-70 and Team A/Team B ordering matches CSV;
- exactly 40 team observations with no duplicate side;
- historical candidate lists (exported from the earlier master matches) show
  that the chosen previous World Cup fixture is the MOST RECENT eligible one;
- previous opponents/dates/IDs match those history candidate lists;
- both participants' prior fixture evidence and dates are checked for
  internal consistency across all 40 observations;
- previous dates precede the current match (blank remains missing, never 0).

This script reads only the two exported CSV inputs. It DOES NOT modify the
original Excel master dataset and DOES NOT calculate X8.

Run: python X7_Matches51_70_Reproduce.py
Requires Python standard library only.
"""
from __future__ import annotations
import csv
import json
from datetime import date
from pathlib import Path

BASE = Path(__file__).resolve().parent
MATCH_FILE = BASE / "X7_Matches51_70_Master_Extract.csv"
PREVIOUS_FILE = BASE / "X7_Matches51_70_Previous_Matches.csv"
OUTPUT_FILE = BASE / "X7_Matches51_70_Calculated_Results.csv"

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


def get_rest(prior_str: str, current: date, label: str) -> int | None:
    if not prior_str.strip():
        return None
    prior = date.fromisoformat(prior_str)
    if prior >= current:
        raise ValueError(f"Invalid previous fixture date for {label}: {prior}")
    return (current - prior).days


def validate_history(record: dict[str, str], current: date) -> None:
    """Check the previous fixture against ALL earlier World Cup matches for that team
    as copied read-only from the original master workbook into this CSV.
    Does not itself fetch/verify official FIFA results or outside friendly schedules.
    """
    key = f"match {record['match_id']} side {record['side']}"
    previous = record["previous_match_date"].strip()
    if not previous:
        return  # Missing remains missing, not 0.
    candidates = json.loads(record["earlier_world_cup_fixtures_json"])
    if not candidates:
        raise ValueError(f"No previous World Cup candidate records: {key}")
    for item in candidates:
        if not all(name in item for name in ("match_id", "match_date", "opponent")):
            raise ValueError(f"Incomplete earlier fixture: {key}")
        if int(item["match_id"]) >= int(record["match_id"]):
            raise ValueError(f"Future/invalid predecessor ID: {key}")
        if date.fromisoformat(item["match_date"]) >= current:
            raise ValueError(f"Future predecessor date: {key}")
    latest = max(candidates, key=lambda p: (p["match_date"], int(p["match_id"])))
    if int(latest["match_id"]) != int(record["previous_master_match_id"]):
        raise ValueError(f"Selected fixture not latest earlier World Cup fixture: {key}")
    if latest["match_date"] != previous or latest["opponent"] != record["previous_opponent"]:
        raise ValueError(f"Selected previous fixture disagrees with master history: {key}")
    if not record["source_url"].startswith("https://"):
        raise ValueError(f"Missing official source URL: {key}")
    if not record["chronology_url"].startswith("https://"):
        raise ValueError(f"Missing general chronology URL: {key}")
    if record["chronology_source_type"] != "GENERAL_FIFA_TOURNAMENT_RESULTS":
        raise ValueError(f"Chronology not labelled GENERAL: {key}")
    if record["source_type"] not in {
        "MATCH_SPECIFIC", "MATCH_SPECIFIC_VIDEO", "MATCH_SPECIFIC_FEATURE",
        "MATCHDAY_ARTICLE_WITH_FIXTURE_SECTION"
    }:
        raise ValueError(f"Unknown official source type: {key}")


def main() -> None:
    matches = read_csv(MATCH_FILE)
    history = read_csv(PREVIOUS_FILE)
    ids = [int(m["match_id"]) for m in matches]
    if ids != list(range(51, 71)):
        raise ValueError(f"Expected match IDs 51-70 in order, got {ids}")
    if len(history) != 40:
        raise ValueError(f"Expected 40 side-level records; got {len(history)}")
    by_key = {}
    for r in history:
        key = (r["match_id"], r["side"])
        if r["side"] not in {"A", "B"} or key in by_key:
            raise ValueError(f"Invalid/duplicate team-side observation {key}")
        by_key[key] = r
    if set(by_key) != {(str(i), side) for i in range(51, 71) for side in ("A", "B")}:
        raise ValueError("Missing/unexpected match-side history")

    output = []
    for m in matches:
        mid = m["match_id"]
        current = date.fromisoformat(m["match_date"])
        a, b = by_key[(mid, "A")], by_key[(mid, "B")]
        if a["team"] != m["team_a"] or b["team"] != m["team_b"]:
            raise ValueError(f"Master team ordering mismatch for match ID {mid}")
        for record in (a, b):
            validate_history(record, current)

        # Cross-check shared match evidence when both sides refer to the same
        # previous fixture elsewhere in this batch. Reused URL is not two sources.
        rest_a = get_rest(a["previous_match_date"], current, f"{mid} A")
        rest_b = get_rest(b["previous_match_date"], current, f"{mid} B")
        issues = []
        if rest_a is None or not a["previous_opponent"]:
            issues.append("UNVERIFIED Team A previous fixture")
        if rest_b is None or not b["previous_opponent"]:
            issues.append("UNVERIFIED Team B previous fixture")
        if a["source_url"] == b["source_url"]:
            issues.append("SAME source URL for both sides: not independent sources")
        if a["source_type"] == "MATCHDAY_ARTICLE_WITH_FIXTURE_SECTION":
            issues.append("Team A source is a matchday article with a fixture section, not a dedicated match report")
        if b["source_type"] == "MATCHDAY_ARTICLE_WITH_FIXTURE_SECTION":
            issues.append("Team B source is a matchday article with a fixture section, not a dedicated match report")
        x7 = rest_a - rest_b if rest_a is not None and rest_b is not None else ""
        # Don't enter X7 if opponents are missing.
        if not a["previous_opponent"] or not b["previous_opponent"]:
            x7 = ""
        notes = " | ".join([a["notes"], b["notes"], *issues])
        output.append({
            "match_id": mid, "match_date": current.isoformat(),
            "team_a": m["team_a"], "team_b": m["team_b"],
            "team_a_previous_date": a["previous_match_date"],
            "team_a_previous_opponent": a["previous_opponent"],
            "team_a_rest_days": rest_a if rest_a is not None else "",
            "team_b_previous_date": b["previous_match_date"],
            "team_b_previous_opponent": b["previous_opponent"],
            "team_b_rest_days": rest_b if rest_b is not None else "",
            "x7_rest_days_difference": x7,
            "team_a_source_url": a["source_url"],
            "team_b_source_url": b["source_url"],
            "team_a_chronology_url": a["chronology_url"],
            "team_b_chronology_url": b["chronology_url"],
            "validation_notes": notes,
        })

    # Each repeated earlier fixture must be consistent in both participating
    # teams' historical CSV entries (dates and same ONE source URL).
    by_prior = {}
    for r in history:
        mid = r["previous_master_match_id"]
        by_prior.setdefault(mid, []).append(r)
    if len(by_prior) != 20:
        raise ValueError(f"Expected 20 distinct prior fixtures, found {len(by_prior)}")
    for prior_id, entries in by_prior.items():
        if len(entries) != 2:
            raise ValueError(f"Previous fixture ID {prior_id} is not referenced by both participating sides")
        e1, e2 = entries
        if (e1["previous_match_date"] != e2["previous_match_date"] or
            e1["source_url"] != e2["source_url"] or
            e1["team"] != e2["previous_opponent"] or
            e2["team"] != e1["previous_opponent"]):
            raise ValueError(f"Shared previous fixture has inconsistent details: {prior_id}")

    with OUTPUT_FILE.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS, lineterminator="\r\n")
        writer.writeheader(); writer.writerows(output)
    print("ID | Match date | Team A | Team B | A rest | B rest | X7")
    for r in output:
        print(f"{int(r['match_id']):>2} | {r['match_date']} | {r['team_a']} | {r['team_b']} | {r['team_a_rest_days']} | {r['team_b_rest_days']} | {r['x7_rest_days_difference']}")
    print(f"Processed {len(output)} matches, {len(history)} observations, "
          f"{len(by_prior)} prior fixture matches. Saved {OUTPUT_FILE.name}")


if __name__ == "__main__":
    main()
