from app.main import ConnectionDb
from app.utils.Logger import logger

from sqlalchemy import insert, text

LOG = logger()
sql_connection = ConnectionDb.alchemy_db

## Modelos de tablas de catalogos

class CatCategoriasPlatillos(sql_connection.Model):
    __tablename__ = 'CatCategoriasPlatillos'
    
    id_CatCategoriasPlatillos = sql_connection.Column(sql_connection.Integer, primary_key=True)
    nombre = sql_connection.Column(sql_connection.String(100), nullable=False)

    def __init__(self, id_CatCategoriasPlatillos, nombre=None) -> None:
        self.id_CatCategoriasPlatillos = id_CatCategoriasPlatillos
        self.nombre = nombre

    @staticmethod
    def get_listado_sp():
        sql = text(f"Exec sp_ObtenerListadoPreCapturas;")
        print(f"Consulta: {sql}")
        LOG.error(f"Consulta: {sql}")
        result = sql_connection.session.execute(sql)
        return result


    def roll_back(self):
        sql_connection.session.rollback(self)

