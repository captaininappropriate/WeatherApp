import sqlite3


def init_db():
    conn = sqlite3.connect("apikeys.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS api_keys (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 key TEXT NOT NULL)""")
    conn.commit()
    conn.close()


def save_api_key(api_key: str):
    conn = sqlite3.connect("apikeys.db")
    c = conn.cursor()
    # Replace any old key with the new one
    c.execute("DELETE FROM api_keys")
    c.execute("INSERT INTO api_keys (key) VALUES (?)", (api_key,))
    conn.commit()
    conn.close()


def load_api_key() -> str | None:
    conn = sqlite3.connect("apikeys.db")
    c = conn.cursor()
    c.execute("SELECT key FROM api_keys ORDER BY id DESC LIMIT 1")
    result = c.fetchone()
    conn.close()
    return result[0] if result else None
