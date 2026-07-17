from app.models.UsuariosModel import UsuariosModel
from app.utils.response import api_response
from app.utils.RaiseException import UnexpectedError
from app.utils.Logger import logger
import traceback
import json
import pandas as pd
from app.utils.RaiseException import ( DatabaseError,  UnexpectedError)
from app.utils.Messages import *
from sqlalchemy import exc

LOG = logger()

class UsuariosService:
    @staticmethod
    def listar_usuarios():
        try:

            listado_result = UsuariosModel.obtener_usuarios()

            # Convertimos valores obtenidos
            columns = listado_result.keys()
            rows = listado_result.fetchall()
            df_result = pd.DataFrame(rows, columns=columns)
            json_result = df_result.to_json(orient="records")
            
            # Procesar el resultado del SP
            json_data = json.loads(json_result)
            # primer_elemento_sql = json_data[0]
            # estadoSQL = primer_elemento_sql.get('estatus')
            # mensajeSQL = primer_elemento_sql.get('mensaje')

            # # si SP falla se retorna su respuesta
            # if estadoSQL != 200:
            #     LOG.info(f"Error: {mensajeSQL} ")
            #     return api_response(409, {"Error": mensajeSQL})

            # # Limpiar t_body antes de asignar nuevos valores
            # t_body = []

            # # Convertimos las filas de datos en una lista de diccionarios
            # t_body = df_result.to_dict(orient="records")

            if not listado_result:
                LOG.warning(f"GET /usuarios-sistema")
                return api_response(STATUS_CODE_404, None,ERROR,ERROR_EMPTY)
            
            return api_response(STATUS_CODE_200,json_data,SUCCESS)

        except exc.StatementError as sta_err:
            error_trace = traceback.format_exc()
            LOG.error(
                f"Err al realizar la sentencia en obtener_usuarios:{str(sta_err)} [{error_trace}]")
            raise DatabaseError("Err al realizar la sentencia SQL")
        except exc.SQLAlchemyError as e: 
            LOG.error(f"DB error en obtener_usuarios: {str(e)}")
            raise DatabaseError("Error al consultar la base de datos")
        except ValueError as e: 
            LOG.warning(f"Parámetro inválido: {str(e)}")
            raise UnexpectedError("Parámetros de búsqueda inválidos")
        except Exception as e:  
            error_trace = traceback.format_exc()
            LOG.error(f"Error inesperado: {str(e)} | Trace: {error_trace}")
            raise UnexpectedError("Ocurrió un error inesperado")
        
    @staticmethod
    def validar_login(data):
        try:
            LOG.info(data)
            # Obtenemos valores 
            usuario = data["usuario"].strip()
            password = data["password"].strip()
            
            valida_result = UsuariosModel.validar_login(usuario,password)

            # Convertimos valores obtenidos
            columns = valida_result.keys()
            rows = valida_result.fetchall()
            df_result = pd.DataFrame(rows, columns=columns)
            json_result = df_result.to_json(orient="records")
            
            # Procesar el resultado del SP
            json_data = json.loads(json_result)
            primer_elemento_sql = json_data[0]
            estadoSQL = primer_elemento_sql.get('estatus')
            mensajeSQL = primer_elemento_sql.get('mensaje')

            # si SP falla se retorna su respuesta
            if estadoSQL != 200:
                LOG.info(f"Error: {mensajeSQL} ")
                return api_response(STATUS_CODE_401, {},mensajeSQL)

            if not valida_result:
                LOG.warning(f"POST /validar-login")
                return api_response(STATUS_CODE_404, None,ERROR,ERROR_EMPTY)
            
            return api_response(STATUS_CODE_200,json_data,SUCCESS)

        except exc.StatementError as sta_err:
            error_trace = traceback.format_exc()
            LOG.error(
                f"Err al realizar la sentencia en obtener_usuarios:{str(sta_err)} [{error_trace}]")
            raise DatabaseError("Err al realizar la sentencia SQL")
        except exc.SQLAlchemyError as e: 
            LOG.error(f"DB error en obtener_usuarios: {str(e)}")
            raise DatabaseError("Error al consultar la base de datos")
        except ValueError as e: 
            LOG.warning(f"Parámetro inválido: {str(e)}")
            raise UnexpectedError("Parámetros de búsqueda inválidos")
        except Exception as e:  
            error_trace = traceback.format_exc()
            LOG.error(f"Error inesperado: {str(e)} | Trace: {error_trace}")
            raise UnexpectedError("Ocurrió un error inesperado")        