import drawsvg as draw
import json
from datetime import datetime

def get_status_class(text):
    t = text.lower()
    if "live" in t: return "status-live"
    if "error" in t or "fatal" in t: return "status-error"
    if "busy" in t or "sync" in t: return "status-busy"
    if "idle" in t: return "status-idle"
    return "status-default"

def generate_master_grid(json_file):
    # Dimensions & Layout
    GRID_SIZE = 4
    CELL_DIM = 100
    GAP = 12
    FOOTER_HEIGHT = 60
    GRID_AREA_SIZE = (CELL_DIM * GRID_SIZE) + (GAP * (GRID_SIZE + 1))
    CANVAS_H = GRID_AREA_SIZE + FOOTER_HEIGHT
    
    # Load Data
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: JSON file not found.")
        return

    d = draw.Drawing(GRID_AREA_SIZE, CANVAS_H)

    # 1. Unified CSS
    d.append(draw.Raw("""
    <style>
        .cell-base { transition: all 0.2s; stroke-width: 2; }
        .outer-group:hover .cell-base { filter: brightness(92%); transform: translateY(-2px); }
        .inner-group:hover .cell-base { fill: #2c3e50 !important; stroke: #3498db; }
        
        .status-live { fill: #ecfdf5; stroke: #10b981; }
        .status-error { fill: #fef2f2; stroke: #ef4444; }
        .status-busy { fill: #fffbeb; stroke: #f59e0b; }
        .status-idle { fill: #f8fafc; stroke: #64748b; }
        .status-default { fill: #ffffff; stroke: #e2e8f0; }
        
        .inner-cell { fill: #34495e; stroke: #2c3e50; }
        .inner-text { fill: #ffffff; font-weight: bold; font-size: 10px; }
        .footer-text { fill: #94a3b8; font-size: 10px; font-family: sans-serif; font-style: italic; }
        
        text { pointer-events: none; font-family: 'Segoe UI', sans-serif; }
    </style>
    """))

    # 2. Render Main Grid (4x4)
    for i in range(16):
        row, col = i // 4, i % 4
        x, y = GAP + (col * (CELL_DIM + GAP)), GAP + (row * (CELL_DIM + GAP))

        if i in [5, 6, 9, 10]:
            if i == 5:
                draw_sub_grid(d, x, y, (CELL_DIM * 2) + GAP, data.get('inner_3x3', []))
            continue

        txt = data.get('outer_cells', [""]*16)[i]
        status = get_status_class(txt)
        g = draw.Group(class_="outer-group")
        g.append(draw.Rectangle(x, y, CELL_DIM, CELL_DIM, rx=8, class_=f"cell-base {status}"))
        g.append(draw.Text(txt, 11, x + CELL_DIM/2, y + CELL_DIM/2, center=True, fill="#1e293b"))
        d.append(g)

    # 3. Footer (Legend + Timestamp)
    draw_footer(d, GRID_AREA_SIZE, GRID_AREA_SIZE)

    d.save_svg("final_dashboard.svg")
    print(f"Dashboard generated at {datetime.now().strftime('%H:%M:%S')}")

def draw_sub_grid(drawing, start_x, start_y, total_dim, inner_data):
    SUB_GRID, SUB_GAP = 3, 6
    S_DIM = (total_dim - (SUB_GAP * (SUB_GRID - 1))) / SUB_GRID
    for i in range(9):
        r, c = i // 3, i % 3
        x, y = start_x + (c * (S_DIM + SUB_GAP)), start_y + (r * (S_DIM + SUB_GAP))
        item = inner_data[i] if i < len(inner_data) else {"text": "-", "url": "#"}
        
        h_link = draw.Hyperlink(item['url'])
        g = draw.Group(class_="inner-group", cursor="pointer")
        g.append(draw.Rectangle(x, y, S_DIM, S_DIM, rx=4, class_="cell-base inner-cell"))
        g.append(draw.Text(item['text'], 10, x + S_DIM/2, y + S_DIM/2, center=True, class_="inner-text"))
        h_link.append(g)
        drawing.append(h_link)

def draw_footer(drawing, canvas_width, top_offset):
    # Legend
    statuses = [("Live", "status-live"), ("Error", "status-error"), ("Busy", "status-busy")]
    for i, (label, s_class) in enumerate(statuses):
        x, y = 12 + (i * 80), top_offset + 20
        drawing.append(draw.Rectangle(x, y, 10, 10, rx=2, class_=f"cell-base {s_class}"))
        drawing.append(draw.Text(label, 9, x + 15, y + 8, fill="#64748b"))

    # Timestamp
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    drawing.append(draw.Text(f"Last Updated: {now}", 10, canvas_width - 12, top_offset + 28, 
                             text_anchor="end", class_="footer-text"))

if __name__ == "__main__":
    generate_master_grid("master_grid.json")
