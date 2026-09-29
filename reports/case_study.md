# When do retail customers convert and return?

## Question

I analyzed purchasing and cart behavior to establish a baseline for conversion timing and repeat purchasing. The aim was to identify useful follow-up questions for lifecycle marketing, without treating observed behavior as proof of campaign impact.

## Data and method

The project used 2,318,502 purchase events and 7,541,117 cart events from the Synerise dataset, covering June–December 2022. Python preparation preserved the original records and checked timestamp parsing, nulls, duplicates and CSV round-trip equality.

In PostgreSQL, I used CTEs and left joins to preserve eligible customers and customer-product pairs even when no later purchase was found. Eligibility cutoffs provided a common follow-up window. pandas then checked aggregate totals and calculated conversion rates, with Matplotlib used for the timing chart.

## Findings

Of 733,827 eligible buyers, 103,012 purchased on a later day within 30 days of their first observed purchase, a rate of **14.04%**.

Of 5,385,794 eligible customer-product pairs, 1,058,066 had a matching purchase within seven days of their first observed cart event, a rate of **19.65%**. Of those converted pairs, **92.40%** converted within the first 24 hours.

September had the highest monthly cart conversion rate at **21.03%**. November's rate was lower at **19.45%**, but its larger eligible population produced **266,005** converted pairs, the highest monthly count. A rate decline therefore did not mean fewer conversions.

## Recommendation

Investigate the first 24 hours after cart addition, including potential checkout friction and differences in customer intent. Review whether product or customer mix helps explain the monthly differences.

If a reminder campaign is considered, use a randomized holdout to measure incremental conversion and monitor customer experience. The observed conversion timing alone cannot identify the best reminder timing or establish that reminders will increase sales.

## Limits

The analysis has no campaign spend, monetary revenue, order IDs or randomized treatment groups. Its cart metric counts customer-product pairs, not whole carts. Its repeat metric starts with a first observed purchase, not a verified new customer. Partial months and the assumed final complete observation day are documented in the README.

## Outcome

The deliverable is a documented set of SQL analyses, validated aggregate outputs, a Python chart and an offline dashboard. It establishes a measurement baseline and proposes investigations. It does not claim a realized increase in conversion or revenue.
