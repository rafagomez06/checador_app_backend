from app.main import ConnectionDb
from app.utils.Logger import logger

from sqlalchemy import insert, text

LOG = logger()
sql_connection = ConnectionDb.alchemy_db

## Modelos de tablas de catalogos

class ChecadorModel(sql_connection.Model):
    __tablename__ = 'ChecadorModel'

    id_ChecadorModel = sql_connection.Column(sql_connection.Integer, primary_key=True)
    nombre = sql_connection.Column(sql_connection.String(100), nullable=False)

    def __init__(self, id_ChecadorModel, nombre=None) -> None:
        self.id_ChecadorModel = id_ChecadorModel
        self.nombre = nombre

    @staticmethod
    def registrar_checada(usuario_id,latitud,longitud):
        sql = text(f"EXEC sp_RegistrarChecada @UsuarioSistema='{usuario_id}',@Latitud={latitud},@Longitud={longitud};")
        print(f"Consulta ######: {sql}")
        LOG.info(f"Consulta: {sql}")
        result = sql_connection.session.execute(sql)
        
        return result


    def roll_back(self):
        sql_connection.session.rollback(self)

