import os
import json
import sqlite3
from contextlib import closing
from flask import Flask, render_template, request, redirect, url_for, jsonify, Response

app = Flask(__name__)
DB_PATH = os.getenv("DB_PATH", "/data/bookmarks.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with closing(get_conn()) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS bookmarks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                category_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
            )
        """)
        # Insert default category if none exists
        existing = conn.execute("SELECT COUNT(*) as cnt FROM categories").fetchone()
        if existing["cnt"] == 0:
            conn.execute("INSERT INTO categories (name) VALUES (?)", ("未分类",))
        conn.commit()


# ============ Pages ============

@app.route("/")
def index():
    search = request.args.get("q", "").strip()
    category_id = request.args.get("cat", "").strip()

    with closing(get_conn()) as conn:
        categories = conn.execute(
            "SELECT id, name FROM categories ORDER BY id"
        ).fetchall()

        query = "SELECT b.id, b.title, b.url, b.category_id, c.name as category_name FROM bookmarks b LEFT JOIN categories c ON b.category_id = c.id"
        conditions = []
        params = []

        if search:
            conditions.append("(b.title LIKE ? OR b.url LIKE ?)")
            params.extend([f"%{search}%", f"%{search}%"])

        if category_id:
            conditions.append("b.category_id = ?")
            params.append(int(category_id))

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY b.id DESC"
        bookmarks = conn.execute(query, params).fetchall()

    return render_template("index.html",
                           bookmarks=bookmarks,
                           categories=categories,
                           search=search,
                           selected_cat=category_id)


# ============ Bookmark CRUD ============

@app.route("/add", methods=["POST"])
def add_bookmark():
    title = request.form.get("title", "").strip()
    url = request.form.get("url", "").strip()
    category_id = request.form.get("category_id", "").strip()

    if not title or not url:
        return redirect(url_for("index"))

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    cat_id = int(category_id) if category_id else None

    with closing(get_conn()) as conn:
        conn.execute(
            "INSERT INTO bookmarks (title, url, category_id) VALUES (?, ?, ?)",
            (title, url, cat_id),
        )
        conn.commit()

    return redirect(url_for("index"))


@app.route("/edit/<int:bookmark_id>", methods=["POST"])
def edit_bookmark(bookmark_id):
    title = request.form.get("title", "").strip()
    url = request.form.get("url", "").strip()
    category_id = request.form.get("category_id", "").strip()

    if not title or not url:
        return redirect(url_for("index"))

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    cat_id = int(category_id) if category_id else None

    with closing(get_conn()) as conn:
        conn.execute(
            "UPDATE bookmarks SET title=?, url=?, category_id=? WHERE id=?",
            (title, url, cat_id, bookmark_id),
        )
        conn.commit()

    return redirect(url_for("index"))


@app.route("/delete/<int:bookmark_id>", methods=["POST"])
def delete_bookmark(bookmark_id):
    with closing(get_conn()) as conn:
        conn.execute("DELETE FROM bookmarks WHERE id = ?", (bookmark_id,))
        conn.commit()
    return redirect(url_for("index"))


@app.route("/move/<int:bookmark_id>", methods=["POST"])
def move_bookmark(bookmark_id):
    category_id = request.form.get("category_id", "").strip()
    cat_id = int(category_id) if category_id else None

    with closing(get_conn()) as conn:
        conn.execute(
            "UPDATE bookmarks SET category_id=? WHERE id=?",
            (cat_id, bookmark_id),
        )
        conn.commit()

    return redirect(url_for("index"))


# ============ Category CRUD ============

@app.route("/category/add", methods=["POST"])
def add_category():
    name = request.form.get("name", "").strip()
    if not name:
        return redirect(url_for("index"))

    with closing(get_conn()) as conn:
        try:
            conn.execute("INSERT INTO categories (name) VALUES (?)", (name,))
            conn.commit()
        except sqlite3.IntegrityError:
            pass  # duplicate name, ignore

    return redirect(url_for("index"))


@app.route("/category/edit/<int:cat_id>", methods=["POST"])
def edit_category(cat_id):
    name = request.form.get("name", "").strip()
    if not name:
        return redirect(url_for("index"))

    with closing(get_conn()) as conn:
        try:
            conn.execute("UPDATE categories SET name=? WHERE id=?", (name, cat_id))
            conn.commit()
        except sqlite3.IntegrityError:
            pass

    return redirect(url_for("index"))


@app.route("/category/delete/<int:cat_id>", methods=["POST"])
def delete_category(cat_id):
    with closing(get_conn()) as conn:
        # Bookmarks in this category will have category_id set to NULL (ON DELETE SET NULL)
        conn.execute("DELETE FROM categories WHERE id = ?", (cat_id,))
        conn.commit()

    return redirect(url_for("index"))


# ============ Import / Export ============

@app.route("/export")
def export_bookmarks():
    with closing(get_conn()) as conn:
        categories = conn.execute("SELECT id, name FROM categories ORDER BY id").fetchall()
        bookmarks = conn.execute(
            "SELECT id, title, url, category_id, created_at FROM bookmarks ORDER BY id"
        ).fetchall()

    data = {
        "categories": [{"id": c["id"], "name": c["name"]} for c in categories],
        "bookmarks": [
            {
                "id": b["id"],
                "title": b["title"],
                "url": b["url"],
                "category_id": b["category_id"],
                "created_at": b["created_at"],
            }
            for b in bookmarks
        ],
    }

    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    return Response(
        json_str,
        mimetype="application/json",
        headers={"Content-Disposition": "attachment; filename=bookmarks_export.json"},
    )


@app.route("/import", methods=["POST"])
def import_bookmarks():
    file = request.files.get("file")
    if not file:
        return redirect(url_for("index"))

    try:
        data = json.loads(file.read().decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return redirect(url_for("index"))

    with closing(get_conn()) as conn:
        # Import categories
        cat_id_map = {}  # old_id -> new_id
        for cat in data.get("categories", []):
            old_id = cat.get("id")
            name = cat.get("name", "").strip()
            if not name:
                continue

            existing = conn.execute(
                "SELECT id FROM categories WHERE name = ?", (name,)
            ).fetchone()

            if existing:
                cat_id_map[old_id] = existing["id"]
            else:
                cursor = conn.execute(
                    "INSERT INTO categories (name) VALUES (?)", (name,)
                )
                cat_id_map[old_id] = cursor.lastrowid

        # Import bookmarks
        for bm in data.get("bookmarks", []):
            title = bm.get("title", "").strip()
            url = bm.get("url", "").strip()
            old_cat_id = bm.get("category_id")

            if not title or not url:
                continue

            new_cat_id = cat_id_map.get(old_cat_id) if old_cat_id else None

            conn.execute(
                "INSERT INTO bookmarks (title, url, category_id) VALUES (?, ?, ?)",
                (title, url, new_cat_id),
            )

        conn.commit()

    return redirect(url_for("index"))


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
