import json
import aiosqlite
from fastapi import FastAPI, Request, Query, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from contextlib import async_counter
from typing import Optional

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

DB_NAME = "graphics.db"
async def init_db():
    async with aiosqlite.connect("graphics.db") as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS designs (
                id INTEGER PRIMARY KEY,
                admin_name TEXT,
                cell_num INT,
                grid_row INT,
                grid_col INT,
                cell_type TEXT, -- e.g., 'corner', 'edge', 'special'
                v_config TEXT,
                h_map_config TEXT,
                admin_notes TEXT DEFAULT ''
            )
        ''')
        await db.commit()
# Helper to generate unique variety for the demo
def get_unique_config(index: int):
    colors = ["#3498db", "#e74c3c", "#2ecc71", "#f1c40f", "#9b59b6", "#34495e"]
    c1 = colors[index % len(colors)]
    c2 = colors[(index + 2) % len(colors)]
    
    v = [(c1, f"L{index}"), "white", (c2, f"R{index}")]
    
    # Create 4 parts, each with 0-2 stripes for visual variety
    h_map = {
        "0": [("#444", "Top")] if index % 2 == 0 else [],
        "1": [("#888", f"M{index}_A"), ("#aaa", f"M{index}_B")] if index % 3 == 0 else [("#555", "Mid")],
        "2": [],
        "3": [("#222", "Base")]
    }
    return {"v": v, "h_map": h_map}

async def get_flag_data():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT v_config, h_map_config FROM designs LIMIT 1") as cursor:
            row = await cursor.fetchone()
            if not row: return {"v": [], "h_map": {}}
            return {
                "v": json.loads(row[0]),
                "h_map": json.loads(row[1])
            }
async def get_all_flags(limit=12):
    async with aiosqlite.connect(DB_NAME) as db:
        # Fetching 12 configurations
        async with db.execute("SELECT v_config, h_map_config FROM designs  ?", (limit,)) as cursor:
            rows = await cursor.fetchall()
            return [{"v": json.loads(r[0]), "h_map": json.loads(r[1])} for r in rows]

@app.get("/admin/search")
async def admin_search(
    request: Request, 
    admin_name: Optional[str] = None, 
    cell_type: Optional[str] = None
):
    query = "SELECT admin_name, cell_type, v_config, h_map_config FROM designs WHERE 1=1"
    params = []

    if admin_name:
        query += " AND admin_name LIKE ?"
        params.append(f"%{admin_name}%")
    if cell_type:
        query += " AND cell_type = ?"
        params.append(cell_type)
    results = []
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(query, params) as cursor:
            async for row in cursor:
                results.append({
                    "admin": row[0],
                    "type": row[1],
                    "flag": {
                        "v": json.loads(row[2]),
                        "h_map": json.loads(row[3])
                    }
                })

    return templates.TemplateResponse("admin_search.html", {
        "request": request, 
        "results": results,
        "admin_name": admin_name,
        "cell_type": cell_type
    })

# Update Notes
@app.post("/admin/update-notes/{design_id}")
async def update_notes(design_id: int, notes: str = Form(...)):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE designs SET admin_notes = ? WHERE id = ?", (notes, design_id))
        await db.commit()
    return RedirectResponse(url="/admin/search", status_code=303)

# Delete Configuration
@app.post("/admin/delete/{design_id}")
async def delete_config(design_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("DELETE FROM designs WHERE id = ?", (design_id,))
        await db.commit()
    return RedirectResponse(url="/admin/search", status_code=303)

@app.get("/")
async def read_grid(request: Request):
    flags = await get_all_flags(12)
    grid_cells, flag_index = 0 = [], 0
    for r in range(4):
        for c in range(4):
            is_outer = (r == 0 or r == 3 or c == 0 or c == 3)
            cell_data = {"is_outer": is_outer, "r": r, "c": c}
            if is_outer and flag_index < len(flags):
                cell_data["flag"] = flags[flag_index] # get_unique_config(flag_index)
                flag_index += 1
            grid_cells.append({cell_data})

    return templates.TemplateResponse("grid.html", {
        "request": request, 
        "grid": grid_cells, 
    })
