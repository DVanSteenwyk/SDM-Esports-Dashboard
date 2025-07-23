# bot/commands/start_new_season.py


import os
import json
import discord
from discord import app_commands
from bot.models.sheets_model import get_spreadsheet
from bot.models.generate_season_report_model import generate_season_report
from bot.configs.configs import REGISTERED_TEAMS_FILE, VALID_SEASON_PREFIXES, SEASON_REPORTS_FOLDER, CURRENT_SEASON_FILE


def get_current_season():
    if not os.path.exists(CURRENT_SEASON_FILE):
        return None
    with open(CURRENT_SEASON_FILE, "r") as f:
        data = json.load(f)
        return data.get("season")


def get_previous_season_code(current_code):
    prefix = current_code[:2]
    year = int(current_code[2:])

    if prefix == "SP":
        prev_prefix = "FA"
        prev_year = year - 1
    elif prefix == "FA":
        prev_prefix = "SP"
        prev_year = year
    else:
        raise ValueError("Invalid season prefix")
    
    return f"{prev_prefix}{prev_year}"


class Season(app_commands.Group):

    @app_commands.command(name="start", description="Start a new season for competition and initialize the backend code.")
    @app_commands.describe(
        season_code="The code for the new season (eg. FA2025 or SP2026)"
    )
    async def start_new_season(self, interaction: discord.Interaction, season_code: str):
        
        if not season_code or not (season_code[:2] in VALID_SEASON_PREFIXES and season_code[2:].isdigit()):
            await interaction.response.send_message("Please specify a valid season code like `SP2025` or `FA2025`.")
            return

        with open(CURRENT_SEASON_FILE, "r") as f:
            data = json.load(f)

            if data.get("season"):
                await interaction.response.send_message(
                    f"A season `{data['season']}` is already active. Please end it before starting a new one.",
                    ephemeral=True
                )

        with open(CURRENT_SEASON_FILE, "w") as f:
            json.dump({"season": season_code}, f)
        
        await interaction.response.send_message(f"Season `{season_code}` has been started!")


        '''
        try:
            previous_season = get_previous_season_code(season_code)
        except ValueError:
            await ctx.send("Invalid season code prefix.")
            return

        if not os.path.exists(REGISTERED_TEAMS_FILE):
            with open(CURRENT_SEASON_FILE, "w") as f:
                json.dump({"season": season_code}, f, indent=2)
            await ctx.send("No registered teams found for previous season. Ready for the new season!")
            return

        with open(REGISTERED_TEAMS_FILE, "r") as f:
            registered_data = json.load(f)

        if not registered_data or not registered_data.get("teams"):
            with open(CURRENT_SEASON_FILE, "w") as f:
                json.dump({"season": season_code}, f, indent=2)
            await ctx.send("No registered teams found for previous season. Ready for the new season!")
            return

        await ctx.send("Processing reports... This might take a moment.")

        folder_path = os.path.join(SEASON_REPORTS_FOLDER, previous_season)
        os.makedirs(folder_path, exist_ok=True)

        team_list = registered_data.get("teams", [])
        spreadsheet = get_spreadsheet()

        for team in team_list:
            try:
                worksheet = spreadsheet.worksheet(team)
                data = worksheet.get_all_records()
                report = generate_season_report(data)

                filename = f"{team.replace(' ', '_')}_report.txt"
                report_path = os.path.join(folder_path, filename)

                with open(report_path, "w") as file:
                    file.write(report)

                await ctx.send(f"**{team}** report ready:", file=discord.File(report_path))

                spreadsheet.del_worksheet(worksheet)

            except Exception as e:
                await ctx.send(f"Error processing `{team}`: {e}")
            '''
    @app_commands.command(name="end", description="Ends the current season of competition and compiles competition reports for each team.")
    @app_commands.describe(
        generate_reports="'True' if you would like reports, 'False' if you do not want reports."
    )
    async def end_current_season(self, interaction: discord.Interaction, generate_reports: bool = True):
        try:
            current_season = get_current_season()

            if not current_season:
                await interaction.response.send_message(
                    "There is no active season to end.",
                    ephemeral=True
                )
            
            if generate_reports:
                try:

                    # generate_reports logic
                    # creates a directory for the current season before ending it
                    # walks through each team's data in the schedule sheet and generates
                    # a synopsis of the year
                    pass
                    # generate_reports()

                except Exception as report_error:
                    await interaction.response.send_message(
                        f"Season ended, but failed to generate reports: `{report_error}`",
                        ephemeral=True
                    )
                    return
            
            # end season logic
            # clears the current season from current_season.json
            # clears the current season and teams from registered_teams.json
            # clears the worksheet of the teams

            with open(REGISTERED_TEAMS_FILE, "r") as f:
                data = json.load(f)

            teams_list = data.get("teams", [])

            clear_warning = []
            spreadsheet = get_spreadsheet()
            for team in teams_list:
                try:
                    worksheet = spreadsheet.worksheet(team)
                    spreadsheet.del_worksheet(worksheet)
                except Exception as e:
                    clear_warning.append(f"Warning: Could not remove worksheet for team `{team}`: {e}")
            

            with open(REGISTERED_TEAMS_FILE, "w") as f:
                json.dump({"season": None, "teams": []}, f)

            with open(CURRENT_SEASON_FILE, "w") as f:
                json.dump({"season": None}, f)

            await interaction.response.send_message(
                f"The season `{current_season}` has been ended."
            )
        
        except Exception as e:
            await interaction.response.send_message(
                f"An error occurred while ending the season: `{e}`",
                ephermal=True
            )
            raise


async def setup(bot):
    bot.tree.add_command(Season(name="season", description="All the commands you will need to start and end competitive season."))
