from flask import Flask
from config import DevelopmentConfig
from app.extensions import db, ma, jwt, cors


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    from app import models
    from app.routes.applications import applications_bp
    app.register_blueprint(applications_bp)

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    cors.init_app(app)

    return app