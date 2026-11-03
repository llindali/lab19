---
name: michael-burry
description: Use when stress-testing a business with Burry-style cash-versus-earnings quality and leverage checks on five 10-K fiscal years, and drafting a skeptical evidence-limited business memo.
---

# Michael Burry — earnings quality and balance-sheet forensics

Source philosophy: [FAskills Michael Burry](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/michael_burry.md). This lab uses his cash-conversion skepticism and balance-sheet scrutiny, not the paid FAskills sources, price calls, or speculative forensic allegations.

1. Run `python panel.py TICKER` after setting the SEC `SEC_USER_AGENT` to your real name and email.
2. Inspect `burry_checks` in `panel.py`: cash flow from operations >= net income for **every** annual 10-K period; and latest liabilities / equity <= **2.0**. Nonpositive or missing equity means the leverage ratio is **not known**. A missing cash-flow or income year makes that check **not known** unless an observed year already proves a failure.
3. Write `memos/TICKER_burry.md` using **only** numbers printed by the script. Give a bold `Verdict: OWN THE BUSINESS`, `WATCH`, or `PASS`. Discuss cash conversion, liabilities and what cannot be determined without reading footnotes. Passing both simple checks is **not** evidence that accounting is clean or there are hidden problems.
4. No stock price, valuation, forward targets, invented claims of fraud, or guessed missing values. Audit memo numbers in the Streamlit app and state whether you trust the limited verdict.

