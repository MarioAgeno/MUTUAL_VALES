import sqlite3, pathlib
import sys

db = pathlib.Path('d:/Python/MUTUAL_VALES/vales/data/db_vales.db')
if not db.exists():
    print('NO_DB_FILE')
    sys.exit(0)
conn = sqlite3.connect(db)
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
rows = cur.fetchall()
for r in rows:
    print(r[0])
conn.close()
