# bot/commands/register_teams.py


import json
import aiohttp
import os
import discord
from discord import app_commands
from bot.models.sheets_model import get_or_create_team_sheet, get_spreadsheet
from bot.commands.season_commands import get_current_season
from bot.configs.configs import REGISTERED_TEAMS_FILE, VARSITY_COORDINATOR_ROLE, HARDROCKER_BLUE, FLASK_UPLOAD_URL, ASSET_DIR, GUILD_ID


def load_registered_teams():
    if os.path.exists(REGISTERED_TEAMS_FILE):
        with open(REGISTERED_TEAMS_FILE, "r") as f:
            data = json.load(f)
            if isinstance(data, list):
                return {"season": None, "teams": data}
            return data
    return {"season": None, "teams": []}


def save_registered_teams(season: str, team_list: list):
    data = {
        "season": season,
        "teams": team_list
    }
    with open(REGISTERED_TEAMS_FILE, "w") as f:
        json.dump(data, f, indent=2)


class LogoLinkView(discord.ui.View):
    def __init__(self, team_name: str, logo, on_response):
        super().__init__(timeout=60)
        self.team_name = team_name
        self.logo = logo
        self.on_response = on_response

    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def no_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer()
        await self.on_response(False, interaction)
        self.stop()
    
    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def yes_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer()
        await self.on_response(True, interaction)
        self.stop()


class Teams(app_commands.Group):
    
    @app_commands.command(name="register", description="Register a list of teams for a given season.")
    @app_commands.describe(
        season_code="The code for the current season (eg. FA2025 or SP2026)",
        teams="List of teams to register. NOTE: must be comma-separated (eg. LoL, RL, Val, etc.)"
    )
    async def register_teams(self, interaction: discord.Interaction, season_code: str, *, teams: str):
        try:
            current_season = get_current_season()

            if season_code and season_code != current_season:
                await interaction.response.send_message(
                    f"The current active season is: `{current_season}`.\n"
                    f"Please change to `{season_code}` using `/season start <SEASON>`, before registering teams.",
                    ephemeral=True
                    )
                return

            if not current_season:
                await interaction.response.send_message(
                    "No season is currently initialized. Please run `/season start <SEASON>` first.",
                    ephemeral=True
                    )
                return

            new_teams = [team.strip() for team in teams.split(",") if team.strip()]

            existing_data = load_registered_teams()
            existing_teams = existing_data.get("teams", [])

            merged_teams = list(set(existing_teams + new_teams))
        
            save_registered_teams(season_code, merged_teams)

            spreadsheet = get_spreadsheet()
            for team_name in new_teams:
                if team_name not in existing_teams:
                    get_or_create_team_sheet(spreadsheet, team_name)
        
            await interaction.response.send_message(
                f"Registered teams for `{season_code}`: {', '.join(new_teams)}\n"
                "{logos}"
                )
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: `{e}`")
            raise


    @app_commands.command(name="list", description="List all registered teams for the current season.")
    async def list_teams(self, interaction: discord.Interaction):
        
        data = load_registered_teams()
        season = data.get("season") or "No season set"
        teams = data.get("teams", [])

        if not teams:
            await interaction.response.send_message(
                f"No reams are registered for the current season ({season}).",
                ephemeral=True
                )
        
        
        embed = discord.Embed(title=f"List of teams for `{season}`", color=int(HARDROCKER_BLUE.strip('#'), 16))
        for team in teams:
            embed.add_field(name=team, value="", inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="remove", description="Remove one or more teams from the registered list of teams for the current season")
    @app_commands.describe(
        teams="List of teams to remove. NOTE: must be comma-separated (eg. LoL, RL, Val, etc.)"
    )
    async def remove_teams(self, interaction: discord.Interaction, *, teams: str):
        data = load_registered_teams()
        season = data.get("season") or "No season set"
        registered_teams = set(data.get("teams", []))

        teams_to_remove = {team.strip() for team in teams.split(",") if team.strip()}

        if not teams_to_remove:
            await interaction.response.send_message(
                "Please specify at least one team to remove.",
                ephemeral=True
                )
            return
        
        removed = teams_to_remove.intersection(registered_teams)
        not_found = teams_to_remove.difference(registered_teams)

        if not removed:
            await interaction.response.send_message(
                "None of the specified teams were found in the registered list.",
                ephemeral=True
                )
            return
        
        updated_teams = list(registered_teams.difference(removed))
        save_registered_teams(season, updated_teams)

        response = []
        spreadsheet = get_spreadsheet()
        for team in removed:
            try:
                worksheet = spreadsheet.worksheet(team)
                spreadsheet.del_worksheet(worksheet)
            except Exception as e:
                response.append(f"Warning: Could not remove worksheet for team `{team}`: {e}")

        if removed:
            response.insert(0, f"Removed teams: {', '.join(sorted(removed))}")
        if not_found:
            response.append(f"Teams not found: {', '.join(sorted(not_found))}")
        
        await interaction.response.send_message("\n".join(response))


    @app_commands.command(name="link_logos", description="Link one or more unlinked teams to a logo,")
    @app_commands.describe(

    )
    async def upload_logos(self, interaction: discord.Interaction):
        




async def setup(bot):
    bot.tree.add_command(Teams(name="teams", description="All the commands you will need for our competitive teams."))


        