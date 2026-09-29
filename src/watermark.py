from datetime import datetime
import pandas as pd

def parse_ts(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00")).replace(tzinfo=None)

def incremental(df: pd.DataFrame, watermark: str) -> pd.DataFrame:
    wm = parse_ts(watermark)
    return df[df["system_modstamp"].map(parse_ts) > wm].copy()

def detect_gap(old_wm: str, new_wm: str, df: pd.DataFrame) -> pd.DataFrame:
    a, b = parse_ts(old_wm), parse_ts(new_wm)
    ts = df["system_modstamp"].map(parse_ts)
    return df[(ts > a) & (ts <= b)].copy()
