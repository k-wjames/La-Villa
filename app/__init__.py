from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_mail import Mail

mail = Mail()
db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    mail.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    # CORS(app)
    CORS(app, resources={r"/*": {"origins": [
    "http://localhost:5173",
    "https://dev.lavilla.co.ke",
    "https://lavilla.co.ke"
]}})
    from .routes import reservation_bp
    app.register_blueprint(reservation_bp)

    with app.app_context():
        db.create_all()

    return app
