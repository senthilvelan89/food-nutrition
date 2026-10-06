# food-nutrition — project prompts

This is the project-level prompt file (`CLAUDE.md`). Cursor and Claude Code load it automatically for work in this repository.

Use it as standing context, and treat the **Common prompts** section as reusable task instructions. Paste a prompt into chat, or say which one to follow (for example, “follow *Log today’s food*”).

## Project

Personal food log and nutrition tracker. The user lists foods eaten that day. Look each item up in a standard nutrition chart, scale to the amount eaten, and total **calories, protein, and fibre**. Compare the day to the targets below so the user can stay at a healthy body weight and hit fibre and protein needs without excess sugar.

This is not medical software. Do not diagnose, prescribe, or present nutrition information as medical advice.

## Personal profile and goals

| | |
| --- | --- |
| Weight | 75 kg |
| Height | 175 cm |
| BMI | 24.5 (WHO **normal weight** is 18.5–24.9) |
| Healthy weight for 175 cm | about 56.7–76.3 kg (WHO BMI 18.5–24.9) |
| Goal | **Stay at this healthy weight** (hold ~75 kg; stay below BMI 25 / ~76.3 kg) while hitting daily fibre and protein |

End goal: remain at a healthy / ideal body weight **and** consume the required fibre and protein every day.

### Daily targets

| Nutrient | Daily target | Basis |
| --- | --- | --- |
| Protein | **80–90 g** | User target (~1.1–1.2 g/kg at 75 kg) |
| Fibre | **25 g** | User target (common adult daily fibre goal) |
| Energy | **~2,000–2,400 kcal**, default check **2,200 kcal** | Working maintenance range to hold 75 kg. ~25 kcal/kg sedentary ≈ 1,875; ~30 kcal/kg light–moderate ≈ 2,250. Age, sex, and activity are not set — if weekly weight trends up toward 76 kg, lower energy; if it trends down, raise it. |
| Free / added sugars | **Limit: &lt; 10% of that day’s calories.** At 2,200 kcal that is **&lt; 55 g**. **Prefer ≤ 25–36 g** (~5% of calories / AHA-style cap) | [WHO sugars guideline](https://www.who.int/publications/i/item/9789241549028): free sugars &lt; 10% of energy (strong); &lt; 5% for extra benefit. [Dietary Guidelines for Americans](https://www.dietaryguidelines.gov/) also limit added sugars to &lt; 10% of calories. AHA practical caps: about 36 g/day (most men) or 25 g/day (most women). |

**Free / added sugars** (count toward the cap): sugars added in cooking or processing, plus honey, syrups, fruit juice, and juice concentrates.

**Do not count toward the cap:** intrinsic sugars in whole fresh fruit and vegetables (WHO). Still report total sugars when the chart lists them.

Flag sugar-sweetened drinks, sweets, and juices clearly. Do not treat “optimum sugar” as zero whole fruit.

## How to score a day’s food

When the user lists what they ate:

1. For each food, look up **USDA FoodData Central** (`https://fdc.nal.usda.gov`) as the standard nutrition chart. Prefer Foundation, SR Legacy, or FNDDS entries for generic foods; use Branded Foods when a package/brand is named.
2. Match the closest food and the amount eaten (g, ml, household measure, or pieces). State the match and the serving used. If the food is ambiguous, ask before guessing.
3. Scale calories, protein, fibre, total sugars, and added/free sugars (when available) to that amount. Do **not** invent numbers.
4. Sum the day. Show remaining room vs targets (protein 80–90 g, fibre 25 g, energy ~2,200 kcal, free/added sugars prefer ≤ 25–36 g and must stay &lt; 10% of that day’s calories).
5. Say whether the day supports **holding ~75 kg**, **hitting fibre and protein**, and **keeping sugars in the WHO/DGA band**. Suggest food swaps only when asked or when a target is clearly missed.

If a nutrient is missing from the chart, mark it unavailable. Do not fill with zero or an estimate unless the user asks for an estimate, and then label it estimated.

Cite the FoodData Central food name and FDC ID (or equivalent source) next to each line.

### Daily log output

Use a table:

| Food | Amount | kcal | protein_g | fibre_g | free/added sugars_g | source (FDC ID) |
| Totals | | | | | | |
| Target | | ~2,200 | 80–90 | 25 | prefer ≤ 25–36; max &lt; 10% kcal | |
| Remaining | | | | | | |

Then a short verdict: on track / short fibre / short protein / over energy / over sugar.

## Usual daily intake

Use this as the default day when the user does not list a different menu. Night is **either** 3 dosa **or** 4 chapati with gravy, not both.

| When | Foods |
| --- | --- |
| Morning | 125 ml milk + 2 Tbsp nut powder (almond, walnut, pista) + 1.5 tsp sugar |
| Next | 2–3 tsp Greek yogurt + 2 spoons soaked chia gel + 25 g groundnut + 5 g walnut |
| Mid | 1 medium banana + 1 medium orange |
| Lunch | 1 cup rice + 2 vegetables (150 g each) + some chips as a side |
| Afternoon | 50 g dhal |
| Later | bread sandwich with 3 tsp honey |
| Evening | 100 ml tea + 1 tsp sugar + 20 almonds (not soaked) |
| Night | 3 dosa **or** 4 chapati, with gravy |

### Assumptions when amounts are missing

- Milk: whole, 125 ml ≈ 129 g (FDC 171265).
- Nut powder: 2 Tbsp ≈ 16 g, equal parts almond / walnut / pistachio.
- 1 tsp sugar = 4.2 g (FDC 169655). Greek yogurt 2.5 tsp ≈ 12.5 g plain nonfat (FDC 170894) — a very small amount; confirm if they meant tablespoons.
- Chia gel: 2 Tbsp of prepared gel ≈ 3 g dry chia at ~1:9 soak (FDC 170554). If they soaked 2 Tbsp **seeds**, use ~20 g dry instead.
- Rice: 1 cup cooked white long-grain = 158 g (FDC 168878).
- Vegetables unnamed: 300 g mixed vegetables, cooked (FDC 2710015).
- Chips amount not given: 20 g potato chips as a small side (FDC 170649) — mark estimated.
- Sandwich: 2 slices white bread (~56 g) + 3 tsp honey = 21 g (FDC 169640). Honey counts as free sugar.
- 20 almonds ≈ 24.7 g (FDC 170567; USDA ~23 almonds / oz).
- Dhal 50 g: treat as **uncooked** → about 125 g cooked lentils (FDC 172421). If it was cooked weight, protein and fibre drop.
- Dosa: 3 × medium 80 g (FDC 2708347). Chapati: prefer homemade ~40 g each; USDA commercial piece is 68 g (FDC 171844).
- Gravy amount not given: 150 g mixed vegetables, cooked, as a katori of sabzi/gravy — oil in gravy is unknown.
- Banana medium 118 g (FDC 173944); orange medium 131 g edible (FDC 169097). Fruit sugars are **not** free sugars.

### Typical scored day (USDA-scaled)

| Night choice | kcal | protein_g | fibre_g | free/added sugars_g |
| --- | --- | --- | --- | --- |
| 3 medium dosa + gravy | ~2,280 | ~72 | ~51 | ~28 |
| 4 homemade chapati (~40 g) + gravy | ~2,250 | ~76 | ~55 | ~28 |
| 4 USDA commercial chapati (68 g) + gravy | ~2,590 | ~89 | ~60 | ~28 |
| Target | ~2,200 | 80–90 | 25 | prefer ≤ 25–36 |

Usual pattern: **fibre is met**, **free sugar is in the preferred band** (honey is most of it), **protein is short** on dosa / homemade-chapati nights, **calories sit near maintenance** unless the chapatis are large.

## Standing instructions

- Prefer small, focused changes. Match existing style once a stack exists.
- Do not invent nutrition numbers. Use USDA FoodData Central, labeled product data, or project fixtures, and record that source next to the values.
- Treat nutrition math as business-critical. Calories, protein, fibre, sugars, serving sizes, and unit conversions must be explicit and testable.
- Keep units and serving sizes visible in UI and in data models. Never assume “one serving” without defining it.
- Prefer official or labeled nutrient names (`energy_kcal`, `protein_g`, `carbohydrate_g`, `fat_g`, `fiber_g`, `sugars_g`, `added_sugars_g`, `sodium_mg`) over vague labels in storage and APIs.
- When a requested nutrient is missing, say it is unavailable. Do not fill gaps with estimates unless the user explicitly asks for an estimate, and then label it as estimated.
- Keep user-facing copy plain and specific. Avoid diet-culture language and unsourced health claims.
- After changing calculation or data-mapping code, add or update tests for the numeric behavior.

## Stack

Not established yet. When the first implementation lands, update this section with language, framework, data source, and how to install, run, and test.

Until then:

- Choose widely used, well-documented tools.
- First slice: log foods eaten, look up USDA values, total calories / protein / fibre / sugars, compare to the targets above.
- Record new project conventions here as they appear.

## Common prompts

### Log today’s food

```text
I will list the foods I ate today (and amounts). Look each one up in USDA FoodData Central, scale to the amount I ate, and total calories, protein, fibre, and free/added sugars.

Compare the day to my targets: hold ~75 kg at 175 cm (BMI 24.5); protein 80–90 g; fibre 25 g; energy around 2,200 kcal (2,000–2,400 working range); free/added sugars prefer ≤ 25–36 g and always under 10% of that day’s calories.

Use a table with source/FDC ID per food. Mark missing nutrients as unavailable. Do not invent numbers. End with remaining amounts and a short on-track verdict.
```

### Add a food

```text
Add a food (or ingredient) to food-nutrition.

Include a stable id, display name, brand if any, serving size with unit, and sourced nutrient values for energy, protein, carbohydrate, fat, fibre, sugars, added/free sugars, and sodium.

Do not invent numbers. Cite USDA FoodData Central (or the label). If a nutrient is missing, store it as unavailable rather than guessing.

Show how the food will be looked up and displayed, and add tests for serving-size scaling.
```

### Look up nutrition facts

```text
Look up nutrition facts for the given food or product in USDA FoodData Central (or this project’s food model if it already exists).

Return values per stated serving and per 100 g (or 100 ml) when both can be derived honestly, including calories, protein, fibre, and sugars.

List the source for every number. If the food is ambiguous, ask for a clarifying match instead of picking silently.
```

### Calculate a meal or recipe

```text
Calculate combined nutrition for a meal or recipe from its ingredients and amounts.

Scale each ingredient from its source serving to the amount used. Sum energy, protein, fibre, and free/added sugars. Preserve units.

Call out ingredients with missing data instead of treating missing values as zero. Show the per-serving result using the recipe’s yield, and how it counts toward the daily 80–90 g protein / 25 g fibre / ~2,200 kcal / sugar-cap targets.
```

### Review nutrition math

```text
Review nutrition calculation and unit-conversion code in this change.

Check serving-size scaling, unit conversions, rounding, and whether missing nutrients are handled explicitly.

Flag invented values, silent zero-fills, and UI that omits serving size. Add or update tests for any bug you fix.
```

### Import or map nutrient data

```text
Map USDA FoodData Central (or another standard chart) into this project’s food model.

Document field mappings, units, and identifiers. Preserve FDC ids so values can be refreshed later.

Do not reshape numbers beyond unit conversion. Add fixture-based tests for a few representative foods covering calories, protein, fibre, and sugars.
```

### Scaffold the first vertical slice

```text
Scaffold the smallest useful food-nutrition slice: the user enters foods eaten today, values are looked up from USDA FoodData Central, and the day is scored against calories (~2,200), protein (80–90 g), fibre (25 g), and free/added sugars (prefer ≤ 25–36 g, max < 10% of energy) so they can stay near 75 kg at 175 cm.

Keep the architecture simple and testable. Record the stack, data source, and run/test commands in CLAUDE.md when you add them.
```
