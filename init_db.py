import sqlite3

with sqlite3.connect("data.db") as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS alimente (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nume TEXT NOT NULL,
            calorii_pe_portie INTEGER NOT NULL,
            categorie TEXT
        );
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS mese (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aliment_id INTEGER,
            portii REAL NOT NULL,
            data TEXT NOT NULL,
            FOREIGN KEY (aliment_id) REFERENCES alimente (id)
        );
    """)
    conn.commit()
