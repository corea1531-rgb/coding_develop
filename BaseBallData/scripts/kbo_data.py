import requests
from datetime import datetime, timedelta
import sqlite3
import pandas as pd
import os


today = datetime.today()

from_date = (today - timedelta(days=5)).strftime('%Y-%m-%d')
to_date = (today + timedelta(days=5)).strftime('%Y-%m-%d')

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ko-KR,ko;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-US;q=0.6,en;q=0.5,ja;q=0.4',
    'charset': 'utf-8',
    'origin': 'https://m.sports.naver.com',
    'priority': 'u=1, i',
    'referer': 'https://m.sports.naver.com/kbaseball/schedule/index?category=kbo&date=2026-03-12',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
    'x-sports-backend': 'kotlin',
}

league = 'kbo'

league_info = {
    'kbo': {'upperCategoryId': 'kbaseball', 'categoryId': 'kbo'},
    'npb': {'upperCategoryId': 'wbaseball', 'categoryId': 'npb'},
    'mlb': {'upperCategoryId': 'wbaseball', 'categoryId': 'mlb'}
}

params = {
    'fields': 'basic,schedule,baseball,manualRelayUrl',
    'upperCategoryId': league_info[league]['upperCategoryId'],
    'categoryId': league_info[league]['categoryId'],
    'fromDate': from_date,
    'toDate': to_date,
    'roundCodes': '',
    'size': '500',
}

DB_PATH = 'kbo.db'

# 디버그 함수, 추후에 지울 것

DEBUG = True

def dprint(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


def safe_int(value, default=0):
    try:
        return int(value)
    except:
        return default

def get_conn():
    return sqlite3.connect(DB_PATH)

def create_tables():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS games (
        game_id TEXT PRIMARY KEY,
        game_date TEXT,
        league TEXT,
        round_code TEXT,
        status_code TEXT,
        away_team TEXT,
        home_team TEXT,
        away_starter_name TEXT,
        home_starter_name TEXT,
        away_starter_pcode TEXT,
        home_starter_pcode TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS pitcher_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        game_id TEXT,
        game_date TEXT,
        team_type TEXT,
        pitcher_name TEXT,
        pitcher_pcode TEXT,
        pitcher_inn TEXT,
        pitcher_bbhp INTEGER,
        event_inning INTEGER,
        batter_name TEXT,
        batter_code TEXT,
        result_type TEXT,
        text TEXT,
        away_team TEXT,
        home_team TEXT,
        UNIQUE(game_id, pitcher_pcode, event_inning, batter_code, result_type, text)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS first_pitch (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        game_id TEXT,
        game_date TEXT,
        inning INTEGER,
        away_team TEXT,
        home_team TEXT,
        batter_name TEXT,
        batter_code TEXT,
        title TEXT,
        pitch_result TEXT,
        text TEXT,
        stuff TEXT,
        speed TEXT,
        UNIQUE(game_id, inning, batter_code)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS batters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        game_id TEXT,
        game_date TEXT,
        team_type TEXT,
        team_name TEXT,
        player_code TEXT,
        name TEXT,
        pos TEXT,
        bat_order TEXT,
        has_player_end TEXT,
        ab TEXT,
        bb TEXT,
        hit TEXT,
        kk TEXT,
        hr TEXT,
        rbi TEXT,
        run TEXT,
        sb TEXT,
        hra TEXT,
        UNIQUE(game_id, player_code)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS batter_inning_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        game_id TEXT,
        game_date TEXT,
        team_type TEXT,
        team_name TEXT,
        player_code TEXT,
        name TEXT,
        pos TEXT,
        bat_order TEXT,
        inning INTEGER,
        inning_key TEXT,
        result TEXT,
        UNIQUE(game_id, player_code, inning_key)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS starting_lineups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        game_id TEXT,
        game_date TEXT,
        team_type TEXT,
        team_name TEXT,
        bat_order INTEGER,
        name TEXT,
        pcode TEXT,
        pos_name TEXT,
        pos TEXT,
        seqno TEXT,
        UNIQUE(game_id, team_type, bat_order)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS team_totals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        game_id TEXT,
        game_date TEXT,
        team_type TEXT,
        team_name TEXT,
        opponent_team TEXT,
        ab TEXT,
        hit TEXT,
        hra TEXT,
        rbi TEXT,
        run TEXT,
        sb TEXT,
        UNIQUE(game_id, team_type)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS starting_pitcher_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        game_id TEXT UNIQUE,
        game_date TEXT,
        away_team TEXT,
        home_team TEXT,

        away_pitcher_name TEXT,
        away_pitcher_pcode TEXT,
        away_g TEXT,
        away_inn TEXT,
        away_r TEXT,
        away_er TEXT,
        away_bb TEXT,
        away_hbp TEXT,
        away_kk TEXT,
        away_hit TEXT,
        away_hr TEXT,
        away_bf TEXT,
        away_ab TEXT,
        away_era TEXT,
        away_wls TEXT,

        home_pitcher_name TEXT,
        home_pitcher_pcode TEXT,
        home_g TEXT,
        home_inn TEXT,
        home_r TEXT,
        home_er TEXT,
        home_bb TEXT,
        home_hbp TEXT,
        home_kk TEXT,
        home_hit TEXT,
        home_hr TEXT,
        home_bf TEXT,
        home_ab TEXT,
        home_era TEXT,
        home_wls TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS game_flow_summary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        game_id TEXT UNIQUE,
        game_date TEXT,
        away_team TEXT,
        home_team TEXT,

        away_starter_name TEXT,
        away_starter_pcode TEXT,
        away_starter_inn TEXT,

        home_starter_name TEXT,
        home_starter_pcode TEXT,
        home_starter_inn TEXT,

        away_starter_r_1 TEXT,
        away_starter_r_4 TEXT,
        away_starter_r_5 TEXT,

        home_starter_r_1 TEXT,
        home_starter_r_4 TEXT,
        home_starter_r_5 TEXT,

        away_team_scored_1 TEXT,
        away_team_allowed_1 TEXT,
        away_team_scored_4 TEXT,
        away_team_allowed_4 TEXT,
        away_team_scored_5 TEXT,
        away_team_allowed_5 TEXT,
        away_team_scored_9 TEXT,
        away_team_allowed_9 TEXT,

        home_team_scored_1 TEXT,
        home_team_allowed_1 TEXT,
        home_team_scored_4 TEXT,
        home_team_allowed_4 TEXT,
        home_team_scored_5 TEXT,
        home_team_allowed_5 TEXT,
        home_team_scored_9 TEXT,
        home_team_allowed_9 TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_game(
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
):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    INSERT OR IGNORE INTO games (
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
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
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
    ))

    conn.commit()
    conn.close()

def insert_starting_lineup_rows(rows):
    conn = get_conn()
    cur = conn.cursor()

    cur.executemany("""
    INSERT OR IGNORE INTO starting_lineups (
        game_id,
        game_date,
        team_type,
        team_name,
        bat_order,
        name,
        pcode,
        pos_name,
        pos,
        seqno
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        (
            row['game_id'],
            row['game_date'],
            row['team_type'],
            row['team_name'],
            row['batOrder'],
            row['name'],
            row['pcode'],
            row['posName'],
            row['pos'],
            row['seqno']
        )
        for row in rows
    ])

    conn.commit()
    conn.close()


def insert_batter_rows(rows):
    conn = get_conn()
    cur = conn.cursor()

    cur.executemany("""
    INSERT OR IGNORE INTO batters (
        game_id,
        game_date,
        team_type,
        team_name,
        player_code,
        name,
        pos,
        bat_order,
        has_player_end,
        ab,
        bb,
        hit,
        kk,
        hr,
        rbi,
        run,
        sb,
        hra
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        (
            row['game_id'],
            row['game_date'],
            row['team_type'],
            row['team_name'],
            row['playerCode'],
            row['name'],
            row['pos'],
            row['batOrder'],
            row['hasPlayerEnd'],
            row['ab'],
            row['bb'],
            row['hit'],
            row['kk'],
            row['hr'],
            row['rbi'],
            row['run'],
            row['sb'],
            row['hra']
        )
        for row in rows
    ])

    conn.commit()
    conn.close()


def insert_batter_inning_event_rows(rows):
    conn = get_conn()
    cur = conn.cursor()

    cur.executemany("""
    INSERT OR IGNORE INTO batter_inning_events (
        game_id,
        game_date,
        team_type,
        team_name,
        player_code,
        name,
        pos,
        bat_order,
        inning,
        inning_key,
        result
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        (
            row['game_id'],
            row['game_date'],
            row['team_type'],
            row['team_name'],
            row['playerCode'],
            row['name'],
            row['pos'],
            row['batOrder'],
            row['inning'],
            row['inning_key'],
            row['result']
        )
        for row in rows
    ])

    conn.commit()
    conn.close()


def insert_team_total_rows(rows):
    conn = get_conn()
    cur = conn.cursor()

    cur.executemany("""
    INSERT OR IGNORE INTO team_totals (
        game_id,
        game_date,
        team_type,
        team_name,
        opponent_team,
        ab,
        hit,
        hra,
        rbi,
        run,
        sb
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        (
            row['game_id'],
            row['game_date'],
            row['team_type'],
            row['team_name'],
            row['opponent_team'],
            row['ab'],
            row['hit'],
            row['hra'],
            row['rbi'],
            row['run'],
            row['sb']
        )
        for row in rows
    ])

    conn.commit()
    conn.close()

def insert_first_pitch_rows(rows):
    conn = get_conn()
    cur = conn.cursor()

    cur.executemany("""
    INSERT OR IGNORE INTO first_pitch (
        game_id,
        game_date,
        inning,
        away_team,
        home_team,
        batter_name,
        batter_code,
        title,
        pitch_result,
        text,
        stuff,
        speed
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        (
            row['game_id'],
            row['game_date'],
            row['inning'],
            row['away_team'],
            row['home_team'],
            row['batter_name'],
            row['batter_code'],
            row['title'],
            row['pitchResult'],
            row['text'],
            row['stuff'],
            row['speed']
        )
        for row in rows
    ])

    conn.commit()
    conn.close()

def insert_pitcher_event_rows(rows):
    conn = get_conn()
    cur = conn.cursor()

    cur.executemany("""
    INSERT OR IGNORE INTO pitcher_events (
        game_id,
        game_date,
        team_type,
        pitcher_name,
        pitcher_pcode,
        pitcher_inn,
        pitcher_bbhp,
        event_inning,
        batter_name,
        batter_code,
        result_type,
        text,
        away_team,
        home_team
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        (
            row['game_id'],
            row['game_date'],
            row['team_type'],
            row['pitcher_name'],
            row['pitcher_pcode'],
            row['pitcher_inn'],
            row['pitcher_bb'],
            row['walk_inning'],
            row['batter_name'],
            row['batter_code'],
            row['result_type'],
            row['text'],
            row['away_team'],
            row['home_team']
        )
        for row in rows
    ])

    conn.commit()
    conn.close()

def insert_starting_pitcher_stats_rows(rows):
    conn = get_conn()
    cur = conn.cursor()

    cur.executemany("""
    INSERT OR IGNORE INTO starting_pitcher_stats (
        game_id,
        game_date,
        away_team,
        home_team,

        away_pitcher_name,
        away_pitcher_pcode,
        away_g,
        away_inn,
        away_r,
        away_er,
        away_bb,
        away_hbp,
        away_kk,
        away_hit,
        away_hr,
        away_bf,
        away_ab,
        away_era,
        away_wls,

        home_pitcher_name,
        home_pitcher_pcode,
        home_g,
        home_inn,
        home_r,
        home_er,
        home_bb,
        home_hbp,
        home_kk,
        home_hit,
        home_hr,
        home_bf,
        home_ab,
        home_era,
        home_wls
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        (
            row['game_id'],
            row['game_date'],
            row['away_team'],
            row['home_team'],

            row['away_pitcher_name'],
            row['away_pitcher_pcode'],
            row['away_g'],
            row['away_inn'],
            row['away_r'],
            row['away_er'],
            row['away_bb'],
            row['away_hbp'],
            row['away_kk'],
            row['away_hit'],
            row['away_hr'],
            row['away_bf'],
            row['away_ab'],
            row['away_era'],
            row['away_wls'],

            row['home_pitcher_name'],
            row['home_pitcher_pcode'],
            row['home_g'],
            row['home_inn'],
            row['home_r'],
            row['home_er'],
            row['home_bb'],
            row['home_hbp'],
            row['home_kk'],
            row['home_hit'],
            row['home_hr'],
            row['home_bf'],
            row['home_ab'],
            row['home_era'],
            row['home_wls']
        )
        for row in rows
    ])

    conn.commit()
    conn.close()

def insert_game_flow_summary_rows(rows):
    conn = get_conn()
    cur = conn.cursor()

    cur.executemany("""
    INSERT OR IGNORE INTO game_flow_summary (
        game_id,
        game_date,
        away_team,
        home_team,

        away_starter_name,
        away_starter_pcode,
        away_starter_inn,

        home_starter_name,
        home_starter_pcode,
        home_starter_inn,

        away_starter_r_1,
        away_starter_r_4,
        away_starter_r_5,

        home_starter_r_1,
        home_starter_r_4,
        home_starter_r_5,

        away_team_scored_1,
        away_team_allowed_1,
        away_team_scored_4,
        away_team_allowed_4,
        away_team_scored_5,
        away_team_allowed_5,
        away_team_scored_9,
        away_team_allowed_9,

        home_team_scored_1,
        home_team_allowed_1,
        home_team_scored_4,
        home_team_allowed_4,
        home_team_scored_5,
        home_team_allowed_5,
        home_team_scored_9,
        home_team_allowed_9
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        (
            row['game_id'],
            row['game_date'],
            row['away_team'],
            row['home_team'],

            row['away_starter_name'],
            row['away_starter_pcode'],
            row['away_starter_inn'],

            row['home_starter_name'],
            row['home_starter_pcode'],
            row['home_starter_inn'],

            row['away_starter_r_1'],
            row['away_starter_r_4'],
            row['away_starter_r_5'],

            row['home_starter_r_1'],
            row['home_starter_r_4'],
            row['home_starter_r_5'],

            row['away_team_scored_1'],
            row['away_team_allowed_1'],
            row['away_team_scored_4'],
            row['away_team_allowed_4'],
            row['away_team_scored_5'],
            row['away_team_allowed_5'],
            row['away_team_scored_9'],
            row['away_team_allowed_9'],

            row['home_team_scored_1'],
            row['home_team_allowed_1'],
            row['home_team_scored_4'],
            row['home_team_allowed_4'],
            row['home_team_scored_5'],
            row['home_team_allowed_5'],
            row['home_team_scored_9'],
            row['home_team_allowed_9']
        )
        for row in rows
    ])

    conn.commit()
    conn.close()

def safe_float(value, default=0.0):
    try:
        return float(value)
    except:
        return default


def get_pitcher_search_end_inning(inn_value):
    if inn_value in [None, '']:
        return 0

    s = str(inn_value).strip()
    s = ' '.join(s.split())
    base_str = s.split()[0]

    try:
        base_inning = int(base_str)
    except:
        return 0

    if ('⅓' in s) or ('⅔' in s) or ('1/3' in s) or ('2/3' in s):
        return base_inning + 1

    return base_inning


def get_scoreboard_runs_by_inning(record_data):
    result = {'away': {}, 'home': {}}

    score_board = record_data.get('scoreBoard', {})
    inn_data = score_board.get('inn', {})

    away_list = inn_data.get('away', [])
    home_list = inn_data.get('home', [])

    if isinstance(away_list, list):
        for idx, val in enumerate(away_list, start=1):
            result['away'][idx] = safe_int(val, 0)

    if isinstance(home_list, list):
        for idx, val in enumerate(home_list, start=1):
            result['home'][idx] = safe_int(val, 0)

    return result


def sum_runs_until(inning_runs, end_inning):
    total = 0
    for i in range(1, end_inning + 1):
        total += safe_int(inning_runs.get(i, 0), 0)
    return total


def get_starter_result_value(runs_allowed_until_n, starter_end_inning, target_inning):
    """
    예:
    - 선발이 5이닝 이상 소화 -> target 이닝까지 실점값 반환
    - 선발이 target 이전에 내려감 -> "" 반환이 아니라
      '선발투수 X이닝 미만' 조건에 따라 실제 소화 범위까지 실점값 반환
    단, 5이닝 항목만 별도 규칙:
      3이닝까지만 던졌다면 5이닝 결과는 "".
    """
    if target_inning == 5 and starter_end_inning < 4:
        return ""

    compare_inning = min(starter_end_inning, target_inning)
    return str(runs_allowed_until_n.get(compare_inning, 0))

def extract_starting_pitcher_stats_row(
    game_id,
    game_date,
    away_team,
    home_team,
    away_pitcher,
    home_pitcher
):
    return {
        'game_id': game_id,
        'game_date': game_date,
        'away_team': away_team,
        'home_team': home_team,

        'away_pitcher_name': away_pitcher.get('name', ''),
        'away_pitcher_pcode': str(away_pitcher.get('pcode', away_pitcher.get('playerCode', ''))).strip(),
        'away_g': away_pitcher.get('g', ''),
        'away_inn': away_pitcher.get('inn', ''),
        'away_r': away_pitcher.get('r', ''),
        'away_er': away_pitcher.get('er', ''),
        'away_bb': away_pitcher.get('bb', ''),
        'away_hbp': away_pitcher.get('hbp', ''),
        'away_kk': away_pitcher.get('kk', ''),
        'away_hit': away_pitcher.get('hit', ''),
        'away_hr': away_pitcher.get('hr', ''),
        'away_bf': away_pitcher.get('bf', ''),
        'away_ab': away_pitcher.get('ab', ''),
        'away_era': away_pitcher.get('era', ''),
        'away_wls': away_pitcher.get('wls', ''),

        'home_pitcher_name': home_pitcher.get('name', ''),
        'home_pitcher_pcode': str(home_pitcher.get('pcode', home_pitcher.get('playerCode', ''))).strip(),
        'home_g': home_pitcher.get('g', ''),
        'home_inn': home_pitcher.get('inn', ''),
        'home_r': home_pitcher.get('r', ''),
        'home_er': home_pitcher.get('er', ''),
        'home_bb': home_pitcher.get('bb', ''),
        'home_hbp': home_pitcher.get('hbp', ''),
        'home_kk': home_pitcher.get('kk', ''),
        'home_hit': home_pitcher.get('hit', ''),
        'home_hr': home_pitcher.get('hr', ''),
        'home_bf': home_pitcher.get('bf', ''),
        'home_ab': home_pitcher.get('ab', ''),
        'home_era': home_pitcher.get('era', ''),
        'home_wls': home_pitcher.get('wls', '')
    }

def extract_game_flow_summary_row(
    record_data,
    game_id,
    game_date,
    away_team,
    home_team,
    away_pitcher,
    home_pitcher
):
    inning_runs = get_scoreboard_runs_by_inning(record_data)

    away_starter_inn = get_pitcher_search_end_inning(away_pitcher.get('inn', ''))
    home_starter_inn = get_pitcher_search_end_inning(home_pitcher.get('inn', ''))

    away_allowed_until = {}
    home_allowed_until = {}

    for n in range(1, 10):
        # away 선발은 home 타선 점수를 허용
        away_allowed_until[n] = sum_runs_until(inning_runs['home'], min(n, 9))
        # home 선발은 away 타선 점수를 허용
        home_allowed_until[n] = sum_runs_until(inning_runs['away'], min(n, 9))

    return {
        'game_id': game_id,
        'game_date': game_date,
        'away_team': away_team,
        'home_team': home_team,

        'away_starter_name': away_pitcher.get('name', ''),
        'away_starter_pcode': str(away_pitcher.get('pcode', away_pitcher.get('playerCode', ''))).strip(),
        'away_starter_inn': away_pitcher.get('inn', ''),

        'home_starter_name': home_pitcher.get('name', ''),
        'home_starter_pcode': str(home_pitcher.get('pcode', home_pitcher.get('playerCode', ''))).strip(),
        'home_starter_inn': home_pitcher.get('inn', ''),

        'away_starter_r_1': get_starter_result_value(away_allowed_until, away_starter_inn, 1),
        'away_starter_r_4': get_starter_result_value(away_allowed_until, away_starter_inn, 4),
        'away_starter_r_5': get_starter_result_value(away_allowed_until, away_starter_inn, 5),

        'home_starter_r_1': get_starter_result_value(home_allowed_until, home_starter_inn, 1),
        'home_starter_r_4': get_starter_result_value(home_allowed_until, home_starter_inn, 4),
        'home_starter_r_5': get_starter_result_value(home_allowed_until, home_starter_inn, 5),

        'away_team_scored_1': str(sum_runs_until(inning_runs['away'], 1)),
        'away_team_allowed_1': str(sum_runs_until(inning_runs['home'], 1)),
        'away_team_scored_4': str(sum_runs_until(inning_runs['away'], 4)),
        'away_team_allowed_4': str(sum_runs_until(inning_runs['home'], 4)),
        'away_team_scored_5': str(sum_runs_until(inning_runs['away'], 5)),
        'away_team_allowed_5': str(sum_runs_until(inning_runs['home'], 5)),
        'away_team_scored_9': str(sum_runs_until(inning_runs['away'], 9)),
        'away_team_allowed_9': str(sum_runs_until(inning_runs['home'], 9)),

        'home_team_scored_1': str(sum_runs_until(inning_runs['home'], 1)),
        'home_team_allowed_1': str(sum_runs_until(inning_runs['away'], 1)),
        'home_team_scored_4': str(sum_runs_until(inning_runs['home'], 4)),
        'home_team_allowed_4': str(sum_runs_until(inning_runs['away'], 4)),
        'home_team_scored_5': str(sum_runs_until(inning_runs['home'], 5)),
        'home_team_allowed_5': str(sum_runs_until(inning_runs['away'], 5)),
        'home_team_scored_9': str(sum_runs_until(inning_runs['home'], 9)),
        'home_team_allowed_9': str(sum_runs_until(inning_runs['away'], 9))
    }

def extract_starting_lineup_rows(relay_data, game_date, game_id, away_team, home_team):
    """
    relay_data 안의 awayLineup / homeLineup 에서
    seqno == 1 인 선발타자만 추출
    batOrder 순으로 정렬해서 row 리스트 반환
    """
    rows = []

    text_relay_data = relay_data.get('result', {}).get('textRelayData', {})

    lineup_info = [
        ('away', away_team, text_relay_data.get('awayLineup', {}).get('batter', [])),
        ('home', home_team, text_relay_data.get('homeLineup', {}).get('batter', [])),
    ]

    for team_type, team_name, batters in lineup_info:
        # seqno == 1 인 선수만 = 선발타자
        starters = [
            batter for batter in batters
            if str(batter.get('seqno', '')).strip() == '1'
        ]

        # batOrder 순 정렬
        starters = sorted(
            starters,
            key=lambda x: int(x.get('batOrder', 999))
        )

        for batter in starters:
            rows.append({
                'game_date': game_date,
                'game_id': game_id,
                'team_type': team_type,
                'team_name': team_name,
                'batOrder': batter.get('batOrder', ''),
                'name': batter.get('name', ''),
                'pcode': batter.get('pcode', ''),
                'posName': batter.get('posName', ''),
                'pos': batter.get('pos', ''),
                'seqno': batter.get('seqno', '')
            })

    return rows


def get_search_end_inning(inn_value):
    """
    예:
    '3'   -> 3
    '3 ⅓' -> 4
    '3 ⅔' -> 4
    '4'   -> 4
    '4 ⅔' -> 5
    """
    if inn_value in [None, '']:
        return 0

    s = str(inn_value).strip()
    s = ' '.join(s.split())

    base_str = s.split()[0]

    try:
        base_inning = int(base_str)
    except:
        return 0

    if ('⅓' in s) or ('⅔' in s) or ('1/3' in s) or ('2/3' in s):
        return base_inning + 1

    return base_inning


def get_result_type(text):
    text = str(text).strip()

    if ('몸에 맞는 볼' in text) or ('사구' in text) or ('몸맞는볼' in text):
        return 'hbp'

    if ('볼넷' in text) or ('고의4구' in text):
        return 'bb'

    return ''


def is_runner_event_text(text):
    text = str(text).strip()
    runner_keywords = ['루주자', '진루', '도루', '폭투', '보크', '견제']
    return any(keyword in text for keyword in runner_keywords)


def make_batter_code_name_map(record_data):
    batter_map = {}

    for side in ['away', 'home']:
        batters = record_data.get('battersBoxscore', {}).get(side, [])
        for batter in batters:
            code = str(
                batter.get('playerCode', batter.get('pcode', batter.get('batterCode', '')))
            ).strip()
            name = batter.get('name', '')
            if code:
                batter_map[code] = name

    return batter_map


def find_final_batter_result(text_options):
    """
    뒤에서부터 보면서
    주자 진루 같은 부가 이벤트를 제외하고
    볼넷/사구 최종 결과를 찾는다.
    """
    if not isinstance(text_options, list) or not text_options:
        return None

    for option in reversed(text_options):
        text = str(option.get('text', '')).strip()
        current_game_state = option.get('currentGameState', {})

        pitcher = str(current_game_state.get('pitcher', '')).strip()
        batter = str(current_game_state.get('batter', '')).strip()

        if not text:
            continue
        if is_runner_event_text(text):
            continue
        if not pitcher or not batter:
            continue

        result_type = get_result_type(text)
        if result_type in ['bb', 'hbp']:
            return {
                'result_type': result_type,
                'text': text,
                'pitcher': pitcher,
                'batter': batter
            }

    return None


def extract_walks_from_one_inning(
    relay_data,
    inning,
    away_starter_pcode,
    home_starter_pcode,
    batter_code_name_map
):
    away_walks = []
    home_walks = []

    text_relays = relay_data.get('result', {}).get('textRelayData', {}).get('textRelays', [])

    for relay in text_relays:
        title = str(relay.get('title', '')).strip()
        text_options = relay.get('textOptions', [])

        final_result = find_final_batter_result(text_options)
        if not final_result:
            continue

        pitcher_code = str(final_result.get('pitcher', '')).strip()
        batter_code = str(final_result.get('batter', '')).strip()
        text = str(final_result.get('text', '')).strip()
        result_type = final_result.get('result_type', '')

        batter_name = batter_code_name_map.get(batter_code, '')

        row = {
            'inning': inning,
            'pitcher_code': pitcher_code,
            'batter_code': batter_code,
            'batter_name': batter_name,
            'title': title,
            'text': text,
            'result_type': result_type
        }

        if pitcher_code == str(away_starter_pcode):
            away_walks.append(row)

        elif pitcher_code == str(home_starter_pcode):
            home_walks.append(row)

    return away_walks, home_walks


def is_inning_start_title(title):
    """
    예: '2회초 한화 공격', '3회말 LG 공격'
    """
    title = str(title).strip()
    return ('회초' in title or '회말' in title) and ('공격' in title)


def get_first_pitch_results_of_inning(relay_data, inning, batter_code_name_map):
    results = []

    text_relays = relay_data.get('result', {}).get('textRelayData', {}).get('textRelays', [])

    for i in range(len(text_relays)):
        title = str(text_relays[i].get('title', '')).strip()

        if not is_inning_start_title(title):
            continue

        # 다음 index = 첫 타자
        batter_idx = i - 1
        if batter_idx < 0:
            continue

        batter_relay = text_relays[batter_idx]
        text_options = batter_relay.get('textOptions', [])

        for option in text_options:
            if option.get('pitchNum') == 1:
                current_game_state = option.get('currentGameState', {})
                batter_code = str(current_game_state.get('batter', '')).strip()

                results.append({
                    'inning': inning,
                    'title': title,
                    'batter_code': batter_code,
                    'batter_name': batter_code_name_map.get(batter_code, ''),
                    'pitchResult': option.get('pitchResult', ''),
                    'text': option.get('text', ''),
                    'stuff': option.get('stuff', ''),
                    'speed': option.get('speed', '')
                })

                break

    return results


def extract_inning_results(player_dict, max_inning=25):
    """
    inn1 ~ inn25 중 빈값이 아닌 것만 dict로 반환
    예:
    {'inn1': '우안', 'inn3': '삼진', 'inn7': '4구'}
    """
    inning_results = {}

    for i in range(1, max_inning + 1):
        key = f'inn{i}'
        value = str(player_dict.get(key, '')).strip()

        if value != '':
            inning_results[key] = value

    return inning_results


def extract_batters_boxscore_rows(record_data, game_date, game_id, team_type, team_name):
    """
    battersBoxscore의 away/home 전체 선수 기본 스탯을 row 단위로 추출
    """
    rows = []
    batters = record_data.get('battersBoxscore', {}).get(team_type, [])

    for batter in batters:
        row = {
            'game_date': game_date,
            'game_id': game_id,
            'team_type': team_type,
            'team_name': team_name,

            'playerCode': batter.get('playerCode', ''),
            'name': batter.get('name', ''),
            'pos': batter.get('pos', ''),
            'batOrder': batter.get('batOrder', ''),
            'hasPlayerEnd': batter.get('hasPlayerEnd', ''),

            'ab': batter.get('ab', ''),
            'bb': batter.get('bb', ''),
            'hit': batter.get('hit', ''),
            'kk': batter.get('kk', ''),
            'hr': batter.get('hr', ''),
            'rbi': batter.get('rbi', ''),
            'run': batter.get('run', ''),
            'sb': batter.get('sb', ''),
            'hra': batter.get('hra', ''),

            'inning_results': extract_inning_results(batter)
        }

        rows.append(row)

    return rows


def extract_batter_inning_event_rows(record_data, game_date, game_id, team_type, team_name):
    """
    inn1 ~ inn25의 빈칸이 아닌 값만 개별 행으로 길게 펼쳐서 추출
    """
    rows = []
    batters = record_data.get('battersBoxscore', {}).get(team_type, [])

    for batter in batters:
        for i in range(1, 26):
            key = f'inn{i}'
            value = str(batter.get(key, '')).strip()

            if value == '':
                continue

            rows.append({
                'game_date': game_date,
                'game_id': game_id,
                'team_type': team_type,
                'team_name': team_name,

                'playerCode': batter.get('playerCode', ''),
                'name': batter.get('name', ''),
                'pos': batter.get('pos', ''),
                'batOrder': batter.get('batOrder', ''),

                'inning': i,
                'inning_key': key,
                'result': value
            })

    return rows

def extract_team_batting_total_rows(record_data, game_date, game_id, away_team, home_team):
    """
    battersBoxscore의 awayTotal, homeTotal 팀 합계 스탯 추출
    """
    rows = []
    batters_boxscore = record_data.get('battersBoxscore', {})

    away_total = batters_boxscore.get('awayTotal', {})
    home_total = batters_boxscore.get('homeTotal', {})

    if away_total:
        rows.append({
            'game_date': game_date,
            'game_id': game_id,
            'team_type': 'away',
            'team_name': away_team,
            'opponent_team': home_team,
            'ab': away_total.get('ab', ''),
            'hit': away_total.get('hit', ''),
            'hra': away_total.get('hra', ''),
            'rbi': away_total.get('rbi', ''),
            'run': away_total.get('run', ''),
            'sb': away_total.get('sb', '')
        })

    if home_total:
        rows.append({
            'game_date': game_date,
            'game_id': game_id,
            'team_type': 'home',
            'team_name': home_team,
            'opponent_team': away_team,
            'ab': home_total.get('ab', ''),
            'hit': home_total.get('hit', ''),
            'hra': home_total.get('hra', ''),
            'rbi': home_total.get('rbi', ''),
            'run': home_total.get('run', ''),
            'sb': home_total.get('sb', '')
        })

    return rows

def run_kbo_build():


    create_tables()


    response = requests.get(
        'https://api-gw.sports.naver.com/schedule/games',
        params=params,
        headers=headers
    )

    TEST_GAME_ID =None

    games = response.json()['result']['games']

    all_rows = []
    first_pitch_rows = []
    all_batter_rows = []
    all_batter_event_rows = []
    all_team_total_rows = []
    all_starting_lineup_rows = []
    all_starting_pitcher_stat_rows = []
    all_game_flow_summary_rows = []

    for game in games:
        game_id = game.get('gameId', '')
        if TEST_GAME_ID and game_id != TEST_GAME_ID:
            continue
        game_date = game.get('gameDate', '')
        home_team = game.get('homeTeamName', '')
        away_team = game.get('awayTeamName', '')
        home_starting = game.get('homeStarterName', '')
        away_starting = game.get('awayStarterName', '')
        status_code = str(game.get('statusCode', '')).strip()
        round_code = str(game.get('roundCode', '')).strip().lower()



        dprint('=' * 80)
        dprint('game_id     :', game_id)
        dprint('game_date   :', game_date)
        dprint('away_team   :', away_team)
        dprint('home_team   :', home_team)
        dprint('away_start  :', away_starting)
        dprint('home_start  :', home_starting)
        dprint('status_code :', status_code)
        dprint('round_code  :', round_code)


        if status_code != 'RESULT':
            dprint('RESULT 경기 아님 -> 스킵')
            continue

        if round_code == 'kbo_e':
            dprint('시범경기(kbo_e) -> 스킵')
            continue

        # 시범경기 제외
        # if round_code == 'kbo_e':
        #     continue
        # 끝난경기만 포함
        # if status_code != 'RESULT':
        #     continue

        record_url = f'https://api-gw.sports.naver.com/schedule/games/{game_id}/record'
        record_response = requests.get(record_url, headers=headers)
        record_json = record_response.json()

        if 'result' not in record_json or 'recordData' not in record_json['result']:
            continue

        record_data = record_json['result']['recordData']

        dprint('record_json keys:', record_json.keys())
        dprint('result keys:', record_json.get('result', {}).keys())
        dprint('record_data keys:', record_data.keys())

        # 팀 타격 합계 row (awayTotal, homeTotal)
        team_total_rows = extract_team_batting_total_rows(
            record_data=record_data,
            game_date=game_date,
            game_id=game_id,
            away_team=away_team,
            home_team=home_team
        )

        all_team_total_rows.extend(team_total_rows)

        # 타자 기본 스탯 row
        away_batter_rows = extract_batters_boxscore_rows(
            record_data=record_data,
            game_date=game_date,
            game_id=game_id,
            team_type='away',
            team_name=away_team
        )

        home_batter_rows = extract_batters_boxscore_rows(
            record_data=record_data,
            game_date=game_date,
            game_id=game_id,
            team_type='home',
            team_name=home_team
        )

        all_batter_rows.extend(away_batter_rows)
        all_batter_rows.extend(home_batter_rows)

        # 타자 이닝별 이벤트 row
        away_batter_event_rows = extract_batter_inning_event_rows(
            record_data=record_data,
            game_date=game_date,
            game_id=game_id,
            team_type='away',
            team_name=away_team
        )

        home_batter_event_rows = extract_batter_inning_event_rows(
            record_data=record_data,
            game_date=game_date,
            game_id=game_id,
            team_type='home',
            team_name=home_team
        )


        

        all_batter_event_rows.extend(away_batter_event_rows)
        all_batter_event_rows.extend(home_batter_event_rows)


        away_pitchers = record_data.get('pitchersBoxscore', {}).get('away', [])
        home_pitchers = record_data.get('pitchersBoxscore', {}).get('home', [])

        dprint('away_pitchers len:', len(away_pitchers))
        dprint('home_pitchers len:', len(home_pitchers))
        dprint('away_pitchers[0]:', away_pitchers[0] if away_pitchers else '없음')
        dprint('home_pitchers[0]:', home_pitchers[0] if home_pitchers else '없음')

        if not away_pitchers or not home_pitchers:
            continue

        away_pitcher = away_pitchers[0]
        home_pitcher = home_pitchers[0]

        starting_pitcher_stat_row = extract_starting_pitcher_stats_row(
        game_id=game_id,
        game_date=game_date,
        away_team=away_team,
        home_team=home_team,
        away_pitcher=away_pitcher,
        home_pitcher=home_pitcher
        )
        all_starting_pitcher_stat_rows.append(starting_pitcher_stat_row)

        game_flow_summary_row = extract_game_flow_summary_row(
            record_data=record_data,
            game_id=game_id,
            game_date=game_date,
            away_team=away_team,
            home_team=home_team,
            away_pitcher=away_pitcher,
            home_pitcher=home_pitcher
        )
        all_game_flow_summary_rows.append(game_flow_summary_row)

        kor_away_pitcher_record = {
            'name': away_pitcher.get('name', away_starting),
            'inn': away_pitcher.get('inn', ''),
            'hit': away_pitcher.get('hit', ''),
            'r': away_pitcher.get('r', ''),
            'kk': away_pitcher.get('kk', ''),
            'bb': away_pitcher.get('bb', ''),
            'ab': away_pitcher.get('ab', ''),
            'bf': away_pitcher.get('bf', ''),
            'era': away_pitcher.get('era', ''),
            'w_l': away_pitcher.get('wls', ''),
            'pcode': str(away_pitcher.get('pcode', away_pitcher.get('playerCode', ''))).strip()
        }

        kor_home_pitcher_record = {
            'name': home_pitcher.get('name', home_starting),
            'inn': home_pitcher.get('inn', ''),
            'hit': home_pitcher.get('hit', ''),
            'r': home_pitcher.get('r', ''),
            'kk': home_pitcher.get('kk', ''),
            'bb': home_pitcher.get('bb', ''),
            'ab': home_pitcher.get('ab', ''),
            'bf': home_pitcher.get('bf', ''),
            'era': home_pitcher.get('era', ''),
            'w_l': home_pitcher.get('wls', ''),
            'pcode': str(home_pitcher.get('pcode', home_pitcher.get('playerCode', ''))).strip()
        }

        away_starter_pcode = kor_away_pitcher_record['pcode']
        home_starter_pcode = kor_home_pitcher_record['pcode']

        if not away_starter_pcode or not home_starter_pcode:
            continue

        insert_game(
            game_id=game_id,
            game_date=game_date,
            league='kbo',
            round_code=round_code,
            status_code=status_code,
            away_team=away_team,
            home_team=home_team,
            away_starter_name=away_starting,
            home_starter_name=home_starting,
            away_starter_pcode=away_starter_pcode,
            home_starter_pcode=home_starter_pcode
        )

        dprint('[DB 저장] games:', game_id, away_team, 'vs', home_team)

        away_search_end_inning = get_search_end_inning(kor_away_pitcher_record['inn'])
        home_search_end_inning = get_search_end_inning(kor_home_pitcher_record['inn'])
        max_search_inning = max(away_search_end_inning, home_search_end_inning)

        if max_search_inning == 0:
            continue

        batter_code_name_map = make_batter_code_name_map(record_data)

        away_walks_all = []
        home_walks_all = []

        print('=' * 100)
        print(f'{game_date}  {away_team} vs {home_team}')
        print()

        for inning in range(1, max_search_inning + 1):
            relay_url = f'https://api-gw.sports.naver.com/schedule/games/{game_id}/relay?inning={inning}'
            relay_response = requests.get(relay_url, headers=headers)

            try:
                relay_data = relay_response.json()
            except:
                continue

            # 1회 relay에서 선발타자 추출 (경기당 1번)
            if inning == 1:
                starting_lineup_rows = extract_starting_lineup_rows(
                    relay_data=relay_data,
                    game_date=game_date,
                    game_id=game_id,
                    away_team=away_team,
                    home_team=home_team
                )

                all_starting_lineup_rows.extend(starting_lineup_rows)

                dprint('[선발타자 추출]')
                for row in starting_lineup_rows:
                    dprint(row['team_type'], row['batOrder'], row['name'], row['pcode'])

            dprint('inning:', inning)
            dprint('relay result keys:', relay_data.get('result', {}).keys())
            dprint('textRelayData keys:', relay_data.get('result', {}).get('textRelayData', {}).keys())

            text_relays = relay_data.get('result', {}).get('textRelayData', {}).get('textRelays', [])
            dprint('text_relays len:', len(text_relays))

            for idx, relay in enumerate(text_relays[:5]):
                dprint(f'text_relays[{idx}] title:', relay.get('title', ''))

            if inning == 1:
                dprint('----- relay titles / textOptions raw -----')
                for relay in text_relays:
                    title = str(relay.get('title', '')).strip()
                    text_options = relay.get('textOptions', [])

                    dprint(f'[title] {title}')
                    for option in text_options:
                        dprint('   text:', option.get('text', ''))

            away_walks, home_walks = extract_walks_from_one_inning(
                relay_data=relay_data,
                inning=inning,
                away_starter_pcode=away_starter_pcode,
                home_starter_pcode=home_starter_pcode,
                batter_code_name_map=batter_code_name_map
            )

            away_walks_all.extend(away_walks)
            home_walks_all.extend(home_walks)

            first_pitch_list = get_first_pitch_results_of_inning(
                relay_data=relay_data,
                inning=inning,
                batter_code_name_map=batter_code_name_map
            )

            for fp in first_pitch_list:
                print(
                    f'{inning}회 -> {fp["batter_name"]} / {fp["pitchResult"]} / {fp["text"]}'
                )

                first_pitch_rows.append({
                    'game_date': game_date,
                    'game_id': game_id,
                    'inning': inning,
                    'away_team': away_team,
                    'home_team': home_team,
                    'batter_name': fp['batter_name'],
                    'batter_code': fp['batter_code'],
                    'title': fp['title'],
                    'pitchResult': fp['pitchResult'],
                    'text': fp['text'],
                    'stuff': fp['stuff'],
                    'speed': fp['speed']
                })

        away_official_bbhb = safe_int(kor_away_pitcher_record['bb'], 0)
        home_official_bbhb = safe_int(kor_home_pitcher_record['bb'], 0)

        away_walks_all = away_walks_all[:away_official_bbhb]
        home_walks_all = home_walks_all[:home_official_bbhb]

        print()
        print(f'[원정 선발] {kor_away_pitcher_record["name"]}')
        print(f'이닝: {kor_away_pitcher_record["inn"]} / 공식 BB: {kor_away_pitcher_record["bb"]}')
        if away_walks_all:
            for row in away_walks_all:
                print(f'  {row["inning"]}회 - {row["batter_name"]} - {row["result_type"]} - {row["text"]}')
                all_rows.append({
                    'game_date': game_date,
                    'game_id': game_id,
                    'team_type': 'away',
                    'pitcher_name': kor_away_pitcher_record['name'],
                    'pitcher_pcode': away_starter_pcode,
                    'pitcher_inn': kor_away_pitcher_record['inn'],
                    'pitcher_bb': kor_away_pitcher_record['bb'],
                    'walk_inning': row['inning'],
                    'batter_name': row['batter_name'],
                    'batter_code': row['batter_code'],
                    'result_type': row['result_type'],
                    'text': row['text'],
                    'away_team': away_team,
                    'home_team': home_team
                })
        else:
            print('  없음')

        print(f'추출 BB/HBP: {len(away_walks_all)}')
        print()

        print(f'[홈 선발] {kor_home_pitcher_record["name"]}')
        print(f'이닝: {kor_home_pitcher_record["inn"]} / 공식 BB: {kor_home_pitcher_record["bb"]}')
        if home_walks_all:
            for row in home_walks_all:
                print(f'  {row["inning"]}회 - {row["batter_name"]} - {row["result_type"]} - {row["text"]}')
                all_rows.append({
                    'game_date': game_date,
                    'game_id': game_id,
                    'team_type': 'home',
                    'pitcher_name': kor_home_pitcher_record['name'],
                    'pitcher_pcode': home_starter_pcode,
                    'pitcher_inn': kor_home_pitcher_record['inn'],
                    'pitcher_bb': kor_home_pitcher_record['bb'],
                    'walk_inning': row['inning'],
                    'batter_name': row['batter_name'],
                    'batter_code': row['batter_code'],
                    'result_type': row['result_type'],
                    'text': row['text'],
                    'away_team': away_team,
                    'home_team': home_team
                })
        else:
            print('  없음')

        print(f'추출 BB/HBP: {len(home_walks_all)}')
        print()



    dprint('pitcher stats rows:', len(all_starting_pitcher_stat_rows))
    dprint('summary rows:', len(all_game_flow_summary_rows))

    insert_starting_lineup_rows(all_starting_lineup_rows)
    dprint('선발타자 행 수:', len(all_starting_lineup_rows))

    insert_batter_rows(all_batter_rows)
    dprint('기본 타자 행 수:', len(all_batter_rows))

    insert_batter_inning_event_rows(all_batter_event_rows)
    dprint('타자 이닝이벤트 행 수:', len(all_batter_event_rows))

    insert_team_total_rows(all_team_total_rows)
    dprint('팀 타격합계 행 수:', len(all_team_total_rows))

    insert_first_pitch_rows(first_pitch_rows)
    dprint('첫타자 첫공 행 수:', len(first_pitch_rows))

    insert_pitcher_event_rows(all_rows)
    dprint('투수 BB/HBP 행 수:', len(all_rows))

    insert_starting_pitcher_stats_rows(all_starting_pitcher_stat_rows)
    dprint('선발투수 누적스탯 행 수:', len(all_starting_pitcher_stat_rows))

    insert_game_flow_summary_rows(all_game_flow_summary_rows)
    dprint('경기 흐름 요약 행 수:', len(all_game_flow_summary_rows))

    # 필요하면 확인용
    print('기본 타자행 수:', len(all_batter_rows))
    print('타자 이닝이벤트 행 수:', len(all_batter_event_rows))
    print('팀 타격합계 행 수:', len(all_team_total_rows))
    print('첫타자 첫공 행 수:', len(first_pitch_rows))
    print('투수 BB/HBP 행 수:', len(all_rows))






def export_one_game_to_excel(game_id, db_path='kbo.db', output_dir='exports'):
    os.makedirs(output_dir, exist_ok=True)

    conn = sqlite3.connect(db_path)

    df_games = pd.read_sql(
        "SELECT * FROM games WHERE game_id = ?",
        conn,
        params=[game_id]
    )
    df_lineups = pd.read_sql(
        "SELECT * FROM starting_lineups WHERE game_id = ? ORDER BY team_type, bat_order",
        conn,
        params=[game_id]
    )
    df_batters = pd.read_sql(
        "SELECT * FROM batters WHERE game_id = ? ORDER BY team_type, bat_order",
        conn,
        params=[game_id]
    )
    df_batter_events = pd.read_sql(
        "SELECT * FROM batter_inning_events WHERE game_id = ? ORDER BY team_type, inning, bat_order",
        conn,
        params=[game_id]
    )
    df_team_totals = pd.read_sql(
        "SELECT * FROM team_totals WHERE game_id = ? ORDER BY team_type",
        conn,
        params=[game_id]
    )
    df_first_pitch = pd.read_sql(
        "SELECT * FROM first_pitch WHERE game_id = ? ORDER BY inning",
        conn,
        params=[game_id]
    )
    df_pitcher_events = pd.read_sql(
        "SELECT * FROM pitcher_events WHERE game_id = ? ORDER BY team_type, event_inning",
        conn,
        params=[game_id]
    )
    df_starting_pitcher_stats = pd.read_sql(
        "SELECT * FROM starting_pitcher_stats WHERE game_id = ?",
        conn,
        params=[game_id]
    )
    df_game_flow_summary = pd.read_sql(
        "SELECT * FROM game_flow_summary WHERE game_id = ?",
        conn,
        params=[game_id]
    )

    conn.close()

    file_name = f'kbo_report_{game_id}.xlsx'
    output_path = os.path.join(output_dir, file_name)

    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df_games.to_excel(writer, sheet_name='games', index=False)
        df_lineups.to_excel(writer, sheet_name='starting_lineups', index=False)
        df_batters.to_excel(writer, sheet_name='batters', index=False)
        df_batter_events.to_excel(writer, sheet_name='batter_events', index=False)
        df_team_totals.to_excel(writer, sheet_name='team_totals', index=False)
        df_first_pitch.to_excel(writer, sheet_name='first_pitch', index=False)
        df_pitcher_events.to_excel(writer, sheet_name='pitcher_events', index=False)
        df_starting_pitcher_stats.to_excel(writer, sheet_name='starting_pitcher_stats', index=False)
        df_game_flow_summary.to_excel(writer, sheet_name='game_flow_summary', index=False)

    print(f'엑셀 생성 완료: {output_path}')
    return output_path
    

if __name__ == "__main__":
    run_kbo_build()
