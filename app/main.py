import os
from datetime import datetime
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS

# Extensiones se instancian sin app (patron Application Factory)
db      = SQLAlchemy()
migrate = Migrate()
jwt     = JWTManager()
bcrypt  = Bcrypt()

class ConnectionDb:
    _instance = None
    alchemy_db = db

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

def create_app(env: str = "default") -> Flask:
    from app.config import config

    app = Flask(__name__)

    app.config.from_object(config[env])
    app.json.sort_keys = False
    # Inicializar extensiones 
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    CORS(app, origins=["http://localhost:3000"])   # Consumo de Front en desarrollo
    URL_PREFIX = '/api/v1'

    # Registrar Rutas de entrada 
    from app.controllers.UsuariosController import UsuariosController
    from app.controllers.ChecadorController import ChecadorController

    # Rutas Endpoints
    app.register_blueprint(UsuariosController, url_prefix=f"{URL_PREFIX}/auth")
    app.register_blueprint(ChecadorController, url_prefix=f"{URL_PREFIX}/checador")


    # Manejadores de errores globales 
    _register_error_handlers(app)

    # HEALT CHECK ENDPOINT
    @app.route('/api/v1/health', methods=['GET'])
    def health_check():
        return jsonify({
            "status": "healthy",
            "service": "Checador API",
            "version": "1.0.0",
            "mensaje": "Funcionando OK",
            "timestamp": datetime.now().isoformat()
        }), 200
    
    return app



def _register_error_handlers(app: Flask):
    """Registra los manejadores de excepciones personalizadas."""
    from app.utils.RaiseException import (
        DatabaseError, MissingValueError, NotFoundError,
        UnexpectedError, UnauthorizedError, FileUploadError
    )
    from app.utils.Logger import logger
    LOG = logger()

    @app.errorhandler(DatabaseError)
    def handle_database_error(error):
        LOG.error(f"DatabaseError: {error}")
        return jsonify({"status": 500, "body": {"error": str(error)}}), 500

    @app.errorhandler(MissingValueError)
    def handle_missing_value(error):
        LOG.warning(f"MissingValueError: {error}")
        return jsonify({"status": 400, "body": {"error": str(error)}}), 400

    @app.errorhandler(NotFoundError)
    def handle_not_found(error):
        LOG.warning(f"NotFoundError: {error}")
        return jsonify({"status": 404, "body": {"error": str(error)}}), 404

    @app.errorhandler(UnauthorizedError)
    def handle_unauthorized(error):
        LOG.warning(f"UnauthorizedError: {error}")
        return jsonify({"status": 401, "body": {"error": str(error)}}), 401

    @app.errorhandler(FileUploadError)
    def handle_file_upload(error):
        LOG.error(f"FileUploadError: {error}")
        return jsonify({"status": 400, "body": {"error": str(error)}}), 400

    @app.errorhandler(UnexpectedError)
    def handle_unexpected(error):
        LOG.error(f"UnexpectedError: {error}")
        return jsonify({"status": 500, "body": {"error": "Ocurrió un error inesperado"}}), 500

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"status": 404, "body": {"error": "Ruta no encontrada"}}), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({"status": 405, "body": {"error": "Método no permitido"}}), 405
