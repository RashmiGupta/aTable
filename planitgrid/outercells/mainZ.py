from fastapi import FastAPI, Request, Query
from fastapi.templating import Jinja2Templates
import aiosqlite
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")
DB_NAME = "graphics.db"

@app.get("/search-grid")
async def search_and_grid(
    request: Request, 
    admin_name: str = Query(None), 
    cell_type_keyword: str = Query(None)
):
    # Base query for filtering pinned configurations
    query = "SELECT grid_row, grid_col, v_config, h_map_config, cell_type FROM designs WHERE 1=1"
    params = []

    if admin_name:
        query += " AND admin_name LIKE ?"
        params.append(f"%{admin_name}%")
    
    if cell_type_keyword:
        query += " AND cell_type LIKE ?"
        params.append(f"%{cell_type_keyword}%")

    grid_map = {}
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(query, params) as cursor:
            async for row in cursor:
                r, c = row[0], row[1]
                grid_map[(r, c)] = {
                    "v": json.loads(row[2]),
                    "h_map": json.loads(row[3]),
                    "type": json.loads(row[4])
                }

    # Generate 4x4 matrix for the template
    matrix = []
    for r in range(4):
        row_list = []
        for c in range(4):
            is_outer = (r == 0 or r == 3 or c == 0 or c == 3)
            cell_data = grid_map.get((r, c))
            row_list.append({"r": r, "c": c, "is_outer": is_outer, "data": cell_data})
        matrix.append(row_list)

    return templates.TemplateResponse("grid.html", {
        "request": request, 
        "matrix": matrix,
        "search_meta": {"admin": admin_name, "keyword": cell_type_keyword}
    })
