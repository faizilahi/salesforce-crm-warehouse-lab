from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
DATA,OUT=ROOT/"data",ROOT/"output"; OUT.mkdir(parents=True, exist_ok=True)
opp=pd.read_csv(DATA/"opportunity.csv"); mp=pd.read_csv(ROOT/"seeds"/"stage_map.csv")
opp=opp.merge(mp, on="StageName", how="left")
opp["stage_std"]=opp["stage_std"].fillna(opp["StageName"])
# natural key dedupe
opp=opp.sort_values("OpportunityId").drop_duplicates(["AccountId","Name"], keep="last")
summary=opp.groupby("stage_std",as_index=False).agg(opportunities=("OpportunityId","count"),pipeline=("Amount","sum"))
summary["pipeline"]=summary["pipeline"].round(2)
summary.to_csv(OUT/"summary.csv",index=False)
print(summary)

