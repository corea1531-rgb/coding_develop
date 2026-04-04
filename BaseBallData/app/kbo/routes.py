from datetime import datetime
from flask import Blueprint, render_template, abort, request
from app.services.kbo_service import (
    get_today_games,
    get_game_detail_with_pitchers,
)

kbo_bp = Blueprint("kbo", __name__, template_folder="../templates")


@kbo_bp.route("/")
def kbo_index():
    date_str = request.args.get("date")

    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%d")

    games = get_today_games(date_str)
    return render_template("kbo/index.html", games=games, today=date_str)


@kbo_bp.route("/game/<game_id>")
def game_detail(game_id):
    range_type = request.args.get("range", "7")

    detail = get_game_detail_with_pitchers(game_id, limit_type=range_type)
    if not detail:
        abort(404)

    return render_template(
        "kbo/game_detail.html",
        game=detail["game"],
        away_pitcher_logs=detail["away_pitcher_logs"],
        home_pitcher_logs=detail["home_pitcher_logs"],
        selected_range=detail["selected_range"],
    )