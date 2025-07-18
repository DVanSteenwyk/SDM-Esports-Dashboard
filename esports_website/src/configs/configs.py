# src/configs/configs.py

import os


BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static/images")

SCHEDULE_SHEET = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQSIZrpRvEvRleoDp8XAqtBwY7p5RCkSyRowyEDCe2sKBG2Uv-TzYT7gN4yrcVlVnKMH4HzoSiUWpPD/pub?output=csv"
