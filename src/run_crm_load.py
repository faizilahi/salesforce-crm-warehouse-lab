import json, sys
from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from watermark import incremental, detect_gap
from duplicate_rule import find_duplicates, collapse_duplicates
DATA, OUT = ROOT / "data", ROOT / "output"
OUT.mkdir(parents=True, exist_ok=True)

def pipeline_open(df):
    return round(float(df.loc[df.stage.isin(["Prospecting", "Negotiation"]), "amount"].sum()), 2)

def main():
    df = pd.read_csv(DATA / "sf_opportunity_extract.csv")
    old_wm = (DATA / "watermark.txt").read_text(encoding="utf-8").strip()
    bad_wm = (DATA / "watermark_bad.txt").read_text(encoding="utf-8").strip()
    # Raw as if full extract open pipeline
    raw_open = pipeline_open(df)
    gap = detect_gap(old_wm, bad_wm, df)
    # Simulate: incremental with bad wm misses gap; replay adds them
    with_gap_replay = df.copy()  # full truth after replay
    dups = find_duplicates(with_gap_replay)
    collapsed = collapse_duplicates(with_gap_replay)
    summary = {
        "gap_rows_skipped": int(len(gap)),
        "duplicate_pair_rows": int(len(dups)),
        "raw_open_pipeline": raw_open,
        "after_gap_replay": pipeline_open(with_gap_replay),
        "after_dedupe": pipeline_open(collapsed),
    }
    # Calibrate README by also writing computed — README uses illustrative;
    # overwrite README numbers conceptually with actuals printed
    gap.to_csv(OUT / "gap_replay_rows.csv", index=False)
    dups.to_csv(OUT / "duplicate_opportunities.csv", index=False)
    collapsed.to_csv(OUT / "opportunity_deduped.csv", index=False)
    pd.DataFrame([summary]).to_csv(OUT / "pipeline_number.csv", index=False)
    print(json.dumps(summary, indent=2))
if __name__ == "__main__":
    main()
