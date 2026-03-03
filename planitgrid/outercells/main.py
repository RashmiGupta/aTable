import json
import aiosqlite
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from contextlib import async_counter

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

DB_NAME = "graphics.db"

async def get_flag_data():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT v_config, h_map_config FROM designs LIMIT 1") as cursor:
            row = await cursor.fetchone()
            if not row: return {"v": [], "h_map": {}}
            return {
                "v": json.loads(row[0]),
                "h_map": json.loads(row[1])
            }

@app.get("/")
async def read_grid(request: Request):
    flag = await get_flag_data()
    
    # Generate 4x4 Grid coordinates
    grid_cells = []
    for r in range(4):
        for c in range(4):
            # Perimeter logic: row 0 or 3, or col 0 or 3
            is_outer = (r == 0 or r == 3 or c == 0 or c == 3)
            grid_cells.append({"is_outer": is_outer, "r": r, "c": c})

    return templates.TemplateResponse("grid.html", {
        "request": request, 
        "grid": grid_cells, 
        "flag": flag
    })
