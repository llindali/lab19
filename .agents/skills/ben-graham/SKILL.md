---
name: ben-graham
description: Use when screening a company's five annual SEC EDGAR 10-K fiscal periods for Graham-style balance-sheet safety and earnings stability, with code-produced checks and a conservative business memo.
---

# Benjamin Graham — defensive financial condition

Source philosophy: [FAskills Benjamin Graham](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/ben_graham.md). Use Graham's defensive financial-condition and earnings-stability emphasis; do not install FAskills or import its paid feeds and price-dependent analyses.

1. Run `python panel.py TICKER` after configuring `SEC_USER_AGENT` with your actual name and email.
2. In `panel.py`, `graham_checks` calculates **three** checks on the shared 10-K data: latest current assets / current liabilities >= **2.0**; net income > 0 in **every** year; final net income > first-year net income. Missing inputs give **not known**. All calculations occur in code, not in the memo.
3. Write `memos/TICKER_graham.md` using only values the script printed and a Graham-inspired conservative assessment. Set bold `Verdict: OWN THE BUSINESS`, `WATCH`, or `PASS` (quality, **not stock price**). Show a non-passing liquidity screen plainly even if earnings improved. Don't invent margins of safety, price multiples, or valuations.
4. **Threshold probe:** run `python panel.py COST --graham-threshold 1.0` (or change the app's Graham threshold to 1.0). COST's current-ratio check should change from **fail** at default **2.0** to **pass** at **1.0**, with other checks unchanged. Put a line below the Graham memo stating the retained threshold and why. Default/retained threshold: **2.0**, for Graham's strict defensive liquidity test.
5. Validate the memo using the app's audit: every number in the memo must have appeared in `panel.py`'s printed output. Keep missing raw facts as **not found**, computed unknowns as **not known**.

