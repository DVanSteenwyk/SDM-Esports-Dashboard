# src/models/db.py


import os
import aiosqlite as sql
from src.configs.configs import PROJECT_DIR, BASE_DIR


class Database:
    def __init__(self, db_path=None):
        
        self.db_path = db_path

        if db_path is None:
            raise ValueError("No db_path given.")
        
        if not os.path.isdir(os.path.abspath(os.path.join(db_path, ".."))):
            os.makedirs(os.path.abspath(os.path.join(db_path, "..")))

    async def connect(self):
        self.conn = await sql.connect(self.db_path)
        return self.conn
    
    async def init_tables(self):
        conn = self.conn
        await conn.execute('''CREATE TABLE IF NOT EXISTS matches (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                title INTEGER,
                                league INTEGER,
                                season INTEGER,
                                round integer,
                                match_datetime DATETIME,
                                away INTEGER,
                                home INTEGER,
                                awayscore INTEGER,
                                homescore INTEGER,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                           );''')
        await conn.execute('''CREATE TABLE IF NOT EXISTS teams (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                title INTEGER,
                                school INTEGER,
                                CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                           );''')
        await conn.execute('''CREATE TABLE IF NOT EXISTS titles (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL UNIQUE,
                                title_logo TEXT,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                           );''')
        await conn.execute('''CREATE TABLE IF NOT EXISTS schools (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL UNIQUE,
                                school_logo TEXT,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                           );''')
        await conn.execute('''CREATE TABLE IF NOT EXISTS leagues (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL UNIQUE,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                           );''')
        await conn.execute('''CREATE TABLE IF NOT EXISTS seasons (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL UNIQUE,
                                start_date DATE DEFAULT CURRENT_DATE,
                                end_date DATE DEFAULT CURRENT_DATE,
                                active BOOL,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                           );''')
        await conn.execute('''CREATE TABLE IF NOT EXISTS team_members (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                           );''')
        await conn.execute('''CREATE TABLE IF NOT EXISTS team_records (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                           );''')
        await conn.execute('''CREATE TABLE IF NOT EXISTS members (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                           );''')
        await conn.execute('''CREATE TABLE IF NOT EXISTS officers (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                           );''')
        # ==============================================================================
        # ADD More Tables Here
        # ==============================================================================
        await conn.commit()

    async def add_row(self, table: str, data: dict):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        values = tuple(data.values())

        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        await self.conn.execute(query, values)
        await self.conn.commit()
    
    async def delete_row(self, table: str, conditions: dict):
        pass

    async def purge_db(self):
        cursor = await self.conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = await cursor.fetchall()

        for (table,) in tables:
            if table != "sqlite_sequence":
                await self.conn.execute(f"DROP TABLE IF EXISTS {table}")
        
        await self.conn.commit()

    async def close(self):
        if self.conn:
            await self.conn.close()
            self.conn = None
