from flask import Blueprint, render_template

mlb_bp = Blueprint("mlb", __name__, template_folder="../templates")

@mlb_bp.route("/")
def mlb_index():
    return render_template("mlb/index.html")