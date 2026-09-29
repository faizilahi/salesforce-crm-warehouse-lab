import pandas as pd, numpy as np
from pathlib import Path
RNG=np.random.default_rng(8)
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data"; SEED=ROOT/"seeds"
DATA.mkdir(parents=True, exist_ok=True); SEED.mkdir(parents=True, exist_ok=True)
stages=["Prospecting","Qualification","Proposal","Closed Won","Closed Lost"]
rows=[]
for i in range(1,301):
  rows.append({"OpportunityId":f"006{i:06d}","AccountId":f"001{int(RNG.integers(1,80)):06d}",
    "Name":f"Deal {i}","StageName":RNG.choice(stages),"Amount":round(float(RNG.uniform(1000,50000)),2)})
# plant messy alternate stage label
rows[0]["StageName"]="Prospect"
pd.DataFrame(rows).to_csv(DATA/"opportunity.csv",index=False)
pd.DataFrame({"StageName":["Prospect","Prospecting"],"stage_std":["Prospecting","Prospecting"]}).to_csv(SEED/"stage_map.csv",index=False)
print("Wrote Salesforce synthetic")

