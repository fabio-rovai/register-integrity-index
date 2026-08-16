#!/usr/bin/env python3
"""Validate the Register Integrity Index.

Recomputes every dimension score and every geometric mean from
data/rii_v1.csv and compares them against the league table published in
README.md. Exits non-zero on any mismatch, on malformed provenance, or on
a prohibited dash character anywhere in the repository's text files.

Scoring rules (see docs/RII_SPEC.md):
  - dimension score = arithmetic mean of its component scores, rounded to 1 dp
  - composite      = geometric mean of the measured dimension scores,
                     each floored at 1.0, rounded to 1 dp
  - coverage       = measured dimensions out of 5; N/A dimensions are excluded
"""
import csv
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "rii_v1.csv"
README_PATH = ROOT / "README.md"
DIMS = ["D1", "D2", "D3", "D4", "D5"]

errors = []


def fail(msg):
    errors.append(msg)


def load_csv():
    rows = []
    with open(CSV_PATH, newline="") as f:
        reader = csv.DictReader(f)
        expected = ["register", "dimension", "component", "raw_metric",
                    "source_repo", "artifact", "formula", "score"]
        if reader.fieldnames != expected:
            fail(f"CSV header is {reader.fieldnames}, expected {expected}")
            return rows
        for i, row in enumerate(reader, start=2):
            for field in expected[:-1]:
                if not row[field].strip():
                    fail(f"CSV line {i}: empty field '{field}'")
            if row["dimension"] not in DIMS:
                fail(f"CSV line {i}: bad dimension '{row['dimension']}'")
            try:
                score = float(row["score"])
            except ValueError:
                fail(f"CSV line {i}: non-numeric score '{row['score']}'")
                continue
            if not 0.0 <= score <= 100.0:
                fail(f"CSV line {i}: score {score} outside [0, 100]")
            row["score"] = score
            rows.append(row)
    return rows


def compute(rows):
    """Return {register: (dim_scores dict, composite, coverage)}."""
    out = {}
    for reg in dict.fromkeys(r["register"] for r in rows):
        dscores = {}
        for d in DIMS:
            comps = [r["score"] for r in rows
                     if r["register"] == reg and r["dimension"] == d]
            if comps:
                dscores[d] = round(sum(comps) / len(comps), 1)
        if len(dscores) < 3:
            fail(f"{reg}: only {len(dscores)} measured dimensions, minimum is 3")
        floored = [max(v, 1.0) for v in dscores.values()]
        composite = round(
            math.exp(sum(math.log(v) for v in floored) / len(floored)), 1)
        out[reg] = (dscores, composite, len(dscores))
    return out


def parse_readme():
    """Parse the league table. Returns list of
    (rank, register, {dim: score-or-None}, composite, coverage)."""
    text = README_PATH.read_text(encoding="utf-8")
    pattern = re.compile(
        r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|"
        r"\s*([\d.]+|N/A)\s*\|\s*([\d.]+|N/A)\s*\|\s*([\d.]+|N/A)\s*\|"
        r"\s*([\d.]+|N/A)\s*\|\s*([\d.]+|N/A)\s*\|"
        r"\s*\*\*([\d.]+)\*\*\s*\|\s*(\d)/5\s*\|\s*$",
        re.MULTILINE)
    parsed = []
    for m in pattern.finditer(text):
        rank = int(m.group(1))
        register = m.group(2)
        dims = {}
        for d, g in zip(DIMS, m.groups()[2:7]):
            dims[d] = None if g == "N/A" else float(g)
        parsed.append((rank, register, dims, float(m.group(8)), int(m.group(9))))
    if not parsed:
        fail("No league table rows found in README.md")
    return parsed


def check_dashes():
    prohibited = {"\u2014": "em dash", "\u2013": "en dash"}
    for path in sorted(ROOT.rglob("*")):
        if path.is_dir() or ".git" in path.parts:
            continue
        if path.suffix not in {".md", ".csv", ".py", ".txt", ""}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, IsADirectoryError):
            continue
        for ch, name in prohibited.items():
            if ch in text:
                fail(f"{path.relative_to(ROOT)}: contains a prohibited {name}")


def main():
    rows = load_csv()
    computed = compute(rows)
    published = parse_readme()

    seen = set()
    for rank, register, dims, composite, coverage in published:
        if register not in computed:
            fail(f"README row '{register}' has no rows in the CSV")
            continue
        seen.add(register)
        cdims, ccomp, ccov = computed[register]
        for d in DIMS:
            pub, comp = dims[d], cdims.get(d)
            if pub is None and comp is None:
                continue
            if pub is None or comp is None or abs(pub - comp) > 0.05:
                fail(f"{register} {d}: README says {pub}, CSV recomputes {comp}")
        if abs(composite - ccomp) > 0.05:
            fail(f"{register} composite: README says {composite}, "
                 f"CSV recomputes {ccomp}")
        if coverage != ccov:
            fail(f"{register} coverage: README says {coverage}/5, "
                 f"CSV recomputes {ccov}/5")

    for reg in computed:
        if reg not in seen:
            fail(f"CSV register '{reg}' missing from the README league table")

    composites = [c for _, _, _, c, _ in published]
    if composites != sorted(composites, reverse=True):
        fail("README league table is not sorted by descending composite")

    check_dashes()

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        print(f"\n{len(errors)} validation error(s).")
        return 1
    print(f"OK: {len(published)} registers, {len(rows)} scored components, "
          f"every dimension mean and geometric mean in README.md matches "
          f"data/rii_v1.csv, no prohibited dashes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
