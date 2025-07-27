# main.py


import asyncio
import discord
from src.models.db import Database
from src.configs.configs import BOT_TOKEN, DB_PATH


async def run():
    db = Database(DB_PATH)
    await db.connect()
    await db.init_tables()
    '''
    await db.add_row(
        "titles", {
        "name": "OW2",
        "title_logo": "https://yourmomshouse.com"
        }
    )
    '''
    # await db.purge_db()
    await db.close()


if __name__ == "__main__":
    asyncio.run(run())

