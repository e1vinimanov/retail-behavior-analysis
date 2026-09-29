# Explaining the project in an interview

## A short introduction

“I wanted to practice turning event data into useful marketing questions. I analyzed about 9.86 million retail purchase and cart events using PostgreSQL and Python. I defined eligibility windows so customers had enough time to convert or return, and kept non-converters in the analysis with left joins. One finding was that 92.4% of the conversions observed within seven days happened in the first 24 hours. I would use that to investigate early purchase behavior and design a controlled reminder test, rather than assume reminders would increase sales.”

## Questions to be ready for

**What was one row in your cart analysis?**

A customer-product pair, using its earliest observed cart event. One customer can contribute several pairs. These are not whole carts or orders.

**Why did you use a left join?**

To keep eligible customers or pairs with no qualifying later purchase. An inner join would remove non-converters and bias the denominator.

**Why did you use November 7 and December 1?**

I treated December 7 as the last complete observation day because December 8 was partial. A first purchase by November 7 leaves 30 calendar days of follow-up. A cart timestamp strictly before December 1 leaves seven elapsed days before December 8 begins.

**What does 92.4% mean?**

Of pairs that converted within seven days, 92.4% converted within one day. It is not the conversion rate for all eligible pairs. That one-day rate was 18.15%.

**Why keep duplicate events?**

There was no event ID to prove they were erroneous. The final metrics use distinct purchase days and earliest qualifying events, so exact repeated rows do not change these definitions in the way they would change a raw event count.

**What did Python add?**

PyArrow handled Parquet inspection and validated CSV preparation. pandas reconciled monthly totals and computed aggregate rates. Matplotlib produced the timing chart. PostgreSQL performed the event-level joins and cohort calculations.

**How did you use AI?**

“I used AI as a coach for query review, metric definitions and debugging, and for assistance with Python and presentation code. I ran the SQL, checked the outputs and worked through the interpretation. I am still developing my pandas fluency, and I can explain what the scripts do and where AI helped.”

Use this wording only to the extent it reflects what you can explain. Do not imply you wrote the whole dashboard yourself.

**What would you do with better data?**

Add order IDs, actual revenue and margin, campaign exposures and spending, and more history. For a reminder experiment, randomize at customer level to avoid the same customer appearing in both treatment and control, predefine the outcome and follow-up period, and assess incremental results.

**How is retail data relevant to a B2B marketing role?**

The transferable skills are metric definition, SQL analysis, follow-up windows, validation and communication. The dataset does not establish B2B domain experience or Google Ads experience.
