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
      AND lower(league) = 'kbo'
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


def get_pitcher_recent_stats(pcode, limit_type="7"):
    if not pcode:
        return []

    conn = get_db_connection()
    cur = conn.cursor()

    if limit_type == "all":
        limit_clause = ""
        params = (pcode, pcode)
    else:
        try:
            row_limit = int(limit_type)
        except:
            row_limit = 7

        limit_clause = f"LIMIT {row_limit}"
        params = (pcode, pcode)

    query = f"""
    SELECT *
    FROM (
        SELECT
            game_id,
            game_date,
            away_team,
            home_team,
            away_pitcher_name AS pitcher_name,
            away_pitcher_pcode AS pitcher_pcode,
            away_g AS g,
            away_inn AS inn,
            away_r AS r,
            away_er AS er,
            away_bb AS bb,
            away_hbp AS hbp,
            away_kk AS kk,
            away_hit AS hit,
            away_hr AS hr,
            away_bf AS bf,
            away_ab AS ab,
            away_era AS era,
            away_wls AS wls,
            'away' AS team_type
        FROM starting_pitcher_stats
        WHERE away_pitcher_pcode = ?

        UNION ALL

        SELECT
            game_id,
            game_date,
            away_team,
            home_team,
            home_pitcher_name AS pitcher_name,
            home_pitcher_pcode AS pitcher_pcode,
            home_g AS g,
            home_inn AS inn,
            home_r AS r,
            home_er AS er,
            home_bb AS bb,
            home_hbp AS hbp,
            home_kk AS kk,
            home_hit AS hit,
            home_hr AS hr,
            home_bf AS bf,
            home_ab AS ab,
            home_era AS era,
            home_wls AS wls,
            'home' AS team_type
        FROM starting_pitcher_stats
        WHERE home_pitcher_pcode = ?
    )
    ORDER BY game_date DESC, game_id DESC
    {limit_clause}
    """

    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_game_detail_with_pitchers(game_id, limit_type="7"):
    game = get_game_basic_info(game_id)
    if not game:
        return None

    away_pitcher_logs = get_pitcher_recent_stats(
        game.get("away_starter_pcode", ""),
        limit_type=limit_type
    )
    home_pitcher_logs = get_pitcher_recent_stats(
        game.get("home_starter_pcode", ""),
        limit_type=limit_type
    )

    return {
        "game": game,
        "away_pitcher_logs": away_pitcher_logs,
        "home_pitcher_logs": home_pitcher_logs,
        "selected_range": limit_type,
    }