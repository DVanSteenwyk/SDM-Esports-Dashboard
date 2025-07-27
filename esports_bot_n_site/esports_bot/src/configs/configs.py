# src/configs/config.py


import os

BOT_TOKEN = ""

# file structure
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROJECT_DIR = os.path.abspath(os.path.join(os.path.join(BASE_DIR, ".."), ".."))
DB_PATH = os.path.join(PROJECT_DIR, "database/esports_database.sqlite")