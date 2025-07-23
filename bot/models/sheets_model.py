# bot/models/sheets_model.py


import gspread
from oauth2client.service_account import ServiceAccountCredentials
from bot.configs.configs import SERVICE_ACCOUNT_FILE, SCOPES, SPREADSHEET_ID


def get_gspread_client():
    creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPES)
    client = gspread.authorize(creds)
    return client


def get_spreadsheet():
    client = get_gspread_client()
    return client.open_by_key(SPREADSHEET_ID)



def get_or_create_team_sheet(spreadsheet, team_name):
    try:
        return spreadsheet.worksheet(team_name)
    except gspread.WorksheetNotFound:
        sheet = spreadsheet.add_worksheet(title=team_name, rows="100", cols="20")
        # init spreadsheet here
        sheet.append_row(["Round", "Date", "Time", "HomeTeam", "AwayTeam", "HomeRank", "AwayRank", "HomeLogo", "AwayLogo", "HomeScore", "AwayScore", "PoolSize", "HomeRecord", "AwayRecord", "League"])
        return sheet