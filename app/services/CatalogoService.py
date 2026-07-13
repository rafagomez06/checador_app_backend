from app.models.catalogo import CatCategoriasPlatillos
from app.utils.response import api_response
from app.utils.RaiseException import UnexpectedError
from app.utils.Logger import logger
import traceback
import pandas as pd
from app.utils.RaiseException import ( DatabaseError,  UnexpectedError)
from app.utils.Messages import *
from sqlalchemy import exc

LOG = logger()

class CatalogoService:
    @staticmethod
    def listar_categorias():
        try:

            listado_result = CatCategoriasPlatillos.get_listado_sp()

            columns = listado_result.keys()
            rows = listado_result.fetchall()
            
            df_result = pd.DataFrame(rows, columns=columns)

            # Limpiar t_body antes de asignar nuevos valores
            t_body = []

            # Convertimos las filas de datos en una lista de diccionarios
            t_body = df_result.to_dict(orient="records")

            if not listado_result:
                LOG.warning(f"GET /categorias-platillos")
                return api_response(STATUS_CODE_404, None,ERROR,ERROR_EMPTY)
            
            return api_response(STATUS_CODE_200,t_body,SUCCESS)
        

        except exc.StatementError as sta_err:
            error_trace = traceback.format_exc()
            LOG.error(
                f"Err al realizar la sentencia en get_listado_sp:{str(sta_err)} [{error_trace}]")
            raise DatabaseError("Err al realizar la sentencia SQL")
        except exc.SQLAlchemyError as e: 
            LOG.error(f"DB error en listar_categorias: {str(e)}")
            raise DatabaseError("Error al consultar la base de datos")
        except ValueError as e: 
            LOG.warning(f"Parámetro inválido: {str(e)}")
            raise UnexpectedError("Parámetros de búsqueda inválidos")
        except Exception as e:  
            error_trace = traceback.format_exc()
            LOG.error(f"Error inesperado: {str(e)} | Trace: {error_trace}")
            raise UnexpectedError("Ocurrió un error inesperado")