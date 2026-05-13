import os
import sqlite3
from contextlib import closing
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DB_PATH = os.getenv("DB_PATH", "/data/bookmarks.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with closing(get_conn()) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS bookmarks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

@app.route("/")
def index():
    with closing(get_conn()) as conn:
        bookmarks = conn.execute(
            "SELECT id, title, url, created_at FROM bookmarks ORDER BY id DESC"
        ).fetchall()
    return render_template("index.html", bookmarks=bookmarks)

@app.route("/add", methods=["POST"])
def add_bookmark():
    title = request.form.get("title", "").strip()
    url = request.form.get("url", "").strip()

    if not title or not url:
        return redirect(url_for("index"))

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    with closing(get_conn()) as conn:
        conn.execute(
            "INSERT INTO bookmarks (title, url) VALUES (?, ?)",
            (title, url),
        )
        conn.commit()

    return redirect(url_for("index"))

@app.route("/delete/<int:bookmark_id>", methods=["POST"])
def delete_bookmark(bookmark_id):
    with closing(get_conn()) as conn:
        conn.execute("DELETE FROM bookmarks WHERE id = ?", (bookmark_id,))
        conn.commit()
    return redirect(url_for("index"))

init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
