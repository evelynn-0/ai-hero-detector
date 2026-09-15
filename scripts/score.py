#!/usr/bin/env python3
"""Calculate scores from semantic annotations; never infer labels from text."""
import json
import sys
from fractions import Fraction

KEYS = ("J", "M", "A", "R", "T", "V")
WEIGHTS = (20, 15, 20, 15, 15, 15)
LABELS = ("话术信号较少", "有一些包装表达", "话术与实质混合", "话术明显主导", "宣言与包装很密集")

def calculate(data):
    if not isinstance(data, dict) or set(data) != {"units"}:
        raise ValueError('input must be an object with only "units"')
    units = data["units"]
    if not isinstance(units, list):
        raise ValueError("units must be a list")
    seen = set()
    for unit in units:
        if not isinstance(unit, dict) or set(unit) != {"id", "quote", "scores"}:
            raise ValueError("each unit requires id, quote, scores only")
        for key in ("id", "quote"):
            if not isinstance(unit[key], str) or not unit[key].strip():
                raise ValueError(key + " must be nonempty text")
        if unit["id"] in seen:
            raise ValueError("duplicate unit id")
        seen.add(unit["id"])
        scores = unit["scores"]
        if not isinstance(scores, dict) or set(scores) != set(KEYS):
            raise ValueError("scores must contain exactly J, M, A, R, T, V")
        if any(type(v) is not int or not 0 <= v <= 4 for v in scores.values()):
            raise ValueError("scores must be integers from 0 to 4; booleans are invalid")
    if not units:
        return {"version": "0.1.0", "n": 0, "score": None, "label": "无法评分"}
    means = {k: Fraction(sum(u["scores"][k] for u in units), len(units)) for k in KEYS}
    contributions = {k: w * (4 - means[k] if k == "V" else means[k]) / 4 for k, w in zip(KEYS, WEIGHTS)}
    raw = sum(contributions.values())
    score = int(raw + Fraction(1, 2))
    return {"version": "0.1.0", "n": len(units), "score": score,
            "raw_score": float(raw), "label": LABELS[min(score // 20, 4)],
            "means": {k: float(v) for k, v in means.items()},
            "contributions": {k: float(v) for k, v in contributions.items()},
            "note": "V contribution is the information gap; semantic annotations are not validated."}

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 scripts/score.py annotations.json", file=sys.stderr)
        return 2
    try:
        with open(sys.argv[1], encoding="utf-8") as stream:
            result = calculate(json.load(stream))
    except (OSError, ValueError, TypeError) as error:
        print("Invalid input: " + str(error), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(main())
