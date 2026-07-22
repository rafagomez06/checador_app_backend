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
            LOG.info(f"## Solicitud entrada: {data}\n")
            
            # Obtenemos valores de peticion
            usuario_id = data["usuario_id"]
            tipo_checada = data["tipo_checada"]
            ubicacion = data.get("ubicacion", {})

            latitud = ubicacion.get("latitud")
            longitud = ubicacion.get("longitud")
            direccion = ubicacion.get("direccionCompleta", {})

            #Extraemos valores de direccionCompleta
            direccionCompleta = direccion.get("direccionCompleta", "")

            #Envio de datos a SP
            checada_result = ChecadorModel.registrar_checada(usuario_id,tipo_checada,latitud,longitud,direccionCompleta)

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
            if estadoSQL != STATUS_CODE_200:
                LOG.info(f"Error: {mensajeSQL} ")
                # ConnectionDb.alchemy_db.session.rollback()
                return api_response(STATUS_CODE_409,{},ERROR,mensajeSQL)
            
            #Commit y Retorno de datos
            ConnectionDb.alchemy_db.session.commit()
            return api_response(STATUS_CODE_200,json_data,SUCCESS,mensajeSQL)

        except exc.StatementError as sta_err:
            error_trace = traceback.format_exc()
            LOG.error(
                f"Error al realizar la sentencia en registrar_checada:{str(sta_err)} [{error_trace}]")
            raise DatabaseError("Error al realizar la sentencia SQL")
        except exc.SQLAlchemyError as e: 
            LOG.error(f"DB error en registrar_checada: {str(e)}")
            raise DatabaseError("Error al consultar la base de datos - registrar_checada")
        except ValueError as e: 
            LOG.warning(f"Parámetro inválido: {str(e)}")
            raise UnexpectedError("Parámetros de búsqueda inválidos")
        except Exception as e:  
            error_trace = traceback.format_exc()
            LOG.error(f"Error inesperado: {str(e)} | Trace: {error_trace}")
            raise UnexpectedError("Ocurrió un error inesperado")        
        
    @staticmethod
    def obtener_historial_checadas(data):
        try:

            LOG.info(f"## rango entrada: {data}")
            
            # Obtenemos valores de peticion
            usuario_id = data["usuario_id"]
            rango_fecha_inicio = data["rango_fecha_inicio"]
            rango_fecha_fin = data["rango_fecha_fin"]

            listado_result = ChecadorModel.obtener_historial_checadas(usuario_id,rango_fecha_inicio,rango_fecha_fin)

            # Convertimos valores obtenidos
            columns = listado_result.keys()
            rows = listado_result.fetchall()

            # Validamos resultado
            if columns is None or len(rows) == 0:
                LOG.info(f"GET /historial-checadas")
                return api_response(STATUS_CODE_404, [],ERROR,ERROR_EMPTY)

            df_result = pd.DataFrame(rows, columns=columns)

            # Limpiar t_body antes de asignar nuevos valores
            t_body = []

            # Convertimos las filas de datos en una lista de diccionarios
            t_body = df_result.to_dict(orient="records")
            
            return api_response(STATUS_CODE_200,t_body,SUCCESS)

        except exc.StatementError as sta_err:
            error_trace = traceback.format_exc()
            LOG.error(
                f"Err al realizar la sentencia en obtener_historial_checadas:{str(sta_err)} [{error_trace}]")
            raise DatabaseError("Err al realizar la sentencia SQL")
        except exc.SQLAlchemyError as e: 
            LOG.error(f"DB error en obtener_historial_checadas: {str(e)}")
            raise DatabaseError("Error al consultar la base de datos - obtener_historial_checadas")
        except ValueError as e: 
            LOG.warning(f"Parámetro inválido: {str(e)}")
            raise UnexpectedError("Parámetros de búsqueda inválidos - obtener_historial_checadas")
        except Exception as e:  
            error_trace = traceback.format_exc()
            LOG.error(f"Error inesperado: {str(e)} | Trace: {error_trace}")
            raise UnexpectedError("Ocurrió un error inesperado - obtener_historial_checadas")