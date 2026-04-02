from app.services.db import get_db_connection


def get_today_games(today_str):
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
    SELECT
        game_id,
        game_date,
        league,
        round_code,
        status_code,
        away_team,
        home_team,
        away_starter_name,
        home_starter_name,
        away_starter_pcode,
        home_starter_pcode
    FROM games
    WHERE game_date = ?
      AND league = 'KBO'
    ORDER BY game_id
    """

    cur.execute(query, (today_str,))
    rows = cur.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_game_basic_info(game_id):
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
    SELECT
        game_id,
        game_date,
        league,
        round_code,
        status_code,
        away_team,
        home_team,
        away_starter_name,
        home_starter_name,
        away_starter_pcode,
        home_starter_pcode
    FROM games
    WHERE game_id = ?
    """

    cur.execute(query, (game_id,))
    row = cur.fetchone()
    conn.close()

    return dict(row) if row else None