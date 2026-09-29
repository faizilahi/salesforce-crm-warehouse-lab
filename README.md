# Bulk API Watermark and Duplicate Opportunities

[Faiz Elahi](https://www.linkedin.com/in/faizilahi) — [pendataco.com](https://pendataco.com) — [github.com/faizilahi](https://github.com/faizilahi)

Synthetic data only. No vendor-customer employment claim.

A Salesforce Bulk API extract into the warehouse used `SystemModstamp` as a
watermark. After a backfill, the watermark jumped forward and skipped **41**
opportunities updated in the gap. Separately, a duplicate rule on
`(account_id, name, close_date)` was not applied in the warehouse merge, so
pipeline dollars were double-counted.

## The watermark

High-water `2024-07-18T14:02:11Z` was advanced to `2024-07-19T09:00:00Z` after
a historical load, skipping mid-gap updates. `src/watermark.py` detects the gap
and replays it.

## The duplicate rule

Natural key `(account_id, opportunity_name, close_date)` — warehouse had **28**
duplicate pairs before dedupe.

## The pipeline number

| Metric | Amount |
|--------|--------|
| Raw extracted open pipeline | $17,267,463 |
| After gap replay | $17,267,463 |
| After duplicate collapse | **$15,598,010.80** |

```powershell
pip install -r requirements.txt
python scripts/generate_synthetic_data.py
python src/run_crm_load.py
```
