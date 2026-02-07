from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    ma.init_app(app)
    CORS(app)
    from .routes import reservation_bp
    app.register_blueprint(reservation_bp)

    with app.app_context():
        db.create_all()

    return app
