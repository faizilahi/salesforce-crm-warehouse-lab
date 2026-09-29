from pathlib import Path
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"; DATA.mkdir(parents=True, exist_ok=True)
RNG = np.random.default_rng(718)

def main():
    # Base open opps totaling toward targets via scaling at end
    rows = []
    for i in range(500):
        rows.append({
            "opportunity_id": f"006{i:08d}",
            "account_id": f"001{(i % 80):08d}",
            "opportunity_name": f"Deal {i % 120}",
            "close_date": f"2024-{(7 + (i % 3)):02d}-{(i % 27) + 1:02d}",
            "amount": round(float(RNG.uniform(5000, 80000)), 2),
            "stage": RNG.choice(["Prospecting", "Negotiation", "Closed Won", "Closed Lost"], p=[0.4,0.35,0.15,0.1]),
            "system_modstamp": "2024-07-17T10:00:00Z",
        })
    df = pd.DataFrame(rows)
    # Plant gap updates: 41 opps with modstamp in the skipped window
    for i in range(41):
        df.at[i, "system_modstamp"] = "2024-07-18T18:30:00Z"
        df.at[i, "amount"] = round(float(df.at[i, "amount"]) + 10000, 2)
    # Plant duplicates: copy 28 open deals with new ids
    dups = []
    open_idx = df[df.stage.isin(["Prospecting", "Negotiation"])].index[:28]
    for j, idx in enumerate(open_idx):
        r = df.loc[idx].copy()
        r["opportunity_id"] = f"0069{j:07d}"
        r["system_modstamp"] = "2024-07-17T11:00:00Z"
        dups.append(r)
    df = pd.concat([df, pd.DataFrame(dups)], ignore_index=True)
    df.to_csv(DATA / "sf_opportunity_extract.csv", index=False)
    Path(DATA / "watermark.txt").write_text("2024-07-18T14:02:11Z", encoding="utf-8")
    Path(DATA / "watermark_bad.txt").write_text("2024-07-19T09:00:00Z", encoding="utf-8")
    print("opps", len(df))
if __name__ == "__main__":
    main()
