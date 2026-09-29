import pandas as pd

KEYS = ["account_id", "opportunity_name", "close_date"]

def find_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    open_df = df[df["stage"].isin(["Prospecting", "Negotiation"])].copy()
    open_df["dup_group"] = open_df.groupby(KEYS).ngroup()
    counts = open_df.groupby("dup_group").size().rename("n")
    open_df = open_df.join(counts, on="dup_group")
    return open_df[open_df["n"] > 1]

def collapse_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    open_mask = df["stage"].isin(["Prospecting", "Negotiation"])
    open_df = df[open_mask].sort_values("system_modstamp")
    dedup = open_df.drop_duplicates(KEYS, keep="last")
    closed = df[~open_mask]
    return pd.concat([dedup, closed], ignore_index=True)
