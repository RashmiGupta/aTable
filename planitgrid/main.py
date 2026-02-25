import aiosqlite
import json
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import drawsvg as draw

app = FastAPI()
templates = Jinja2Templates(directory="templates")

DB_PATH = "dashboard.db"

# --- SVG Logic (Integrated) ---
def generate_svg(outer_data, inner_data):
    GRID_SIZE, CELL_DIM, GAP = 4, 100, 12
    FOOTER_H = 60
    SIZE = (CELL_DIM * GRID_SIZE) + (GAP * (GRID_SIZE + 1))
    d = draw.Drawing(SIZE, SIZE + FOOTER_H)
    
    # (Simplified CSS/Logic from previous steps)
    d.append(draw.Raw("<style>.status-live{fill:#ecfdf5;stroke:#10b981;} .status-default{fill:white;stroke:#ccc;}</style>"))

    for i in range(16):
        row, col = i // 4, i % 4
        x, y = GAP + (col * (CELL_DIM + GAP)), GAP + (row * (CELL_DIM + GAP))
        
        if i in [5, 6, 9, 10]:
            continue # Inner 3x3 logic would go here
            
        txt = outer_data[i] if i < len(outer_data) else ""
        d.append(draw.Rectangle(x, y, CELL_DIM, CELL_DIM, rx=8, class_="status-default"))
        d.append(draw.Text(txt, 11, x+CELL_DIM/2, y+CELL_DIM/2, center=True))

    output_path = "static/dashboard.svg"
    d.save_svg(output_path)
    return output_path

# --- Routes ---
@app.on_event("startup")
async def setup_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS grid_data (id INTEGER PRIMARY KEY, category TEXT, content TEXT, link TEXT)")
        # Insert mock data if empty
        cursor = await db.execute("SELECT count(*) FROM grid_data")
        if (await cursor.fetchone())[0] == 0:
            for i in range(16):
                await db.execute("INSERT INTO grid_data (category, content) VALUES ('outer', ?)", (f"Node {i}",))

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "svg_path": None})

@app.post("/generate")
async def handle_generate(request: Request):
    async with aiosqlite.connect(DB_PATH) as db:
        # Fetch data
        async with db.execute("SELECT content FROM grid_data WHERE category='outer' LIMIT 16") as cursor:
            outer = [row[0] for row in await cursor.fetchall()]
        async with db.execute("SELECT content, link FROM grid_data WHERE category='inner' LIMIT 9") as cursor:
            inner = [{"text": row[0], "url": row[1]} for row in await cursor.fetchall()]
            
    svg_file = generate_svg(outer, inner)
    return templates.TemplateResponse("index.html", {"request": request, "svg_path": f"/{svg_file}?{datetime.now().timestamp()}"})
