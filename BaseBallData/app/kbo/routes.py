from datetime import datetime
from flask import Blueprint, render_template, abort
from app.services.kbo_service import get_today_games, get_game_basic_info

kbo_bp = Blueprint("kbo", __name__, template_folder="../templates")


@kbo_bp.route("/")
def kbo_index():
    today_str = datetime.now().strftime("%Y-%m-%d")
    games = get_today_games(today_str)
    return render_template("kbo/index.html", games=games, today=today_str)


@kbo_bp.route("/game/<game_id>")
def game_detail(game_id):
    game = get_game_basic_info(game_id)
    if not game:
        abort(404)

    return render_template("kbo/game_detail.html", game=game)