from flask import Flask, render_template
import json
import aiosqlite

app = Flask(__name__)

@app.route('/')
async def draw_square():
    async with aiosqlite.connect("graphics.db") as db:
        async with db.execute("SELECT v_config, h_map_config FROM designs LIMIT 1") as cursor:
            row = await cursor.fetchone()
            v = json.loads(row[0])
            h_map = json.loads(row[1])

    return render_template('square.html', v=v, h_map=h_map)

if __name__ == '__main__':
    app.run(debug=True)
