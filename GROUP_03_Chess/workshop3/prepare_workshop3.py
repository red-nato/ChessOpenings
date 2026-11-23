"""Refresh W3 chart data from the saved C2 tables and September game split."""

import csv
import json
from collections import Counter, defaultdict
from math import isclose
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
DATA = HERE / "data"
TABLES = PROJECT / "outputs" / "tables"
BANDS = ("Under 1200", "1200-1599", "1600-1999", "2000+")
OUTCOMES = ("win", "draw", "loss")
WHITE_OUTCOME = {"white_win": "win", "draw": "draw", "black_win": "loss"}
OPPONENT_RESULT = {"win": "loss", "draw": "draw", "loss": "win"}
POINTS = {"win": 1, "draw": 0.5, "loss": 0}


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as source:
        return list(csv.DictReader(source))


def write_csv(filename, rows):
    with (DATA / filename).open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def band(rating):
    return BANDS[sum(rating >= cutoff for cutoff in (1200, 1600, 2000))]


def prepare():
    games = read_csv(PROJECT / "data" / "splits" / "test.csv")
    game_ids = {row["game_id"] for row in games}
    assert len(game_ids) == len(games) == 30_553
    assert all(row["start_utc"].startswith("2026-09-01") for row in games)

    manual = read_csv(TABLES / "C2_manual_rule_test.csv")
    actual = defaultdict(Counter)
    for row in games:
        white = WHITE_OUTCOME[row["outcome"]]
        for color, result in (("white", white), ("black", OPPONENT_RESULT[white])):
            key = (color, row["speed"], band(int(row[f"{color}_rating"])))
            actual[key][result] += 1

    rates = {}
    for row in manual:
        key = (row["color"], row["speed"], row["rating_band"])
        counts = actual[key]
        n = counts.total()
        score = sum(count * POINTS[outcome] for outcome, count in counts.items()) / n
        assert n == int(row["n"]) and isclose(score, float(row["score_rate"]), abs_tol=1e-12)
        rates[key] = (n, score)
    assert rates.keys() == actual.keys()

    segments = []
    for rating_band in BANDS:
        for speed in ("blitz", "rapid"):
            n_white, white_rate = rates["white", speed, rating_band]
            n_black, black_rate = rates["black", speed, rating_band]
            segments.append({
                "speed": speed, "rating_band": rating_band,
                "n_white": n_white, "n_black": n_black,
                "white_score_rate": white_rate, "black_score_rate": black_rate,
                "white_minus_black_pp": 100 * (white_rate - black_rate),
            })

    overlap = {row["cluster"]: row for row in read_csv(TABLES / "C2_player_overlap_sensitivity.csv")}
    clusters = []
    for row in read_csv(TABLES / "C2_cluster_profile_by_color_test.csv"):
        sensitivity = overlap[row["cluster"]]
        full = float(row["white_minus_black_pp"])
        unseen = 100 * (float(sensitivity["score_rate_white_unseen_pairs"])
                        - float(sensitivity["score_rate_black_unseen_pairs"]))
        n_full = int(float(row["n_white"])) + int(float(row["n_black"]))
        assert n_full == int(sensitivity["n_full_test"])
        cross_check = 100 * (float(sensitivity["score_rate_white_full_test"])
                             - float(sensitivity["score_rate_black_full_test"]))
        assert isclose(full, cross_check, abs_tol=1e-12)
        clusters.append({
            "cluster": row["cluster"], "n_full": n_full,
            "n_unseen": int(sensitivity["n_unseen_pairs"]),
            "blitz_share": float(row["pct_blitz"]), "mean_rating": float(row["mean_rating"]),
            "full_gap_pp": full, "unseen_gap_pp": unseen,
        })
    assert sum(row["n_full"] for row in clusters) == 2 * len(games)

    membership = {row["game_id"]: row["subset"] for row in
                  read_csv(PROJECT / "data" / "splits" / "membership.csv")}
    assert {key for key, split in membership.items() if split == "test"} == game_ids
    july_players = set()
    september_pairs = []
    with (PROJECT / "data" / "processed" / "games.csv").open(encoding="utf-8", newline="") as source:
        for row in csv.DictReader(source):
            players = (row["white_id"], row["black_id"])
            split = membership[row["game_id"]]
            if split == "train":
                july_players.update(players)
            elif split == "test":
                september_pairs.append(players)
    n_unseen_games = sum(white not in july_players and black not in july_players
                         for white, black in september_pairs)
    assert len(september_pairs) == len(games)
    assert sum(row["n_unseen"] for row in clusters) == 2 * n_unseen_games

    selection = max(segments, key=lambda row: abs(row["white_minus_black_pp"]))
    assert (selection["speed"], selection["rating_band"]) == ("blitz", "2000+")
    opening_counts = defaultdict(Counter)
    for row in games:
        if row["speed"] == selection["speed"] and band(int(row["white_rating"])) == selection["rating_band"]:
            opening_counts[row["opening_family_20"]][WHITE_OUTCOME[row["outcome"]]] += 1
    assert "" not in opening_counts
    assert sum(opening_counts.values(), Counter()) == actual["white", "blitz", "2000+"]

    openings = [
        {"opening_family": name, **{outcome: counts[outcome] for outcome in OUTCOMES}, "games": counts.total()}
        for name, counts in sorted(opening_counts.items(), key=lambda pair: (-pair[1].total(), pair[0]))
    ]
    windows = read_csv(TABLES / "C2_month_sensitivity.csv")
    context = {
        "first_test_utc": min(row["start_utc"] for row in games),
        "last_test_utc": max(row["start_utc"] for row in games),
        "n_test_games": len(games),
        "n_unseen_games": n_unseen_games,
        "largest_window_share_range_pp": 100 * max(float(row["share_max_minus_min"]) for row in windows),
    }
    DATA.mkdir(exist_ok=True)
    write_csv("cluster_gaps.csv", clusters)
    write_csv("segment_gaps.csv", segments)
    write_csv("opening_outcomes.csv", openings)
    (DATA / "context.json").write_text(json.dumps(context, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    prepare()
