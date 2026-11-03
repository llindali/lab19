---
name: buffett-investor
description: Use when deciding if a company's five annual 10-K financial results meet Buffett-style business-quality checks, using SEC EDGAR values computed by the Lab 19 panel script.
---

# Buffett — quality and owner earnings

Source philosophy: [FAskills Warren Buffett](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/warren_buffett.md). Use its investing principles, **not** its paid sources or stock-price, valuation, and holdings instructions.

1. Run `python panel.py TICKER` from the project root, with `SEC_USER_AGENT` containing your real name and email. No code-generated numbers may be revised by AI.
2. Review the **Buffett** checks produced by `buffett_checks` in `panel.py`: ROE >= 15% in *each* of the five annual 10-K periods; owner earnings (OCF minus capex) positive *each* year; last owner earnings > first. Explain which pass, fail or are **not known**.
3. Write `memos/TICKER_buffett.md`, with a bold `Verdict: OWN THE BUSINESS`, `WATCH`, or `PASS` line. A positive quality screen can justify OWN THE BUSINESS as a *business-quality* opinion, never a stock purchase call. Evaluate predictable earnings and cash production while explicitly distinguishing proved facts from unproved moats and management quality.
4. Include only numeric facts the script **prints**; use no market prices, projections, inferred data or fabricated facts. Missing underlying tags are **not found**; dependent metrics and checks are **not known**.
5. Validate all numeric tokens through the app's number audit: `streamlit run app.py`. End with a one-line confidence/condition for trusting the verdict.

Caveat: owner earnings = operating cash flow - **total** capital spending is this lab's teaching proxy, not Buffett's refined maintenance-capex concept. The 15% test is a classroom threshold, not a claim about his actual binding rules.

