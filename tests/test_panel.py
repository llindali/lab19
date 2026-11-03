"""Offline unit tests: instructor COST table is fixture data, not production output."""
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from panel import check_all, choose, compute, formatted, unsupported_numbers

YEARS = [
    ("2022-08-28", "2021-08-30", 226954, 5844, 7392, 3891, 20642, 1.02, 2.11),
    ("2023-09-03", "2022-08-29", 242290, 6292, 11068, 4323, 25058, 1.07, 1.75),
    ("2024-09-01", "2023-09-04", 254453, 7367, 11339, 4710, 23622, 0.97, 1.96),
    ("2025-08-31", "2024-09-02", 275235, 8099, 13335, 5498, 29164, 1.03, 1.64),
    ("2026-08-30", "2025-09-01", 303154, 9226, 15817, 6435, 35803, 1.06, 1.49),
]


def item(val, end, start=None, form="10-K", filed="2026-10-01"):
    entry = {"val": val, "end": end, "filed": filed, "form": form}
    if start is not None:
        entry["start"] = start
    return entry


def sample_cost():
    def flow(idx):
        return [item(row[idx] * 1_000_000, row[0], row[1]) for row in YEARS]

    def instant(idx):
        return [item(row[idx] * 1_000_000, row[0]) for row in YEARS]

    metrics = {
        "RevenueFromContractWithCustomerExcludingAssessedTax": flow(2),
        "NetIncomeLoss": flow(3),
        "NetCashProvidedByUsedInOperatingActivities": flow(4),
        "PaymentsToAcquirePropertyPlantAndEquipment": flow(5),
        "StockholdersEquity": instant(6),
        # Synthetic current liabilities chosen solely to reproduce the
        # instructor's ratios. No such assumptions enter the live SEC fetch.
        "LiabilitiesCurrent": [item(100_000_000, row[0]) for row in YEARS],
        "AssetsCurrent": [item(round(row[7] * 100_000_000), row[0]) for row in YEARS],
        "Liabilities": [item(round(row[8] * row[6] * 1_000_000), row[0]) for row in YEARS],
    }
    return {"entityName": "COST fixture", "facts": {"us-gaap": {
        key: {"units": {"USD": value}} for key, value in metrics.items()
    }}}


class PanelTests(unittest.TestCase):
    def test_cost_matches_lab19_all_eight_checks(self):
        result = compute(sample_cost())
        self.assertEqual(list(result["checks"]["Buffett"].values()), ["pass"] * 3)
        self.assertEqual(list(result["checks"]["Graham"].values()), ["fail", "pass", "pass"])
        self.assertEqual(list(result["checks"]["Burry"].values()), ["pass", "pass"])
        for expected, actual in zip(YEARS, result["rows"]):
            self.assertEqual(actual["fy_end"], expected[0])
            self.assertEqual(formatted("current_ratio", actual["metrics"]["current_ratio"]["value"]),
                             f"{expected[7]:.2f}")
            self.assertEqual(formatted("liabilities_to_equity", actual["metrics"]["liabilities_to_equity"]["value"]),
                             f"{expected[8]:.2f}")
            self.assertEqual(formatted("owner_earnings", actual["metrics"]["owner_earnings"]["value"]),
                             f"{expected[4] - expected[5]:,}")
            self.assertEqual(formatted("roe", actual["metrics"]["roe"]["value"]),
                             f"{expected[3] / expected[6] * 100:.1f}%")

    def test_graham_threshold_probe(self):
        self.assertEqual(list(compute(sample_cost(), 1.0)["checks"]["Graham"].values()),
                         ["pass", "pass", "pass"])

    def test_missing_remains_unknown(self):
        fixture = sample_cost()
        facts = fixture["facts"]["us-gaap"]
        del facts["PaymentsToAcquirePropertyPlantAndEquipment"]
        del facts["AssetsCurrent"]
        del facts["Liabilities"]
        result = compute(fixture)
        self.assertEqual(result["checks"]["Buffett"]["Owner earnings positive every year"], "not known")
        self.assertEqual(list(result["checks"]["Graham"].values())[0], "not known")
        self.assertEqual(list(result["checks"]["Burry"].values())[-1], "not known")
        self.assertEqual(result["rows"][0]["metrics"]["capital_spending"]["tag"], "not found")

    def test_nonpositive_equity_means_roe_and_leverage_unknown(self):
        fixture = sample_cost()
        eq = fixture["facts"]["us-gaap"]["StockholdersEquity"]["units"]["USD"]
        eq[-1]["val"] = 0
        result = compute(fixture)
        self.assertEqual(result["checks"]["Buffett"]["ROE >= 15% in every year"], "not known")
        self.assertEqual(list(result["checks"]["Burry"].values())[-1], "not known")

    def test_memo_guard_all_three(self):
        result = compute(sample_cost())
        folder = Path(__file__).resolve().parents[1] / "memos"
        for investor in ("buffett", "graham", "burry"):
            memo = (folder / f"COST_{investor}.md").read_text(encoding="utf-8")
            self.assertEqual(unsupported_numbers(memo, result), [], investor)
        self.assertEqual(unsupported_numbers("I claim ROE 40.0%", result), ["40.0%"])

    def test_latest_filed_10k_wins_and_10q_excluded(self):
        fixture = sample_cost()
        end, start = YEARS[-1][:2]
        income = fixture["facts"]["us-gaap"]["NetIncomeLoss"]["units"]["USD"]
        income += [item(77, end, start, filed="2026-11-01"),
                   item(88, end, start, form="10-Q", filed="2026-12-01")]
        self.assertEqual(choose(fixture, ("NetIncomeLoss",), end, True)["value"], 77)

    def test_known_fail_over_unknown(self):
        self.assertEqual(check_all([None, -1, 2], lambda x: x > 0), "fail")
        self.assertEqual(check_all([None, 2], lambda x: x > 0), "not known")


if __name__ == "__main__":
    unittest.main()

