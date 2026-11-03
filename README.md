# FIN 43900 — Lab 19: Legend Panel

Three independent investor skills (Buffett, Graham, Burry) examine the **same five annual SEC EDGAR 10-K facts**. Python calculates everything; the skills use printed facts to write judgment memos. No FAskills installation, paid API, market prices, or estimated missing figures.

## Run

```bash
python -m pip install -r requirements.txt
```

Set the SEC-mandated identifying User-Agent **using your own actual name and email**:

- PowerShell: `$env:SEC_USER_AGENT="Your Name your-email@school.edu"`
- macOS/Linux: `export SEC_USER_AGENT="Your Name your-email@school.edu"`

```bash
python panel.py COST
python panel.py COST --graham-threshold 1.0
python panel.py NVDA
python -m streamlit run app.py
python -m unittest discover -s tests -v
```

The Streamlit app defaults to **COST**, displays both the original Lab 18 five-year chart and table, eight checks in a panel table, the three investor verdicts and editable memos side by side, and a number audit across **all** memos. The 1.0 Graham-threshold probe is available in the app as a control. To test the audit, type an unsupported `40.0%` into any memo; it should flag that investor **and** the whole panel, and disable saving.

## Known-answer verification

The instructor's COST reference values imply: **Buffett 3/3 pass; Graham 2/3 pass (current ratio 1.06 < 2.0); Burry 2/2 pass (latest liabilities/equity 1.49)**. The unit tests check the five published annual ratios and the rule outputs using **test fixtures only**. The production script fetches live values from SEC EDGAR; it does not embed instructor reference numbers.

Graham's **threshold probe**: lowering the requirement from **2.0 to 1.0** makes the COST current-ratio check pass. I **retain 2.0** because Graham's defensive liquidity screen should not be weakened just to improve an outcome (also recorded under his memo).

## Project 2 fund company

My Lab 15 Project 2 uses **SGOV, BND and VT** ([prior work](https://github.com/llindali/lab15/blob/main/README.md)). **NVDA** is the largest position inside **VT**, according to [Vanguard's holdings as of 2026-09-30](https://advisors.vanguard.com/investments/products/vt/vanguard-total-world-stock-etf). Run `python panel.py NVDA` and enter `NVDA` in the app to obtain its actual five-year checks; the three agent skills then write NVDA-specific memos from those printed results. **Do not use COST values for NVDA.** If no actual SEC data can be retrieved, leave its metrics unknown and document that rather than fabricate a run.

## Panel decision

**Only with a condition:** I would use the panel to screen Project 2 companies **only after validating each SEC-sourced number and investigating disagreements, unknown values and company-specific qualitative risks**; a coded screen cannot establish fair value or replace financial-statement diligence.

## Deliverable files

- [`panel.py`](panel.py) — EDGAR fetch, same-facts table, Buffett/Graham/Burry checks and numeric memo audit.
- [`app.py`](app.py) — three-column panel, original chart, editable memos and unsupported-number flag.
- [Buffett skill](.agents/skills/buffett-investor/SKILL.md), [Graham skill](.agents/skills/ben-graham/SKILL.md), [Burry skill](.agents/skills/michael-burry/SKILL.md).
- [`memos/COST_buffett.md`](memos/COST_buffett.md), [`memos/COST_graham.md`](memos/COST_graham.md), [`memos/COST_burry.md`](memos/COST_burry.md).
- [`tests/test_panel.py`](tests/test_panel.py) — COST reference-value rules, honest gaps, threshold probe, and memo-number flag.

The partner oral explanations, classroom bull/bear exchange, and Brightspace checkout are intentionally left for class. **Live EDGAR verification still requires your real SEC User-Agent.**

[Professor's Lab 19 instructions](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-11/lab-19-legend-panel.md).

