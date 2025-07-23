# main.py

import time
import os
import discord
from discord.ext import commands
from bot.configs.configs import BOT_TOKEN, GUILD_ID, COMMAND_DIR


def run():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)  # may not be needed?
    
    @bot.event
    async def on_ready():
        
        for filename in os.listdir(COMMAND_DIR):
            if filename.endswith(".py"):
                try:
                    start = time.perf_counter()
                    await bot.load_extension(f"bot.commands.{filename[:-3]}")
                    bot.tree.copy_global_to(guild=discord.Object(GUILD_ID))
                    await bot.tree.sync(guild=discord.Object(GUILD_ID))
                    end = time.perf_counter()
                    print(f"Extension '{filename[:-3]}' successfully loaded in {end - start:.2f} seconds.")
                except commands.errors.ExtensionAlreadyLoaded:
                    print(f"Extension already loaded: {filename}")
                except Exception as e:
                    print(f"Failed to load {filename}: {e}")
            
        print(f"Logged in as {bot.user}")

    bot.run(BOT_TOKEN, root_logger=True)


if __name__ == "__main__":
    run()






'''

import aiohttp



FLASK_UPLOAD_URL = 'https://a8093cd3cb12.ngrok-free.app/upload_svg'








@client.event
async def on_message(message):
    if message.author.bot:
        return

    for attachment in message.attachments:
        if attachment.filename.endswith('.svg'):
            svg_data = await attachment.read()

            data = aiohttp.FormData()
            data.add_field('file', svg_data,
                           filename=attachment.filename,
                           content_type='image/svg+xml')
            
            async with aiohttp.ClientSession() as session:
                print(f"Posting to: {FLASK_UPLOAD_URL}")
                async with session.post(FLASK_UPLOAD_URL, data=data) as resp:
                    if resp.status == 200:
                        await message.channel.send(f"Uploaded {attachment.filename} successfully!")
                    else:
                        await message.channel.send(f"Failed to upload {attachment.filename}. Server returned {resp.status}")


'''