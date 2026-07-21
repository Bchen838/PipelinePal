from flask import Flask, jsonify
from config import DevelopmentConfig, ProductionConfig
from marshmallow import ValidationError
from app.extensions import db, ma, jwt, cors
import os


def create_app():
    app = Flask(__name__)

    
    config = ProductionConfig if os.environ.get('FLASK_ENV') == 'production' else DevelopmentConfig
    app.config.from_object(config)
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    from app import models
    with app.app_context():
        db.create_all()

    from app.routes.applications import applications_bp
    app.register_blueprint(applications_bp)

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)


    if os.environ.get('FLASK_ENV') == 'production':
        cors.init_app(app, origins=[os.environ.get('FRONTEND_URL')])
    else:
        cors.init_app(app, origins=['http://localhost:5173'])


    @app.errorhandler(ValidationError)
    def error_handler(err):
        return jsonify({'message': err.messages}), 400


    return app