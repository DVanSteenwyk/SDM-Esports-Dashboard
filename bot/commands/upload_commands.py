# bot/commands/uploads.py


import os
import re
import json
import discord
import cairosvg
from datetime import datetime, timezone
from discord import app_commands
from bot.models.zip_model import ZipExtractor
from bot.configs.configs import ASSET_DIR, MANIFEST_FILE


def sanitize_emoji_name(name: str) -> str:
    name = os.path.splitext(name)[0]
    name = name.lower().replace(" ", "_")
    name = re.sub(r'[^a-z0-9_]', '', name)
    return name[:32] or "emoji"


def sanitize_filename(name: str) -> str:
    base = os.path.splitext(name)[0].lower()
    base = re.sub(r'[^a-z0-9_]', '', base)
    return base or "logo"


def load_manifest():
    if not os.path.exists(MANIFEST_FILE):
        return []
    try:
        with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_manifest(data):
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)


SUPPORTED_EXTENSIONS = [".svg"]


class Uploads(app_commands.Group):

    @app_commands.command(name="logos", description="Upload one or more logos in zip or svg file format.")
    @app_commands.describe(
        logos="Upload a .zip or .svg file."
    )
    async def upload_logos(self, interaction: discord.Interaction, logos: discord.Attachment):
        
        guild = interaction.guild
        
        await interaction.response.defer(thinking=True, ephemeral=True)
        os.makedirs(ASSET_DIR, exist_ok=True)

        manifest = load_manifest()
        existing_files = {entry["stored_svg"] for entry in manifest}
        file_list = []
        skipped = []
        processed = []

        if logos.filename.endswith(".zip"):
            zip_bytes = await logos.read()
            zipextractor = ZipExtractor(zip_bytes, SUPPORTED_EXTENSIONS)
            zipextractor.extract()

            for root, _, files in os.walk(zipextractor.temp_dir):
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext in SUPPORTED_EXTENSIONS:
                        path = os.path.join(root, file)
                        with open(path, "rb") as f:
                            file_list.append((file, f.read()))
            
            zipextractor.cleanup()
        

        elif logos.filename.endswith(SUPPORTED_EXTENSIONS):
            ext = os.path.splitext(logos.filename)[1].lower()
            if ext in SUPPORTED_EXTENSIONS:
                file_bytes = await logos.read()
                file_list.append((logos.filename, file_bytes))
            else:
                await interaction.followup.send("Unsupported file format.", ephemeral=True)
                return
        
        else:
            await interaction.followup.send("Unsupported file type. Upload a .zip .svg file.", ephemeral=True)
            return
        
        for original_name, file_bytes in file_list:
            base = sanitize_filename(original_name)
            ext = os.path.splitext(original_name)[1].lower()

            final_svg_name = f"{base}{ext}"
            if final_svg_name in existing_files:
                skipped.append(final_svg_name)
                continue

            svg_path = os.path.join(ASSET_DIR, final_svg_name)
            with open(svg_path, "wb") as f:
                f.write(file_bytes)
            
            png_name = f"{base}.png"
            png_path = os.path.join(ASSET_DIR, png_name)

            try:
                if ext == ".svg":
                    cairosvg.svg2png(
                        bytestring=file_bytes,
                        write_to=png_path,
                        output_width=128,
                        output_height=128
                    )
            except Exception as e:
                await interaction.followup.send(
                    f"Failed to convert {original_name} to PNG: {e}", ephemeral=True
                )
                continue

            manifest.append({
                "original_name": original_name,
                "stored_svg": final_svg_name,
                "stored_png": png_name,
                "upload_time": datetime.now(timezone.utc).isoformat()
            })

            processed.append(final_svg_name)
        
        save_manifest(manifest)

        summary = ''
        if processed:
            summary += f"Uploaded and processed: {', '.join(processed)}\n"
        if skipped:
            summary += f"Skipped duplicates: {', '.join(skipped)}"
        
        await interaction.followup.send(summary, ephemeral=False)


async def setup(bot):
    bot.tree.add_command(Uploads(name="uploads", description="All the commands you will need for uploading logos."))