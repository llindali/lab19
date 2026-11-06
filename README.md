# FIN 43900 — Lab 19: Buffett / Cathie Wood / Burry (customized)

**Rubric warning:** The published assignment explicitly asks for Benjamin Graham and a current-ratio probe. This requested Cathie Wood substitution is **not** the professor's original rubric; seek approval if this is to be graded against the original assignment.

The three skills read the **same five annual SEC EDGAR 10-K facts**, with all checks implemented in Python. Numbers come from code, missing data stays missing, and memo numbers are audited across all three investor memos. This project does not use stock prices, paid APIs, or install FAskills.

## Run

```bash
python -m pip install -r requirements.txt
# Set SEC_USER_AGENT to your REAL name and email, e.g. "Your Name you@example.com"
python panel.py COST
python panel.py NVDA
python -m streamlit run app.py
python -m unittest discover -s tests -v
```

`SEC_USER_AGENT` must be set in your terminal's environment before making SEC requests. For PowerShell: `$env:SEC_USER_AGENT="Your Name you@example.com"`. Never commit personal email credentials. SEC calls have not been verified live in this workspace.

## Skills and checks

- [Buffett](.agents/skills/buffett-investor/SKILL.md): ROE at least 15% each year; owner earnings positive each year; owner earnings grew from first to last.
- [Cathie Wood-inspired](.agents/skills/cathie-wood/SKILL.md): revenue grew first-to-last; latest year-over-year revenue growth at least 15%; operating cash flow grew first-to-last. **The 15% threshold is a user-selected classroom design choice, not ARK policy.** The app lets you probe it at 10%.
- [Burry](.agents/skills/michael-burry/SKILL.md): operating cash flow at least net income every year; latest liabilities/equity no more than 2.

ARK's actual process involves innovation identification, technology cost curves, market adoption, five-year forecasts and valuation, none of which can be established from these SEC financial metrics alone. [Source: ARK Invest](https://www.ark-invest.com/investment-process).

## Costco known-answer fixture (offline)

The tests use the instructor's COST 2022–2026 values as **synthetic test fixtures**, never as a substitute for live SEC retrieval. Expected checks: Buffett 3/3, Wood 2/3 (latest revenue growth fails the 15% classroom proxy), Burry 2/2. The [three memos](memos) use only printed script values. A memo with a numerical claim not printed by the script is flagged in the Streamlit interface. The latest growth threshold can be lowered to 10% for a sensitivity demonstration; this changes the Wood-inspired verdict without changing the underlying facts.

## Project 2 company

The selected fund is VT, whose largest holding was identified as NVDA in the earlier Lab 19 work. Run `python panel.py NVDA` and the app to produce its actual SEC panel. **NVDA live EDGAR numbers and company-specific memos have not been generated or verified here.** Missing values remain `not found` / `not known`. No claims about the company are fabricated.

## Submission / class-only work

Files: [panel.py](panel.py), [app.py](app.py), [requirements.txt](requirements.txt), [tests/test_panel.py](tests/test_panel.py), three skill `SKILL.md` files, and three COST memos. Partner explanation, bull/bear exchange, personal reflection, Brightspace quiz and instructor permission for the substitution remain for class. This is a business-quality exercise, not investment advice.
