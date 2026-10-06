---
name: calc-nutrition
description: Calculate today's calories, protein, and fibre from foods and amounts the user lists. Invoke with /calc-nutrition and paste the day's food log. Scores against 80-90 g protein, 25 g fibre, and ~2200 kcal.
disable-model-invocation: true
---

# Calculate daily nutrition

Score one day’s food for **calories, protein, and fibre** (also free/added sugars) against this project’s personal targets. The user invokes `/calc-nutrition` and pastes foods with quantities in the same message.

Read `CLAUDE.md` in the repo root for the full profile, sugar rules, and usual-day assumptions. Use `references/common-foods.md` in this skill for foods already mapped to USDA values.

This is a food log, not medical advice. Do not diagnose or prescribe.

## When to use

- User types `/calc-nutrition` (or `/calc-nutrition/`) and lists foods.
- User asks to total today’s protein, fibre, and calories from a meal list.

If the prompt has **no foods**, ask for the list. Do not silently score the usual daily intake unless they say to use the usual day.

## Targets (from CLAUDE.md)

| Nutrient | Daily target |
| --- | --- |
| Protein | **80–90 g** |
| Fibre | **25 g** |
| Energy | **~2,000–2,400 kcal**, default check **2,200 kcal** |
| Free / added sugars | Prefer **≤ 25–36 g**; must stay **&lt; 10% of that day’s calories** |

Free/added sugars: table sugar, honey, syrups, fruit juice, juice concentrates. Do **not** count intrinsic sugars in whole fruit and vegetables. Lactose in milk and plain yogurt is not free sugar.

## Workflow

1. Parse every food and amount from the user prompt (g, ml, tsp, Tbsp, cup, piece, handful).
2. Convert household measures to grams. Use the table below and `CLAUDE.md` assumptions for this person’s usual foods. If an amount is missing or ambiguous, **ask** (or, if they want a score now, state the assumption and mark the row estimated).
3. Look up each food in **USDA FoodData Central** (`https://fdc.nal.usda.gov`). Prefer Foundation, SR Legacy, or FNDDS. Use Branded Foods when a package is named. Check `references/common-foods.md` first for repeats.
4. Scale per-100 g values to the amount eaten. **Do not invent numbers.** If a nutrient is missing, mark it unavailable — do not treat missing as zero.
5. Write a JSON list of items and run the scaler so totals are not done by hand:

```bash
python3 .cursor/skills/calc-nutrition/scripts/calc_day.py
```

The script reads JSON from stdin. Example:

```json
{
  "items": [
    {
      "name": "Milk, whole",
      "amount": "125 ml",
      "grams": 129,
      "kcal_per_100": 61,
      "protein_per_100": 3.15,
      "fiber_per_100": 0,
      "free_sugar_per_100": 0,
      "source": "FDC 171265"
    }
  ]
}
```

6. Reply with the script’s table (or the same columns if you cannot run it), then a one-line verdict: on track / short fibre / short protein / over energy / over sugar.

Suggest food swaps only when a target is clearly missed or the user asks.

## Household measures

| Measure | Use |
| --- | --- |
| 1 tsp sugar | 4.2 g |
| 1 tsp honey | 7 g |
| 1 Tbsp | 15 ml; nut powder ≈ 8 g |
| 1 cup cooked white rice | 158 g |
| Milk | 1 ml ≈ 1.03 g |
| Medium banana | 118 g |
| Medium orange (edible) | 131 g |
| 1 almond | ≈ 1.23 g (USDA ~23 per oz) |
| 1 medium dosa | 80 g (FDC 2708347) |
| Homemade chapati | ≈ 40 g; USDA commercial piece 68 g |

Chia **gel**: 2 Tbsp gel ≈ 3 g dry seed (about 1:9 soak). If they soaked 2 Tbsp **seeds**, use ~20 g dry.

Dhal given as a gram weight: treat as **uncooked** unless they say cooked.

Night staple: 3 dosa **or** 4 chapati, not both, unless they list both.

## Output

Always use this table:

| Food | Amount | kcal | protein_g | fibre_g | free/added sugars_g | source (FDC ID) |
| Totals | | | | | | |
| Target | | ~2,200 | 80–90 | 25 | prefer ≤ 25–36 | |
| Remaining | | | | | | |

Cite the FDC food name and ID on every row. Label estimated amounts.

Keep the reply short after the table: remaining protein / fibre / kcal, then the verdict.
