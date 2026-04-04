import sqlite3
import os

print("현재 DB 경로:", os.path.abspath("kbo.db"))

conn = sqlite3.connect("kbo.db")
cur = conn.cursor()

cur.execute("""
SELECT game_id, game_date, away_team, home_team, status_code
FROM games
ORDER BY game_date DESC, game_id DESC
LIMIT 20
""")

rows = cur.fetchall()
print("조회 건수:", len(rows))

for row in rows:
    print(row)

conn.close()