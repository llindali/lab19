"""Lab 19: keyless SEC EDGAR 10-K facts shared by three deterministic investor screens."""
import argparse
import os
import re
from datetime import date

import requests

TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
TAGS = {
    "revenue": ("RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues"),
    "net_income": ("NetIncomeLoss",),
    "operating_cash_flow": ("NetCashProvidedByUsedInOperatingActivities",),
    "capital_spending": ("PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets"),
    "equity": ("StockholdersEquity",),
    "liabilities": ("Liabilities",),
    "current_assets": ("AssetsCurrent",),
    "current_liabilities": ("LiabilitiesCurrent",),
}
INSTANT = {"equity", "liabilities", "current_assets", "current_liabilities"}
INVESTORS = ("Buffett", "Graham", "Burry")
NUMBER = re.compile(r"(?<!\d)[+-]?\d[\d,]*(?:\.\d+)?%?(?!\d)")


def sec_session():
    agent = os.getenv("SEC_USER_AGENT", "").strip()
    if not re.search(r"\S+\s+\S+@\S+\.\S+", agent):
        raise ValueError("Set SEC_USER_AGENT to your actual name and email before using EDGAR.")
    session = requests.Session()
    session.headers.update({"User-Agent": agent, "Accept-Encoding": "gzip, deflate"})
    return session


def fetch_company(ticker, session=None):
    session = session or sec_session()
    response = session.get(TICKERS_URL, timeout=30)
    response.raise_for_status()
    matches = response.json().values()
    match = next((item for item in matches if item["ticker"].upper() == ticker.upper()), None)
    if match is None:
        raise ValueError(f"Ticker {ticker!r} was not in SEC company_tickers.json")
    response = session.get(FACTS_URL.format(cik=int(match["cik_str"])), timeout=30)
    response.raise_for_status()
    return response.json()


def valid_fact(item, annual):
    if item.get("form") != "10-K" or "val" not in item or "end" not in item:
        return False
    if not annual:
        return "start" not in item
    try:
        days = (date.fromisoformat(item["end"]) - date.fromisoformat(item["start"])).days
    except (KeyError, TypeError, ValueError):
        return False
    return 330 <= days <= 380  # full fiscal year, including 53-week years


def choose(companyfacts, tags, end, annual):
    """Tag fallback order first, latest filed 10-K observation for that year second."""
    facts = companyfacts.get("facts", {}).get("us-gaap", {})
    for tag in tags:
        items = facts.get(tag, {}).get("units", {}).get("USD", [])
        choices = [x for x in items if valid_fact(x, annual) and x["end"] == end]
        if choices:
            item = max(choices, key=lambda x: (x.get("filed", ""), x.get("accn", "")))
            return {"value": item["val"], "tag": tag, "filed": item.get("filed")}
    return {"value": None, "tag": "not found", "filed": None}


def metric(row, key):
    return row["metrics"][key]["value"]


def check_all(values, predicate):
    """A known violation fails; otherwise any unknown makes outcome not known."""
    if any(x is not None and not predicate(x) for x in values):
        return "fail"
    return "not known" if any(x is None for x in values) else "pass"


def check_pair(left, right, predicate):
    if left is None or right is None:
        return "not known"
    return "pass" if predicate(left, right) else "fail"


def buffett_checks(rows):
    roes = [metric(r, "roe") for r in rows]
    owners = [metric(r, "owner_earnings") for r in rows]
    return {
        "ROE >= 15% in every year": check_all(roes, lambda x: x >= 15),
        "Owner earnings positive every year": check_all(owners, lambda x: x > 0),
        "Owner earnings grew, first year to last": check_pair(owners[-1], owners[0], lambda a, b: a > b),
    }


def graham_checks(rows, current_ratio_threshold=2.0):
    """Graham's checks: note the override used only for the threshold probe."""
    incomes = [metric(r, "net_income") for r in rows]
    ratio = metric(rows[-1], "current_ratio")
    return {
        f"Current ratio >= {current_ratio_threshold:.1f}, latest year":
            "not known" if ratio is None else "pass" if ratio >= current_ratio_threshold else "fail",
        "Net income positive every year": check_all(incomes, lambda x: x > 0),
        "Net income grew, first year to last": check_pair(incomes[-1], incomes[0], lambda a, b: a > b),
    }


def burry_checks(rows):
    cash = [metric(r, "operating_cash_flow") for r in rows]
    incomes = [metric(r, "net_income") for r in rows]
    ratios = metric(rows[-1], "liabilities_to_equity")
    return {
        "Operating cash flow >= net income every year":
            check_all([None if a is None or b is None else a - b for a, b in zip(cash, incomes)],
                      lambda x: x >= 0),
        "Liabilities / equity <= 2.0, latest year":
            "not known" if ratios is None else "pass" if ratios <= 2.0 else "fail",
    }


def compute(companyfacts, graham_threshold=2.0):
    """Five 10-K fiscal-year rows, same numerical data for all three investor skills."""
    income = companyfacts.get("facts", {}).get("us-gaap", {}).get("NetIncomeLoss", {}).get("units", {}).get("USD", [])
    year_ends = sorted({x["end"] for x in income if valid_fact(x, True)}, reverse=True)[:5]
    if len(year_ends) != 5:
        raise ValueError(f"Expected 5 annual 10-K periods; found {len(year_ends)}. No guessing.")
    rows = []
    for end in sorted(year_ends):
        facts = {name: choose(companyfacts, tags, end, name not in INSTANT)
                 for name, tags in TAGS.items()}
        ni, eq = facts["net_income"]["value"], facts["equity"]["value"]
        cash, capex = facts["operating_cash_flow"]["value"], facts["capital_spending"]["value"]
        ca, cl = facts["current_assets"]["value"], facts["current_liabilities"]["value"]
        liab = facts["liabilities"]["value"]
        facts["roe"] = {"value": None if ni is None or eq is None or eq <= 0 else ni / eq * 100,
                        "tag": "NetIncomeLoss / StockholdersEquity"}
        facts["owner_earnings"] = {"value": None if cash is None or capex is None else cash - capex,
                                   "tag": f"{facts['operating_cash_flow']['tag']} - {facts['capital_spending']['tag']}"}
        facts["current_ratio"] = {"value": None if ca is None or cl is None or cl <= 0 else ca / cl,
                                   "tag": "AssetsCurrent / LiabilitiesCurrent"}
        facts["liabilities_to_equity"] = {"value": None if liab is None or eq is None or eq <= 0 else liab / eq,
                                          "tag": "Liabilities / StockholdersEquity"}
        rows.append({"fy_end": end, "metrics": facts})
    checks = {
        "Buffett": buffett_checks(rows),
        "Graham": graham_checks(rows, graham_threshold),
        "Burry": burry_checks(rows),
    }
    return {"company": companyfacts.get("entityName", "Unknown company"),
            "rows": rows, "checks": checks, "graham_threshold": graham_threshold}


def formatted(name, value):
    if value is None:
        return "not known" if name in ("roe", "owner_earnings", "current_ratio", "liabilities_to_equity") else "not found"
    if name == "roe":
        return f"{value:.1f}%"
    if name in ("current_ratio", "liabilities_to_equity"):
        return f"{value:.2f}"
    return f"{value / 1_000_000:,.0f}"


def normalize_number(token):
    return token.strip().replace(",", "").replace("%", "").lstrip("+")


def printed_numbers(result):
    """Exactly the numeric tokens in the human-readable computation output."""
    return {normalize_number(t) for t in NUMBER.findall(render(result))}


def unsupported_numbers(memo, result):
    allowed = printed_numbers(result)
    return sorted({token for token in NUMBER.findall(memo)
                   if normalize_number(token) not in allowed})


def render(result):
    output = [f"{result['company']} — SEC EDGAR 10-K | USD millions except ratios and ROE"]
    for row in result["rows"]:
        output.append(f"FY end: {row['fy_end']}")
        for name, item in row["metrics"].items():
            output.append(f"  {name}: {formatted(name, item['value'])} | XBRL: {item['tag']}")
    for investor, checks in result["checks"].items():
        passed = sum(value == "pass" for value in checks.values())
        output.append(f"{investor}: {passed}/{len(checks)} passed")
        for label, status in checks.items():
            output.append(f"  {label}: {status}")
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description="EDGAR 10-K three-investor panel")
    parser.add_argument("ticker", help="Ticker: COST or VT's largest company NVDA")
    parser.add_argument("--graham-threshold", type=float, default=2.0,
                        help="Classroom probe: 2.0 baseline, then try 1.0")
    args = parser.parse_args()
    if args.graham_threshold < 0:
        parser.error("Threshold must be nonnegative")
    print(render(compute(fetch_company(args.ticker), args.graham_threshold)))


if __name__ == "__main__":
    main()

