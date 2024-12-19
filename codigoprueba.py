# Librerías
import pandas as pd
import geopandas as gpd
import sys
import json
import psycopg2
from shapely.geometry import Polygon
from sqlalchemy import create_engine
from sqlalchemy import text

# Función para transformar geometría a WKT
def transform_geometry_column(gdf, target_crs="EPSG:4326"):
    """
    Convierte la geometría en formato WKT y opcionalmente transforma al sistema de coordenadas especificado.

    Parameters:
        gdf (GeoDataFrame): GeoDataFrame con geometrías.
        target_crs (str): EPSG del sistema de coordenadas al que transformar (opcional).

    Returns:
        GeoDataFrame: GeoDataFrame con geometría en formato WKT.
    """
    if target_crs:
        if gdf.crs is None:
            raise ValueError("El GeoDataFrame no tiene un CRS definido.")
        gdf = gdf.to_crs(target_crs)
        print(f"[OK] - Geometría transformada al CRS: {target_crs}")

    # Convertir a formato WKT
    gdf["geometry"] = gdf["geometry"].apply(lambda geom: geom.wkt if geom else None)
    print("[OK] - Geometría convertida a formato WKT")
    return gdf


def execute_sql_query(mapstore_engine, sql_query):

    with mapstore_engine.connect().execution_options(autocommit=True) as con:
        con.execute(sql_query)
        con.commit()
    print("[OK] - SQL query successfully executed")

def open_sql_query(sql_file, ):

    with open("./sql_queries/" + sql_file, encoding = "utf8") as file:
        sql_query = text(file.read())
    print("[OK] - " + sql_file + " SQL file successfully opened")
    return sql_query
 
def df_to_db(df, config_data, db_object, mapstore_engine, table_name):
    """Copy the IDE DataFrames to the mapstore database.

    Args:
        df (pandas.core.frame.DataFrame): Dataframe from IDE service.
        config_data (dict): config.json parameters.
        mapstore_engine (sqlalchemy.engine.base.Engine): Mapstore DB sqlalchemy engine.
        table_name (str): Name of the output table on the mapstore's database.
    
    Raises:
        SAWarning: Did not recognize type 'geometry' of column 'geom'
    """

    df.to_sql(table_name, 
                mapstore_engine, 
                if_exists = 'replace', 
                schema = config_data[db_object]['schema'], 
                index = False)

    print("[OK] - " + table_name + " dataframe successfully copied to Mapstore database")

def connect_to_engine(db_engine, config_data, db_object):
    """Connects to sqlalchemy database engine.

    Args:
        db_engine (sqlalchemy.engine.base.Engine): SQLAlchemy database engine.
        config_data (dict): config.json parameters.
        db_object (str): Name of the DB object specified on the config.json file.

    Returns:
        sqlalchemy.engine.Connection.connect
    """

    db_type = config_data[db_object]['db_type']

    if db_type == 'postgresql':
        db_con = db_engine.connect()

    else:
        db_con = db_engine.connect().execution_options(autocommit=False)
    
    print('[OK] - SQLAlchemy connection succesfully generated')
    return db_con

def create_db_engine(config_data, db_object, db_string):
    """Creates the SQL Alchemy db engine. 

    Args:
        config_data (dict): config.json parameters.
        db_object (str): Name of the DB object specified on the config.json file.
        db_string (str):  Mapstore database connection string.
    
    Returns:
        sqlalchemy.engine.base.Engine.
    """

    try:
        db_type = config_data[db_object]['db_type']

        if db_type == 'postgresql':
            db_engine = create_engine(db_string)
            print("[OK] - SQLAlchemy engine successfully created")
            return db_engine

        else:
            conn_args={
                "TrustServerCertificate": "yes",
                "Echo": "True",
                "MARS_Connection": "yes"}

            db_engine = create_engine(db_string, connect_args=conn_args)
            print("[OK] - SQLAlchemy engine succesfully generated")
            return db_engine

    except Exception as e:
        print("[ERROR] - Creating the database connection engine")
        print(e)
        sys.exit(2)

def create_db_string(config_data, db_object):
    """Create database connection string based on the config file parameters.

    Args:
        config_data (dict): config.json parameters.
        db_object (str): Name of the DB object specified on the config.json file.

    Returns:
        str
    """

    db_string = '{}://{}:{}@{}:{}/{}'.format(
        config_data[db_object]['db_type'],
        config_data[db_object]['user'],
        config_data[db_object]['passwd'], 
        config_data[db_object]['host'], 
        config_data[db_object]['port'], 
        config_data[db_object]['db'])

    # Case if the DB is SQL Server
    if config_data[db_object]['db_type'] == 'mssql+pyodbc':
        db_string = db_string + '?driver=ODBC+Driver+17+for+SQL+Server'
    
    print("[OK] - Connection string successfully generated")
    return db_string 

def get_config(filepath=""):

    if filepath == "":
        sys.exit("[ERROR] - Config filepath empty.")

    with open(filepath) as json_file:
        data = json.load(json_file)

    if data == {}:
        sys.exit("[ERROR] - Config file is empty.")

    return data

def get_parameters(argv):

    config_filepath = argv[1]
    return config_filepath

def main(argv):
    # JSON agregado 
    argv = ["codigoprueba.py", "config.json"]

    # Obtener parámetros
    config_filepath = get_parameters(argv)

    # Leer archivo de configuración
    config_data = get_config(config_filepath)

    # Cargar shapefiles como GeoDataFrames
    gdf = gpd.read_file(r'C:\Users\nicos\Desktop\PEP\entradas\Manzanas.shp')
    gdf1 = gpd.read_file(r'C:\Users\nicos\Desktop\PEP\entradas\PRC.shp')
    gdf2 = gpd.read_file(r'C:\Users\nicos\Desktop\PEP\entradas\DPA.shp')

    # Convertir geometrías a formato WKT
    gdf = transform_geometry_column(gdf)
    gdf1 = transform_geometry_column(gdf1)
    gdf2 = transform_geometry_column(gdf2)

    # Crear cadena de conexión
    postgres_string = create_db_string(config_data, 'database')

    # Establecer conexión
    postgres_connection = create_db_engine(config_data, 'database', postgres_string)
    postgres_engine = connect_to_engine(postgres_connection, config_data, 'database')

    # Guardar los GeoDataFrames en la base de datos
    table_name = 'Manzanas'
    table_name1 = 'PRC'
    table_name2 = 'DPA'

    df_to_db(gdf, config_data, 'database', postgres_engine, table_name)
    df_to_db(gdf1, config_data, 'database', postgres_engine, table_name1)
    df_to_db(gdf2, config_data, 'database', postgres_engine, table_name2)

    # Abrir archivo SQL
    ex_query = open_sql_query("add_geometry_to_table.sql")
    ex_query1 = open_sql_query("calculate_zones.sql")

    # Ejecutar consulta SQL
    execute_sql_query(postgres_connection, ex_query)
    execute_sql_query(postgres_connection, ex_query1)

if __name__ == "__main__":
    main(sys.argv)
