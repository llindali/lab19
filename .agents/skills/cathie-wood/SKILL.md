---
name: cathie-wood
summary: Innovation-growth-inspired business screen using five annual SEC EDGAR 10-K periods and a clearly labeled classroom proxy.
description: Analyze 10-K historical revenue and operating cash flow through a Cathie Wood-inspired growth lens without inventing forward-looking innovation evidence.
---

# Cathie Wood-inspired growth skill (classroom adaptation)

Read ARK Invest's [investment process](https://www.ark-invest.com/investment-process). ARK uses disruptive innovation research, technology cost curves, market adoption and five-year company forecasts. **The three checks below are invented classroom proxies, not ARK criteria or a prediction of Wood's real investments.**

Run `python panel.py COST` (requires a real identifying `SEC_USER_AGENT`) and read the printed five annual 10-K rows. Use exactly these three coded checks from `wood_checks`:

1. Revenue grew from first to last fiscal year.
2. Latest year-on-year revenue growth at least 15% (adjustable educational threshold).
3. Operating cash flow grew from first to last fiscal year.

A missing input yields **not known**, not a fabricated figure. The skill must write a `memos/TICKER_wood.md` business memo with **OWN THE BUSINESS / WATCH / PASS** and use only printed numbers. Distinguish *growth supported by historical filings* from *innovation leadership not established*. Do not claim to know TAM, unit adoption, cost curves, valuation, share price, or ARK's portfolio decision without separately sourced and computed evidence. Do not invent an ARK endorsement. The memo should explain a bull and bear interpretation and when more evidence is required. All numeric claims must pass `unsupported_numbers`.

This skill compares alongside Buffett and Burry using **the same** SEC facts. No paid API or external FAskills installation is needed.
