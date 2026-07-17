from app.main import ConnectionDb
from app.utils.Logger import logger

from sqlalchemy import insert, text

LOG = logger()
sql_connection = ConnectionDb.alchemy_db

## Modelos de tablas de catalogos

class UsuariosModel(sql_connection.Model):
    __tablename__ = 'UsuariosModel'

    id_UsuariosModel = sql_connection.Column(sql_connection.Integer, primary_key=True)
    nombre = sql_connection.Column(sql_connection.String(100), nullable=False)

    def __init__(self, id_UsuariosModel, nombre=None) -> None:
        self.id_UsuariosModel = id_UsuariosModel
        self.nombre = nombre

    @staticmethod
    def obtener_usuarios():
        sql = text(f"SELECT * FROM Usu_Usuarios;")
        print(f"Consulta: {sql}")
        LOG.info(f"Consulta: {sql}")
        result = sql_connection.session.execute(sql)
        return result
    
    @staticmethod
    def validar_login(usuario,password):
        sql = text(f"EXEC sp_ValidarUsuariosSistema @UsuarioSistema='{usuario}',@PasswordSistema='{password}';")
        print(f"Consulta: {sql}")
        LOG.info(f"Consulta: {sql}")
        result = sql_connection.session.execute(sql)
        return result


    def roll_back(self):
        sql_connection.session.rollback(self)

