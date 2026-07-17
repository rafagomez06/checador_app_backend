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

# @UsuariosController.route("/usuarios", methods=["GET"])
# # @jwt_required()
# def listar_usuarios():
#     return UsuariosService.listar_usuarios()


@UsuariosController.route("/login", methods=["POST"])
# @jwt_required()
def validar_login():
    data = request.get_json()
    return UsuariosService.validar_login(data)


