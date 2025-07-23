# bot/configs/configs.py


import os

# bot configs
BOT_TOKEN = 'MTM5NDA1OTMwODA4NTQxNjA4Nw.GLJ83Z.GaDipWr5bI6KlVxOvW_6R-YORLHVonp7Nlz9eg'
GUILD_ID = '1032502640514445312'

# website configs
FLASK_UPLOAD_URL = 'https://a8093cd3cb12.ngrok-free.app/upload_svg'

# embed configs
HARDROCKER_BLUE = "#07244d"

# file structure
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
COMMAND_DIR = os.path.join(BASE_DIR, "commands")
ASSET_DIR = os.path.join(BASE_DIR, "static/images")

# sheets configs
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, "static/json/credentials.json")
SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
SPREADSHEET_ID = "1fEf3sIHh62NGcrRmFLKZicyVfrbXn6xoo19eocEoz-8"  # not the full google sheet link, just the ID

# commands
REGISTERED_TEAMS_FILE = os.path.join(BASE_DIR, "static/json/registered_teams.json")
VARSITY_COORDINATOR_ROLE = "Student Varsity Coordinator"
VALID_SEASON_PREFIXES = ("SP", "FA")
SEASON_REPORTS_FOLDER = os.path.join(PROJECT_ROOT, "records")
CURRENT_SEASON_FILE = os.path.join(BASE_DIR, "static/json/current_season.json")
MANIFEST_FILE = os.path.join(BASE_DIR, "static/json/logo_manifest.json")