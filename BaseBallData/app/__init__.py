from flask import Flask, render_template
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.kbo.routes import kbo_bp
    from app.npb.routes import npb_bp
    from app.mlb.routes import mlb_bp

    app.register_blueprint(kbo_bp, url_prefix="/kbo")
    app.register_blueprint(npb_bp, url_prefix="/npb")
    app.register_blueprint(mlb_bp, url_prefix="/mlb")

    @app.route("/")
    def home():
        return render_template("home.html")

    return app