#!/usr/bin/env python3
"""Group a folder of postings (.txt, .md, .eml) into duplicates and mirrors.

Usage:
    python3 -I dedupe_postings.py <folder> [--threshold 0.6] [--json]

Exact duplicates share a fingerprint (same posting re-sent). Mirrors share
at least `threshold` of their near_key positions (same request, different
broker). Output: one group per line, exact duplicates marked "=", mirrors "~".
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from parse_posting import near_similarity, parse, read_text  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--threshold", type=float, default=0.6)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    items = []
    for p in sorted(Path(args.folder).iterdir()):
        if p.suffix.lower() not in {".txt", ".md", ".eml"}:
            continue
        text, _ = read_text(p)
        r = parse(text)
        items.append({"file": p.name, "fingerprint": r["fingerprint"], "near_key": r["near_key"],
                      "broker": r["broker"], "words": r["word_count"]})

    groups = []  # each: {"members": [...], "kind": "=" | "~"}
    for it in items:
        placed = False
        for g in groups:
            head = g["members"][0]
            if it["fingerprint"] == head["fingerprint"]:
                g["members"].append(it)
                placed = True
                break
            if near_similarity(it["near_key"], head["near_key"]) >= args.threshold:
                g["members"].append(it)
                g["kind"] = "~"
                placed = True
                break
        if not placed:
            groups.append({"members": [it], "kind": "="})

    if args.json:
        print(json.dumps(groups, ensure_ascii=False, indent=2))
        return
    for i, g in enumerate(groups, 1):
        names = ", ".join(f"{m['file']} ({m['broker'] or '?'})" for m in g["members"])
        mark = g["kind"] if len(g["members"]) > 1 else " "
        print(f"{i:3d} {mark} {names}")


if __name__ == "__main__":
    main()
