from flask import Blueprint, render_template

npb_bp = Blueprint("npb", __name__, template_folder="../templates")

@npb_bp.route("/")
def npb_index():
    return render_template("npb/index.html")