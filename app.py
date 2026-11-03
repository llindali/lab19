"""Lab 19 — side-by-side investor skills on one audited EDGAR data set."""
import re
from pathlib import Path

import pandas as pd
import streamlit as st

from panel import compute, fetch_company, formatted, render, unsupported_numbers

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title="Legend Investor Panel", layout="wide")
st.title("Legend Investor Panel")
st.caption("Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.")

ticker = st.text_input("US-listed company ticker", value="COST").strip().upper()
graham_threshold = st.number_input("Graham current-ratio threshold (try 1.0 for the probe)",
                                    min_value=0.0, value=2.0, step=0.1, format="%.1f")
if not re.fullmatch(r"[A-Z][A-Z0-9.-]{0,9}", ticker):
    st.error("Enter a ticker such as COST or NVDA.")
    st.stop()


@st.cache_data(ttl=3600, show_spinner=False)
def load_facts(symbol):
    return fetch_company(symbol)


try:
    result = compute(load_facts(ticker), graham_threshold)
except Exception as exc:
    st.error(f"Unable to load verified 10-K data: {exc}")
    st.stop()

st.subheader(f"{result['company']} ({ticker})")
rows = []
for r in result["rows"]:
    line = {"Fiscal year end": r["fy_end"]}
    for name, item in r["metrics"].items():
        line[name.replace("_", " ").title()] = formatted(name, item["value"])
    rows.append(line)
st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

chart = pd.DataFrame([
    {"Fiscal year end": r["fy_end"],
     "Net income": (r["metrics"]["net_income"]["value"] or 0) / 1_000_000
         if r["metrics"]["net_income"]["value"] is not None else None,
     "Owner earnings": r["metrics"]["owner_earnings"]["value"] / 1_000_000
         if r["metrics"]["owner_earnings"]["value"] is not None else None}
    for r in result["rows"]
]).set_index("Fiscal year end")
st.subheader("Net income vs. owner earnings (USD millions)")
st.line_chart(chart)

st.subheader("Investor × check: one shared set of 10-K facts")
checks = []
for investor, tests in result["checks"].items():
    for name, status in tests.items():
        checks.append({"Investor": investor, "Check": name, "Result": status})
st.dataframe(pd.DataFrame(checks), hide_index=True, use_container_width=True)

st.subheader("Three investor memos")
all_flags = {}
cols = st.columns(3)
for col, investor in zip(cols, result["checks"]):
    with col:
        file = ROOT / "memos" / f"{ticker}_{investor.lower()}.md"
        if file.exists():
            original = file.read_text(encoding="utf-8")
        else:
            original = (f"# {ticker} — {investor}-inspired business memo\n\n"
                        "**Verdict: WATCH (memo pending)**\n\n"
                        "Run this investor's skill on the verified figures above to write "
                        "an independent, evidence-based business assessment. "
                        "Missing evidence must stay not known.\n")
        written = st.text_area(f"{investor} memo", value=original, height=330,
                               key=f"{ticker}_{investor}_memo")
        flagged = unsupported_numbers(written, result)
        all_flags[investor] = flagged
        status = re.search(r"\*\*Verdict:\s*(OWN THE BUSINESS|OWN|WATCH|PASS)\b", written, re.I)
        st.write(f"**Verdict:** {status.group(1).upper() if status else 'not stated'}")
        passed = sum(v == "pass" for v in result["checks"][investor].values())
        st.write(f"**Checks:** {passed}/{len(result['checks'][investor])} pass")
        if flagged:
            st.error("Numbers not printed by script: " + ", ".join(flagged))
        else:
            st.success("Number audit passed")
        st.markdown(written)
        if st.button(f"Save {investor} memo", key=f"save_{ticker}_{investor}",
                     disabled=bool(flagged)):
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text(written, encoding="utf-8")
            st.success(f"Saved {file.relative_to(ROOT)}")

if any(all_flags.values()):
    st.error("Panel-wide memo audit failed: " + "; ".join(
        f"{name}: {', '.join(nums)}" for name, nums in all_flags.items() if nums))
else:
    st.success("Panel-wide memo audit passed for all three memos")

with st.expander("View exact printed numbers and XBRL tags used by the memos"):
    st.code(render(result), language="text")

