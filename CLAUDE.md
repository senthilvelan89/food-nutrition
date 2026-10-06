# food-nutrition — project prompts

This is the project-level prompt file (`CLAUDE.md`). Cursor and Claude Code load it automatically for work in this repository.

Use it as standing context, and treat the **Common prompts** section as reusable task instructions. Paste a prompt into chat, or say which one to follow (for example, “follow *Add a food*”).

## Project

`food-nutrition` helps people look up foods and understand calories, macros, micronutrients, and serving sizes so they can make informed food choices.

This is not medical software. Do not diagnose, prescribe, or present nutrition information as medical advice.

## Standing instructions

- Prefer small, focused changes. Match existing style once a stack exists.
- Do not invent nutrition numbers. Use a documented source (USDA FoodData Central, labeled product data, or project fixtures) and record that source next to the values.
- Treat nutrition math as business-critical. Calories, macros, serving sizes, and unit conversions must be explicit and testable.
- Keep units and serving sizes visible in UI and in data models. Never assume “one serving” without defining it.
- Prefer official or labeled nutrient names (`energy_kcal`, `protein_g`, `carbohydrate_g`, `fat_g`, `fiber_g`, `sodium_mg`) over vague labels like “carbs” in storage and APIs.
- When a requested nutrient is missing, say it is unavailable. Do not fill gaps with estimates unless the user explicitly asks for an estimate, and then label it as estimated.
- Keep user-facing copy plain and specific. Avoid diet-culture language and unsourced health claims.
- After changing calculation or data-mapping code, add or update tests for the numeric behavior.

## Stack

Not established yet. When the first implementation lands, update this section with language, framework, data source, and how to install, run, and test.

Until then:

- Choose widely used, well-documented tools.
- Keep the first version small: food search, nutrient display, serving-size conversion.
- Record new project conventions here as they appear.

## Common prompts

### Add a food

```text
Add a food (or ingredient) to food-nutrition.

Include a stable id, display name, brand if any, serving size with unit, and sourced nutrient values for energy, protein, carbohydrate, fat, fiber, and sodium.

Do not invent numbers. Cite the data source. If a nutrient is missing, store it as unavailable rather than guessing.

Show how the food will be looked up and displayed, and add tests for serving-size scaling.
```

### Look up nutrition facts

```text
Look up nutrition facts for the given food or product in this project.

Return values per stated serving and per 100 g (or 100 ml) when both can be derived honestly.

List the source for every number. If the food is ambiguous, ask for a clarifying match instead of picking silently.
```

### Calculate a meal or recipe

```text
Calculate combined nutrition for a meal or recipe from its ingredients and amounts.

Scale each ingredient from its source serving to the amount used. Sum energy and macros. Preserve units.

Call out ingredients with missing data instead of treating missing values as zero. Show the per-serving result using the recipe’s yield.
```

### Review nutrition math

```text
Review nutrition calculation and unit-conversion code in this change.

Check serving-size scaling, unit conversions, rounding, and whether missing nutrients are handled explicitly.

Flag invented values, silent zero-fills, and UI that omits serving size. Add or update tests for any bug you fix.
```

### Import or map nutrient data

```text
Map an external nutrition dataset (for example USDA FoodData Central) into this project’s food model.

Document field mappings, units, and identifiers. Preserve source ids so values can be refreshed later.

Do not reshape numbers beyond unit conversion. Add fixture-based tests for a few representative foods.
```

### Scaffold the first vertical slice

```text
Scaffold the smallest useful food-nutrition slice: search or select a food, show sourced nutrition facts, and convert between serving sizes.

Keep the architecture simple and testable. Record the stack, data source, and run/test commands in CLAUDE.md when you add them.

Do not add diet plans, trackers, or accounts until the nutrition core works.
```
