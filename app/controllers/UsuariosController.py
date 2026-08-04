from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.utils.Messages import *
from app.utils.Logger import logger
from app.services.UsuariosService import UsuariosService

LOG = logger()
UsuariosController  = Blueprint("usuarios", __name__)

# #####################################
# Rutas privadas (JWT)
# #####################################

@UsuariosController.route("/login", methods=["POST"])
# @jwt_required()
def validar_login():
    data = request.get_json()
    return UsuariosService.validar_login(data)

@UsuariosController.route("/registrar-usuario", methods=["POST"])
def registrar_usuario():
    data = request.get_json()
    return UsuariosService.registrar_usuario(data)

@UsuariosController.route("/actualizar-password", methods=["PUT"])
@jwt_required()
def actualizar_password():
    data = request.get_json()
    return UsuariosService.actualizar_password(data)
