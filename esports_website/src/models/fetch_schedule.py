# src/models/fetch_schedule.py

import pandas as pd
import requests
import time
from io import StringIO
from src.configs.configs import SCHEDULE_SHEET

cached_df = None
last_fetch_time = 0
CACHE_DURATION = 15

def fetch_schedule():
    global cached_df, last_fetch_time

    now = time.time()
    if cached_df is not None and now - last_fetch_time < CACHE_DURATION:
        return cached_df
    
    try:
        response = requests.get(SCHEDULE_SHEET, timeout=5)
        response.raise_for_status()
        csv_data = response.text.strip()

        if not csv_data:
            raise ValueError("CSV is empty")

        df = pd.read_csv(StringIO(csv_data))

        if df.empty or 'Round' not in df.columns:
            raise ValueError("Missing required columns")
        
        cached_df = df
        last_fetch_time = now
        return df
    
    except Exception as e:
        print(f"[ERROR] Could not fetch schedule: {e}")
        return cached_df if cached_df is not None else pd.DataFrame()

