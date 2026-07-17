from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.utils.Messages import *
from app.utils.Logger import logger
from app.services.ChecadorService import ChecadorService


LOG = logger()
ChecadorController  = Blueprint("checador", __name__)

# #####################################
# Rutas privadas (JWT)
# #####################################

# @ChecadorController.route("/usuarios", methods=["GET"])
# # @jwt_required()
# def listar_usuarios():
#     return UsuariosService.listar_usuarios()


@ChecadorController.route("/registrar-checada", methods=["POST"])
# @jwt_required()
def registrar_checada():
    data = request.get_json()
    return ChecadorService.registrar_checada(data)


