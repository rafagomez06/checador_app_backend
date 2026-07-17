from app.models.ChecadorModel import ChecadorModel
from app.utils.response import api_response
from app.utils.RaiseException import UnexpectedError
from app.utils.Logger import logger
import traceback
import json
import pandas as pd
from app.utils.RaiseException import ( DatabaseError,  UnexpectedError)
from app.utils.Messages import *
from sqlalchemy import exc
from app.main import ConnectionDb

LOG = logger()

class ChecadorService:
    @staticmethod
    def registrar_checada(data):
        try:
            LOG.info(f"Solicitud entrada: {data}")
            
            # Obtenemos valores de peticion
            usuario_id = data["usuario_id"]
            ubicacion = data.get("ubicacion", {})

            latitud = ubicacion.get("latitud")
            longitud = ubicacion.get("longitud")
            precision = ubicacion.get("precision")
            direccion = ubicacion.get("direccion")

            
            checada_result = ChecadorModel.registrar_checada(usuario_id,latitud,longitud)

            # Convertimos valores obtenidos
            columns = checada_result.keys()
            rows = checada_result.fetchall()
            df_result = pd.DataFrame(rows, columns=columns)
            json_result = df_result.to_json(orient="records")
            
            json_data = []
            # Procesar el resultado del SP
            json_data = json.loads(json_result)
            primer_elemento_sql = json_data[0]
            estadoSQL = primer_elemento_sql.get('estatus')
            mensajeSQL = primer_elemento_sql.get('mensaje')

            # si SP falla se retorna su respuesta
            if estadoSQL != 200:
                LOG.info(f"Error: {mensajeSQL} ")
                return api_response(STATUS_CODE_409, {},mensajeSQL)
            
            #Commit y Retorno de datos
            ConnectionDb.alchemy_db.session.commit()
            return api_response(STATUS_CODE_200,json_data,SUCCESS)

        except exc.StatementError as sta_err:
            error_trace = traceback.format_exc()
            LOG.error(
                f"Error al realizar la sentencia en registrar_checada:{str(sta_err)} [{error_trace}]")
            raise DatabaseError("Error al realizar la sentencia SQL")
        except exc.SQLAlchemyError as e: 
            LOG.error(f"DB error en registrar_checada: {str(e)}")
            raise DatabaseError("Error al consultar la base de datos")
        except ValueError as e: 
            LOG.warning(f"Parámetro inválido: {str(e)}")
            raise UnexpectedError("Parámetros de búsqueda inválidos")
        except Exception as e:  
            error_trace = traceback.format_exc()
            LOG.error(f"Error inesperado: {str(e)} | Trace: {error_trace}")
            raise UnexpectedError("Ocurrió un error inesperado")        