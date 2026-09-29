# Salesforce CRM Warehouse Lab

**Author:** [Faiz Elahi](https://github.com/faizilahi) (`faizilahi`) · **Type:** EDUCATIONAL LAB · **Synthetic data only**

---

## Educational disclaimer

This is an **educational portfolio lab**. Datasets are **synthetic**. It does **not** claim employment at a customer, hospital, bank, SAP shop, or Oracle estate. No real PHI/PII. No live cloud spend. No API keys required.

---

## Problem statement

Account/Contact/Opportunity syncs produce duplicate funnel counts unless natural-key MERGE and stage mapping are certified.

**Domain focus:** RevOps analytics

---

## Why this tool (Salesforce → warehouse ELT patterns)

| Duplicate opportunities | Natural-key MERGE |
|---|---|
| Stage rename breaks | Mapping seed + accepted values |

---

## Architecture

```mermaid
flowchart LR
  GEN[generate_synthetic_data.py]
  DATA[data/*.csv]
  RUN[run_lab.py]
  OUT[output/*.csv]
  CHART[generate_charts.py]
  IMG[docs/images/*.png]
  GEN --> DATA --> RUN --> OUT
  OUT --> CHART --> IMG
```

See [`docs/architecture.md`](docs/architecture.md).

---

## Dataset dictionary

| File | Notes |
|------|-------|
| `data/opportunity.csv` | Synthetic CRM |
| `seeds/stage_map.csv` | Stage normalization |
| `output/summary.csv` | Funnel |

---

## Prerequisites

- Python 3.10+
- Packages in `requirements.txt`

---

## How to run

```powershell
cd "salesforce-crm-warehouse-lab"
python -m venv .venv
.\\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/generate_synthetic_data.py
python src/run_lab.py
python scripts/generate_charts.py
```

Inspect `output/summary.csv` and `docs/images/primary_metric.png`.

---

## Local vs cloud (honest)

Synthetic Salesforce CSV extracts only. No Salesforce API calls or Fivetran connector.

---

## Results interpretation

Open `output/` CSVs and the PNGs under `docs/images/`. Numbers are synthetic teaching fixtures — use them to explain grain, filters, and control totals, not as real business KPIs.

---

## Limitations

- Stand-in engines (DuckDB/SQLite/pandas) replace paid MPP/warehouses where noted.
- Simplified schemas vs production SAP/Oracle/Hive estates.
- Charts are matplotlib teaching visuals, not vendor BI embeds.

---

## Exercises

1. Break stage names and fix via mapping seed.
2. Deduplicate on AccountId+Name.
3. Add dbt-style accepted_values test.

---

## License / attribution

Educational portfolio content by Faiz Elahi. Synthetic data for teaching only.

