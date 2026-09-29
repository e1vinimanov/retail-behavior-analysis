"""Validate aggregate exports, calculate rates and save the conversion chart.
Run from any directory: python /path/to/scripts/analyze_conversion.py
"""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

project_folder = Path(__file__).resolve().parents[1]
data_folder = project_folder / "data" / "processed"
windows = pd.read_csv(data_folder / "conversion_windows.csv")
repeat = pd.read_csv(data_folder / "monthly_repeat_purchase.csv")
cart = pd.read_csv(data_folder / "monthly_cart_conversion_7d.csv")

# Verify the saved snapshot before producing charts.
assert len(windows) == 1
assert len(repeat) == 6 and len(cart) == 6
assert repeat["cohort_month"].is_unique and cart["cart_month"].is_unique
assert repeat["eligible_customers"].sum() == 733827
assert repeat["returned_within_30_days"].sum() == 103012
assert cart["eligible_pairs"].sum() == 5385794
assert cart["converted_pairs"].sum() == 1058066
s = windows.iloc[0]
assert s["eligible_pairs"] == cart["eligible_pairs"].sum()
assert s["converted_7d"] == cart["converted_pairs"].sum()
assert 0 <= s["converted_1d"] <= s["converted_3d"] <= s["converted_7d"] <= s["eligible_pairs"]
for frame, numerator, denominator, rate in [
    (repeat, "returned_within_30_days", "eligible_customers", "return_percentage"),
    (cart, "converted_pairs", "eligible_pairs", "conversion_pct"),
]:
    assert not frame.isna().any().any()
    assert (frame[denominator] > 0).all()
    assert (frame[numerator] >= 0).all()
    assert (frame[numerator] <= frame[denominator]).all()
    expected = (100 * frame[numerator] / frame[denominator]).round(2)
    assert ((expected - frame[rate]).abs() < 0.001).all()

summary = pd.DataFrame({
    "window_days": [1, 3, 7],
    "converted_pairs": [int(s["converted_1d"]), int(s["converted_3d"]), int(s["converted_7d"])],
})
summary["conversion_pct"] = (100 * summary["converted_pairs"] / s["eligible_pairs"]).round(2)
summary.to_csv(data_folder / "conversion_summary.csv", index=False)
print(summary.to_string(index=False))
print(f"Overall 30-day repeat rate: {100 * repeat.returned_within_30_days.sum() / repeat.eligible_customers.sum():.2f}%")
print(f"Share of seven-day conversions within one day: {100 * s.converted_1d / s.converted_7d:.2f}%")

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(["Within 1 day", "Within 3 days", "Within 7 days"], summary["conversion_pct"], color="#198577")
ax.bar_label(bars, fmt="%.2f%%", padding=5)
ax.set_ylim(0, 25)
ax.set_ylabel("Eligible customer-product pairs converted (%)")
ax.set_title("Cart-to-purchase conversion by observation window")
ax.spines[["top", "right"]].set_visible(False)
fig.text(0.5, 0.02, f"Same {int(s.eligible_pairs):,} eligible pairs in every window. Counts are cumulative.", ha="center", fontsize=9)
fig.tight_layout(rect=[0, 0.06, 1, 1])
figures = project_folder / "reports" / "figures"
figures.mkdir(parents=True, exist_ok=True)
fig.savefig(figures / "conversion_windows.png", dpi=200, bbox_inches="tight")
plt.close(fig)
print("Aggregate validation passed. CSV and chart saved.")
