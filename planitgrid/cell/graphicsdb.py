import aiosqlite
import json

DB_NAME = "graphics.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS designs (
                id INTEGER PRIMARY KEY,
                v_config TEXT,
                h_map_config TEXT
            )
        ''')
        # Insert a sample record
        v = [("royalblue", "Left"), "white", ("crimson", "Right")]
        h_map = {0: [("gold", "Top")], 1: [], 2: [], 3: []}
        
        await db.execute("INSERT INTO designs (v_config, h_map_config) VALUES (?, ?)",
                         (json.dumps(v), json.dumps(h_map)))
        await db.commit()
