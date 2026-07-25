from app.models.UsuariosModel import UsuariosModel
from app.utils.response import api_response
from app.utils.RaiseException import UnexpectedError
from app.utils.Logger import logger
import traceback
import json
import pandas as pd
from app.utils.RaiseException import ( DatabaseError,  UnexpectedError)
from app.utils.Messages import *
from app.utils.PassConvert import set_password,check_password
from app.main import ConnectionDb

from sqlalchemy import exc

LOG = logger()

class UsuariosService:
    # Registra un nuevo usuario
    @staticmethod
    def registrar_usuario(data):
        try:
            LOG.info("registrar_usuario")
            # Obtenemos valores 
            id_empleado = data["id_empleado"]
            id_empresa = data["id_empresa"]
            usuario_checador = data["usuario_checador"].strip()
            nombre = data["nombre"].strip()
            apellido_paterno = data["apellido_paterno"].strip()
            apellido_materno = data["apellido_materno"].strip()
            password = data["password"]

            password_hash = set_password(password)
            #Envio de datos
            registrar_result = UsuariosModel.registrar_usuario(id_empleado,
                                                            id_empresa,usuario_checador,nombre
                                                            ,apellido_paterno
                                                            ,apellido_materno,password_hash)

            # Convertimos valores obtenidos
            columns = registrar_result.keys()
            rows = registrar_result.fetchall()
            df_result = pd.DataFrame(rows, columns=columns)
            json_result = df_result.to_json(orient="records")
            
            # Procesar el resultado del SP
            json_data = json.loads(json_result)
            primer_elemento_sql = json_data[0]
            estadoSQL = primer_elemento_sql.get('estatus')
            mensajeSQL = primer_elemento_sql.get('mensaje')

            # si SP falla se retorna su respuesta
            if estadoSQL != STATUS_CODE_200:
                LOG.info(f"Error: {mensajeSQL} ")
                # ConnectionDb.alchemy_db.session.rollback()
                return api_response(STATUS_CODE_400,{},ERROR,mensajeSQL)
            
            #Commit y Retorno de datos
            ConnectionDb.alchemy_db.session.commit()
            return api_response(STATUS_CODE_200,json_data,SUCCESS,mensajeSQL)

        except exc.StatementError as sta_err:
            error_trace = traceback.format_exc()
            LOG.error(
                f"Err al realizar la sentencia en registrar_usuario:{str(sta_err)} [{error_trace}]")
            raise DatabaseError("Err al realizar la sentencia SQL")
        except exc.SQLAlchemyError as e: 
            LOG.error(f"DB error en registrar_usuario: {str(e)}")
            raise DatabaseError("Error al consultar la base de datos - registrar_usuario")
        except ValueError as e: 
            LOG.warning(f"Parámetro inválido: {str(e)}")
            raise UnexpectedError("Parámetros de búsqueda inválidos")
        except Exception as e:  
            error_trace = traceback.format_exc()
            LOG.error(f"Error inesperado: {str(e)} | Trace: {error_trace}")
            raise UnexpectedError("Ocurrió un error inesperado - registrar_usuario")     

    # Valida login de usuario
    @staticmethod
    def validar_login(data):
        try:
            LOG.info("validar_login")
            # Obtenemos valores 
            usuario = data["usuario"].strip()
            password = data["password"]

            #Consultamos usuario
            password_hashSQL = UsuariosService.obtener_usuario_login(usuario)
            
            #Valida si pass es correcto
            es_pass_valido = check_password(password_hashSQL, password)

            if not es_pass_valido:
                LOG.info(f"Contraseña incorrecta para el usuario: {usuario}")
                return api_response(STATUS_CODE_400,{},ERROR,CREDENCIALES_FALLIDAS)
            
            #Validamos login
            valida_result = UsuariosModel.validar_login(usuario,password_hashSQL)

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
            if estadoSQL != STATUS_CODE_200:
                LOG.info(f"Error: {mensajeSQL} ")
                # ConnectionDb.alchemy_db.session.rollback()
                return api_response(STATUS_CODE_400,{},ERROR,mensajeSQL)
            
            #Commit y Retorno de datos
            return api_response(STATUS_CODE_200,json_data,SUCCESS,mensajeSQL)

        except exc.StatementError as sta_err:
            error_trace = traceback.format_exc()
            LOG.error(
                f"Err al realizar la sentencia en validar_login:{str(sta_err)} [{error_trace}]")
            raise DatabaseError("Err al realizar la sentencia SQL - validar_login")
        except exc.SQLAlchemyError as e: 
            LOG.error(f"DB error en validar_login: {str(e)}")
            raise DatabaseError("Error al consultar la base de datos - validar_login")
        except ValueError as e: 
            LOG.warning(f"Parámetro inválido: {str(e)}")
            raise UnexpectedError("Parámetros de búsqueda inválidos - validar_login")
        except Exception as e:  
            error_trace = traceback.format_exc()
            LOG.error(f"Error inesperado: {str(e)} | Trace: {error_trace}")
            raise UnexpectedError("Ocurrió un error inesperado - validar_login")       

    # Obtiene la pass de usuario hasheada (encriptada)
    @staticmethod
    def obtener_usuario_login(usuario):
        try:
            LOG.info("obtener_usuario_login")
            # Obtenemos valores 
            result = UsuariosModel.obtener_usuario_login(usuario)

            # Convertimos valores obtenidos
            columns = result.keys()
            rows = result.fetchall()
            df_result = pd.DataFrame(rows, columns=columns)
            json_result = df_result.to_json(orient="records")
            
            # Procesar el resultado del SP
            json_data = json.loads(json_result)
            primer_elemento_sql = json_data[0]
            estadoSQL = primer_elemento_sql.get('estatus')
            mensajeSQL = primer_elemento_sql.get('mensaje')
            password_hashSQL = primer_elemento_sql.get('password_hash')

            # si SP falla se retorna su respuesta
            if estadoSQL != STATUS_CODE_200:
                LOG.info(f"Error: {mensajeSQL} ")
                # ConnectionDb.alchemy_db.session.rollback()
                return api_response(STATUS_CODE_400,{},ERROR,mensajeSQL)
            
            print("password_hash SQL ", password_hashSQL)
            
            #Retornamos Passhasheada 
            return password_hashSQL
        except exc.StatementError as sta_err:
            error_trace = traceback.format_exc()
            LOG.error(
                f"Err al realizar la sentencia en validar_login:{str(sta_err)} [{error_trace}]")
            raise DatabaseError("Err al realizar la sentencia SQL - validar_login")
        except exc.SQLAlchemyError as e: 
            LOG.error(f"DB error en validar_login: {str(e)}")
            raise DatabaseError("Error al consultar la base de datos - validar_login")
        except ValueError as e: 
            LOG.warning(f"Parámetro inválido: {str(e)}")
            raise UnexpectedError("Parámetros de búsqueda inválidos - validar_login")
        except Exception as e:  
            error_trace = traceback.format_exc()
            LOG.error(f"Error inesperado: {str(e)} | Trace: {error_trace}")
            raise UnexpectedError("Ocurrió un error inesperado - validar_login")      
    
    # Actualizar Pass de usuario
    @staticmethod
    def actualizar_password(data):
        try:
            LOG.info("actualizar_password")
            # Obtenemos valores 
            usuario = data["usuario"].strip()
            password = data["password"]

            password_hash = set_password(password)

            #Envio de datos
            actualizar_result = UsuariosModel.actualizar_password(usuario,password_hash)

            # Convertimos valores obtenidos
            columns = actualizar_result.keys()
            rows = actualizar_result.fetchall()
            df_result = pd.DataFrame(rows, columns=columns)
            json_result = df_result.to_json(orient="records")
            
            # Procesar el resultado del SP
            json_data = json.loads(json_result)
            primer_elemento_sql = json_data[0]
            estadoSQL = primer_elemento_sql.get('estatus')
            mensajeSQL = primer_elemento_sql.get('mensaje')

            # si SP falla se retorna su respuesta
            if estadoSQL != STATUS_CODE_200:
                LOG.info(f"Error: {mensajeSQL} ")
                # ConnectionDb.alchemy_db.session.rollback()
                return api_response(STATUS_CODE_400,{},ERROR,mensajeSQL)
            
            #Commit y Retorno de datos
            ConnectionDb.alchemy_db.session.commit()
            return api_response(STATUS_CODE_200,json_data,SUCCESS,mensajeSQL)        

        except exc.StatementError as sta_err:
            error_trace = traceback.format_exc()
            LOG.error(
                f"Err al realizar la sentencia en actualizar_password:{str(sta_err)} [{error_trace}]")
            raise DatabaseError("Err al realizar la sentencia SQL")
        except exc.SQLAlchemyError as e: 
            LOG.error(f"DB error en actualizar_password: {str(e)}")
            raise DatabaseError("Error al consultar la base de datos - actualizar_password")
        except ValueError as e: 
            LOG.warning(f"Parámetro inválido: {str(e)}")
            raise UnexpectedError("Parámetros de búsqueda inválidos")
        except Exception as e:  
            error_trace = traceback.format_exc()
            LOG.error(f"Error inesperado: {str(e)} | Trace: {error_trace}")
            raise UnexpectedError("Ocurrió un error inesperado - actualizar_password")   