#!/usr/bin/env python3
"""Scale per-100 g USDA values to portions and score a day."""

from __future__ import annotations

import json
import sys

TARGETS = {
    "kcal": 2200.0,
    "protein_g": (80.0, 90.0),
    "fiber_g": 25.0,
    "free_sugar_prefer_g": (25.0, 36.0),
}


def scale(item: dict) -> dict:
    grams = float(item["grams"])
    factor = grams / 100.0

    def nutrient(key: str):
        value = item.get(key)
        if value is None:
            return None
        return float(value) * factor

    return {
        "name": item.get("name", ""),
        "amount": item.get("amount", f"{grams:g} g"),
        "grams": grams,
        "kcal": nutrient("kcal_per_100"),
        "protein_g": nutrient("protein_per_100"),
        "fiber_g": nutrient("fiber_per_100"),
        "free_sugar_g": nutrient("free_sugar_per_100"),
        "source": item.get("source", ""),
        "estimated": bool(item.get("estimated", False)),
    }


def fmt(value, digits=1) -> str:
    if value is None:
        return "n/a"
    return f"{value:.{digits}f}"


def add(total: dict, row: dict, key: str) -> None:
    if row[key] is None:
        total[f"{key}_missing"] = True
        return
    total[key] += row[key]


def remaining_kcal(total_kcal: float) -> str:
    return fmt(TARGETS["kcal"] - total_kcal, 0)


def remaining_protein(total_protein: float) -> str:
    low, high = TARGETS["protein_g"]
    return f"{fmt(low - total_protein)} to {fmt(high - total_protein)}"


def remaining_fiber(total_fiber: float) -> str:
    return fmt(TARGETS["fiber_g"] - total_fiber)


def remaining_sugar(total_sugar, total_kcal) -> str:
    if total_sugar is None:
        return "n/a"
    prefer_high = TARGETS["free_sugar_prefer_g"][1]
    max_10pct = 0.10 * total_kcal if total_kcal else 0
    return (
        f"{fmt(prefer_high - total_sugar)} vs prefer 36; "
        f"10% cap {fmt(max_10pct)} g"
    )


def verdict(total: dict) -> str:
    bits = []
    protein = total["protein_g"]
    fiber = total["fiber_g"]
    kcal = total["kcal"]
    sugar = total["free_sugar_g"]

    if protein < 80:
        bits.append("short protein")
    elif protein > 90:
        bits.append("protein above 90 g")
    else:
        bits.append("protein on track")

    if fiber < 25:
        bits.append("short fibre")
    else:
        bits.append("fibre met")

    if kcal > 2400:
        bits.append("over energy")
    elif kcal < 2000:
        bits.append("under energy band")
    else:
        bits.append("energy near maintenance")

    if sugar is None:
        bits.append("free sugar incomplete")
    else:
        cap = 0.10 * kcal if kcal else 0
        if sugar > cap:
            bits.append("over sugar (10% energy)")
        elif sugar > 36:
            bits.append("sugar above preferred band")
        else:
            bits.append("sugar in preferred band")

    return " / ".join(bits)


def render(rows: list[dict]) -> str:
    total = {
        "kcal": 0.0,
        "protein_g": 0.0,
        "fiber_g": 0.0,
        "free_sugar_g": 0.0,
        "kcal_missing": False,
        "protein_g_missing": False,
        "fiber_g_missing": False,
        "free_sugar_g_missing": False,
    }
    lines = [
        "| Food | Amount | kcal | protein_g | fibre_g | free/added sugars_g | source (FDC ID) |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        for key in ("kcal", "protein_g", "fiber_g", "free_sugar_g"):
            add(total, row, key)
        name = row["name"]
        if row["estimated"]:
            name += " (estimated)"
        lines.append(
            "| {name} | {amount} | {kcal} | {pro} | {fib} | {sugar} | {src} |".format(
                name=name,
                amount=row["amount"],
                kcal=fmt(row["kcal"], 0),
                pro=fmt(row["protein_g"]),
                fib=fmt(row["fiber_g"]),
                sugar=fmt(row["free_sugar_g"]),
                src=row["source"],
            )
        )

    def tot(key, digits=1):
        if total[f"{key}_missing"] and total[key] == 0:
            return "n/a"
        if total[f"{key}_missing"]:
            return f"{fmt(total[key], digits)}+"
        return fmt(total[key], digits)

    lines.append(
        "| **Totals** | | {kcal} | {pro} | {fib} | {sugar} | |".format(
            kcal=tot("kcal", 0),
            pro=tot("protein_g"),
            fib=tot("fiber_g"),
            sugar=tot("free_sugar_g"),
        )
    )
    lines.append("| Target | | ~2,200 | 80–90 | 25 | prefer ≤ 25–36 | |")
    lines.append(
        "| Remaining | | {kcal} | {pro} | {fib} | {sugar} | |".format(
            kcal=remaining_kcal(total["kcal"]),
            pro=remaining_protein(total["protein_g"]),
            fib=remaining_fiber(total["fiber_g"]),
            sugar=remaining_sugar(
                None if total["free_sugar_g_missing"] else total["free_sugar_g"],
                total["kcal"],
            ),
        )
    )
    lines.append("")
    lines.append(f"**Verdict:** {verdict(total)}")
    return "\n".join(lines)


def main() -> int:
    raw = sys.stdin.read().strip()
    if not raw:
        print("Pass JSON on stdin with an 'items' array.", file=sys.stderr)
        return 2
    data = json.loads(raw)
    items = data if isinstance(data, list) else data.get("items", [])
    if not items:
        print("No items in JSON.", file=sys.stderr)
        return 2
    rows = [scale(item) for item in items]
    print(render(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
