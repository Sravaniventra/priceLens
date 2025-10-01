'''import sqlite3
from datetime import datetime

DB_NAME = "pricelens.db"


# -------------------------
# Initialize Database
# -------------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # products table
    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            site TEXT,
            name TEXT
        )
    """)

    # prices table with timestamp
    c.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            price REAL,
            checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    """)

    conn.commit()
    conn.close()


# -------------------------
# Insert Product
# -------------------------
def insert_product(url, site, name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        INSERT OR IGNORE INTO products (url, site, name)
        VALUES (?, ?, ?)
    """, (url, site, name))

    conn.commit()

    # return product id
    c.execute("SELECT id FROM products WHERE url = ?", (url,))
    pid = c.fetchone()[0]

    conn.close()
    return pid


# -------------------------
# Insert Price
# -------------------------
def insert_price(product_id, price):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        INSERT INTO prices (product_id, price, checked_at)
        VALUES (?, ?, ?)
    """, (product_id, float(price), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    conn.commit()
    conn.close()


# -------------------------
# Get Last Price
# -------------------------
def get_last_price(product_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        SELECT price, checked_at
        FROM prices
        WHERE product_id = ?
        ORDER BY checked_at DESC
        LIMIT 1
    """, (product_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None  # ✅ only return price


# -------------------------
# Get Price History
# -------------------------
def get_price_history(product_id, days=7):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        SELECT checked_at, price
        FROM prices
        WHERE product_id = ?
          AND checked_at >= datetime('now', ?)
        ORDER BY checked_at ASC
    """, (product_id, f'-{days} days'))

    rows = c.fetchall()
    conn.close()

    #  return rows as list of dicts for easier plotting
    return [{"date": r[0], "price": r[1]} for r in rows]


# -------------------------
# Run Once to Initialize DB
# -------------------------
if __name__ == "__main__":
    init_db()
    print("✅ Database initialized")
   '''
   
import sqlite3
from datetime import datetime

DB_NAME = "pricelens.db"

# -------------------------
# Initialize Database
# -------------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # products table
    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            site TEXT,
            name TEXT
        )
    """)

    # prices table with timestamp
    c.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            price REAL,
            checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    """)

    # subscribers table (NEW)
    c.execute("""
        CREATE TABLE IF NOT EXISTS subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            email TEXT,
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    """)

    conn.commit()
    conn.close()

# Insert Product
def insert_product(url, site, name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        INSERT OR IGNORE INTO products (url, site, name)
        VALUES (?, ?, ?)
    """, (url, site, name))

    conn.commit()

    # return product id
    c.execute("SELECT id FROM products WHERE url = ?", (url,))
    pid = c.fetchone()[0]

    conn.close()
    return pid

# Insert Price
def insert_price(product_id, price):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        INSERT INTO prices (product_id, price, checked_at)
        VALUES (?, ?, ?)
    """, (product_id, float(price), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    conn.commit()
    conn.close()

# Get Last Price
def get_last_price(product_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        SELECT price, checked_at
        FROM prices
        WHERE product_id = ?
        ORDER BY checked_at DESC
        LIMIT 1
    """, (product_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None  # only return price

# Get Price History
def get_price_history(product_id, days=7):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        SELECT checked_at, price
        FROM prices
        WHERE product_id = ?
          AND checked_at >= datetime('now', ?)
        ORDER BY checked_at ASC
    """, (product_id, f'-{days} days'))

    rows = c.fetchall()
    conn.close()

    # return rows as list of dicts for easier plotting
    return [{"date": r[0], "price": r[1]} for r in rows]

# Add Subscriber (NEW)
def add_subscriber(product_id, email):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        INSERT INTO subscribers (product_id, email)
        VALUES (?, ?)
    """, (product_id, email))

    conn.commit()
    conn.close()

# Get Subscribers (NEW)
def get_subscribers(product_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT email FROM subscribers WHERE product_id = ?", (product_id,))
    rows = c.fetchall()
    conn.close()

    return [r[0] for r in rows]  # return list of emails

# Run Once to Initialize DB
if __name__ == "__main__":
    init_db()
    print("✅ Database initialized")
   