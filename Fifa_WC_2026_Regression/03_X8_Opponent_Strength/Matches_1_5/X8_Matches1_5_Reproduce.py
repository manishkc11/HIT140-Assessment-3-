#!/usr/bin/env python3
"""Reproduce X8 for FIFA World Cup 2026 master match IDs 1–5.

Academic integrity / provenance:
    Historical fixtures and dated FIFA-ranking positions in the v2 source CSV
    were gathered, compared and documented with generative-AI assistance in
    earlier research stages. Python code in this file was also AI-generated.
    This program checks structural and chronological consistency and performs
    calculations; it does NOT independently authenticate online sources.

    Nicaragua's October 2025 rank of 133 is an unresolved provisional baseline;
    a user-reported alternative is 132. This program reports the sensitivity
    separately without changing any input ranking.

Usage:
    python X8_Matches1_5_Reproduce.py
    python X8_Matches1_5_Reproduce.py --input custom.csv --output result.csv

Input must contain the original 50 v2 observations with their source metadata.
Only five matches are processed; no master Excel file is read or edited.
"""
from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from datetime import date
from decimal import Decimal
from pathlib import Path

DEFAULT_INPUT = "X8_Matches1_5_Input_Extract.csv"
DEFAULT_OUTPUT = "X8_Matches1_5_Calculated_Results.csv"
EXPECTED_IDS = set(range(1, 6))
EXPECTED_OBSERVATIONS = 50
SENSITIVE_MATCH = 5
SENSITIVE_SIDE = "A"
SENSITIVE_OPPONENT = "Nicaragua"
SENSITIVE_FIXTURE_DATE = "2025-11-18"
SENSITIVE_RANK_EDITION = "2025-10-17"
SENSITIVE_BASELINE = 133
SENSITIVE_ALTERNATIVE = 132

FIELDS = [
    "match_id", "world_cup_match_date", "team_a", "team_b",
    "team_a_previous_opponents_with_ranks", "team_b_previous_opponents_with_ranks",
    "team_a_rank_sum", "team_b_rank_sum",
    "team_a_average_opponent_rank", "team_b_average_opponent_rank",
    "x8_last5_opponent_strength_diff",
    "oct_2025_nicaragua_baseline_rank", "oct_2025_nicaragua_alternative_rank",
    "x8_if_oct_2025_nicaragua_rank_132", "x8_change_if_rank_132",
    "ranking_source_quality_note",
]


def parse_iso(raw: str, description: str) -> date:
    if not raw:
        raise ValueError(f"Missing {description}")
    try:
        return date.fromisoformat(raw)
    except ValueError as exc:
        raise ValueError(f"Invalid {description}: {raw!r}") from exc


def fmt2(value: Decimal) -> str:
    """Format for reporting only; never round an intermediate sum or mean."""
    return format(value, ".2f")


def read_and_validate(path: Path) -> dict[tuple[int, str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {
            "match_id", "world_cup_match_date", "team_side", "team",
            "world_cup_opponent", "previous_match_recency",
            "previous_match_date", "previous_opponent", "opponent_fifa_rank",
            "ranking_publication_date", "verified_historical_edition",
            "primary_ranking_evidence_url", "verification_status",
        }
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(f"Missing required input columns: {sorted(required - set(reader.fieldnames or []))}")
        rows = list(reader)

    if len(rows) != EXPECTED_OBSERVATIONS:
        raise ValueError(f"Expected exactly 50 observations, got {len(rows)}")

    grouped = defaultdict(list)
    recency_keys = set()
    fixture_keys = set()
    match_details: dict[int, tuple[str, dict[str, tuple[str, str]]]] = {}

    for row_no, row in enumerate(rows, start=2):
        try:
            match_id = int(row["match_id"])
            side = row["team_side"].strip()
            recency = int(row["previous_match_recency"])
            rank = int(row["opponent_fifa_rank"])
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Row {row_no}: invalid match ID, recency, or integer rank") from exc
        if match_id not in EXPECTED_IDS or side not in {"A", "B"}:
            raise ValueError(f"Row {row_no}: invalid match ID/side {match_id}/{side}")
        if recency not in range(1, 6) or not (1 <= rank <= 250):
            raise ValueError(f"Row {row_no}: invalid recency or FIFA rank")
        if not row["team"].strip() or not row["previous_opponent"].strip():
            raise ValueError(f"Row {row_no}: missing team or previous opponent")

        wc_date = parse_iso(row["world_cup_match_date"], "current match date")
        prev_date = parse_iso(row["previous_match_date"], "previous match date")
        published_date = parse_iso(row["ranking_publication_date"], "ranking publication date")
        edition = parse_iso(row["verified_historical_edition"], "verified ranking edition")
        if not (published_date < prev_date < wc_date):
            raise ValueError(f"Row {row_no}: date order must be ranking publication < previous fixture < WC fixture")
        if edition != published_date:
            raise ValueError(f"Row {row_no}: ranking edition and publication date do not match")
        if not row["primary_ranking_evidence_url"].startswith("https://"):
            raise ValueError(f"Row {row_no}: missing HTTPS primary ranking evidence URL")

        rec_key = (match_id, side, recency)
        fixture_key = (match_id, side, row["previous_match_date"], row["previous_opponent"])
        if rec_key in recency_keys:
            raise ValueError(f"Row {row_no}: duplicate match/side/recency {rec_key}")
        if fixture_key in fixture_keys:
            raise ValueError(f"Row {row_no}: duplicate previous fixture {fixture_key}")
        recency_keys.add(rec_key)
        fixture_keys.add(fixture_key)
        grouped[(match_id, side)].append(row)

        if match_id not in match_details:
            match_details[match_id] = (row["world_cup_match_date"], {})
        previous_date, teams = match_details[match_id]
        if previous_date != row["world_cup_match_date"]:
            raise ValueError(f"Row {row_no}: inconsistent current-match date for ID {match_id}")
        pair = (row["team"], row["world_cup_opponent"])
        if side in teams and teams[side] != pair:
            raise ValueError(f"Row {row_no}: inconsistent team/opponent for match {match_id} side {side}")
        teams[side] = pair

    expected_groups = {(mid, side) for mid in EXPECTED_IDS for side in ("A", "B")}
    if set(grouped) != expected_groups:
        raise ValueError("Expected exactly 5 A + 5 B observations for every match ID 1–5")

    for match_id in sorted(EXPECTED_IDS):
        _, teams = match_details[match_id]
        if teams["A"][0] != teams["B"][1] or teams["B"][0] != teams["A"][1]:
            raise ValueError(f"Team A/B ordering or opponents inconsistent for match {match_id}")
        for side in ("A", "B"):
            team_rows = sorted(grouped[(match_id, side)], key=lambda r: int(r["previous_match_recency"]))
            if len(team_rows) != 5 or [int(r["previous_match_recency"]) for r in team_rows] != [1, 2, 3, 4, 5]:
                raise ValueError(f"Expected each recency 1–5 once for match {match_id}, side {side}")
            fixture_dates = [parse_iso(r["previous_match_date"], "previous match date") for r in team_rows]
            if fixture_dates != sorted(fixture_dates, reverse=True):
                raise ValueError(f"Previous-match recency not in date order for {match_id}, side {side}")
            grouped[(match_id, side)] = team_rows
    return dict(grouped)


def calculate(groups: dict[tuple[int, str], list[dict[str, str]]]) -> list[dict[str, str]]:
    baseline_rows = [r for r in groups[(SENSITIVE_MATCH, SENSITIVE_SIDE)]
                     if r["previous_opponent"] == SENSITIVE_OPPONENT
                     and r["previous_match_date"] == SENSITIVE_FIXTURE_DATE
                     and r["ranking_publication_date"] == SENSITIVE_RANK_EDITION]
    if len(baseline_rows) != 1 or int(baseline_rows[0]["opponent_fifa_rank"]) != SENSITIVE_BASELINE:
        raise ValueError("The required provisional Nicaragua 133 baseline is missing or has changed")

    results = []
    for mid in sorted(EXPECTED_IDS):
        a = groups[(mid, "A")]
        b = groups[(mid, "B")]
        a_ranks = [int(r["opponent_fifa_rank"]) for r in a]
        b_ranks = [int(r["opponent_fifa_rank"]) for r in b]
        a_sum, b_sum = sum(a_ranks), sum(b_ranks)
        a_mean = Decimal(a_sum) / Decimal(len(a_ranks))
        b_mean = Decimal(b_sum) / Decimal(len(b_ranks))
        x8 = a_mean - b_mean

        alt_x8, delta, base_rank, alternative = "", "", "", ""
        if mid == SENSITIVE_MATCH:
            alternative_a_sum = a_sum - SENSITIVE_BASELINE + SENSITIVE_ALTERNATIVE
            alternative_x8 = Decimal(alternative_a_sum) / Decimal(len(a_ranks)) - b_mean
            alt_x8, delta = fmt2(alternative_x8), fmt2(alternative_x8 - x8)
            base_rank, alternative = str(SENSITIVE_BASELINE), str(SENSITIVE_ALTERNATIVE)
        quality_note = (
            "October 2025 Nicaragua ranking is PROVISIONAL: 133 retained from v2; "
            "user-reported contemporary source says 132; no official row-level resolution."
            if mid == SENSITIVE_MATCH else
            "Ranking inputs come from AI-assisted v2 source audit; some rely on third-party historical archives."
        )
        results.append({
            "match_id": str(mid),
            "world_cup_match_date": a[0]["world_cup_match_date"],
            "team_a": a[0]["team"], "team_b": b[0]["team"],
            "team_a_previous_opponents_with_ranks": "; ".join(f"{r['previous_opponent']} ({r['opponent_fifa_rank']})" for r in a),
            "team_b_previous_opponents_with_ranks": "; ".join(f"{r['previous_opponent']} ({r['opponent_fifa_rank']})" for r in b),
            "team_a_rank_sum": str(a_sum), "team_b_rank_sum": str(b_sum),
            "team_a_average_opponent_rank": fmt2(a_mean),
            "team_b_average_opponent_rank": fmt2(b_mean),
            "x8_last5_opponent_strength_diff": fmt2(x8),
            "oct_2025_nicaragua_baseline_rank": base_rank,
            "oct_2025_nicaragua_alternative_rank": alternative,
            "x8_if_oct_2025_nicaragua_rank_132": alt_x8,
            "x8_change_if_rank_132": delta,
            "ranking_source_quality_note": quality_note,
        })
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path(__file__).resolve().parent / DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / DEFAULT_OUTPUT)
    args = parser.parse_args()
    rows = calculate(read_and_validate(args.input))
    with args.output.open("w", encoding="utf-8", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    for row in rows:
        print(f"Match {row['match_id']}: {row['team_a']} v {row['team_b']}: "
              f"A={row['team_a_average_opponent_rank']}, "
              f"B={row['team_b_average_opponent_rank']}, "
              f"X8={row['x8_last5_opponent_strength_diff']}")
    print(f"Validated 50 historical observations; saved {args.output}")


if __name__ == "__main__":
    main()
