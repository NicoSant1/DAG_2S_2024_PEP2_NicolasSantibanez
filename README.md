# DAG_2S_2024_PEP2_NicolasSantibanez
- Entrega Pep 2 DAG 2 Semestre
- Alumno: Nicolás Santibáñez
- Profesor: Ignacio Yañez
- Ayudante: Nicolás Triviño
# Proyecto de Procesamiento de Datos Geoespaciales

## Descripción
Este proyecto tiene como objetivo procesar y cargar datos geoespaciales en una base de datos PostgreSQL/PostGIS mediante el uso de Python. A continuación, se explican los pasos para configurar, ejecutar y probar el proyecto en un entorno local.
Dicho proyecto tiene como objetivo seleccionar un servicio (como gimnasio, supermercado, clínica veterinaria, etc.) que desee instalar en una comuna de elección. Mediante uso de un modelo espacial🌐 debe determinar el o los predios óptimos para la instalación del servicio escogido.

##Proyecto escogido
Se eligió la instalación de canchas de basketball vecinales, las cuales tienen como variables para seleccionar el lugar lo que son la cantidad de personas (menos de 50) que no debe ser muy alta para asi mantener las condiciones de la cancha para los vecinos
Así como también que no se encuentren a mucha distancia de áreas verdes (<200 metros). Esto se fijó tomando en cuenta que la comuna de elección corresponde a Vitacura, una comuna con una densidad poblacional menor la mayoria y que cuenta con extensas áreas verdes.

## Requisitos
- Python 3.8 o superior.
- PostgreSQL con la extensión PostGIS habilitada.
- Sistema operativo compatible con Python y PostgreSQL (Linux, Windows o macOS).

## Instalación de Dependencias
1. Clona este repositorio en tu máquina local:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd <NOMBRE_DEL_REPOSITORIO>
   ```

2. Crea un entorno virtual y actívalo:
   ```bash
   python -m venv venv
   # En Windows
   venv\Scripts\activate
   # En macOS/Linux
   source venv/bin/activate
   ```

3. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```

## Configuración
### Archivos SHP
Actualiza las rutas de los archivos SHP en el script `main()` del archivo `codigoprueba.py`. Por ejemplo:
```python
gdf = gpd.read_file(r'C:\ruta\a\tu\archivo\Manzanas.shp')
gdf1 = gpd.read_file(r'C:\ruta\a\tu\archivo\PRC.shp')
gdf2 = gpd.read_file(r'C:\ruta\a\tu\archivo\DPA.shp')
```
Estas rutas deben apuntar a los archivos SHP que deseas procesar.

### Configuración de la Base de Datos
El archivo `config.json` contiene las credenciales de conexión a la base de datos. Debes actualizarlo con los valores correspondientes a tu entorno:
```json
{
    "database": {
        "db_type": "postgresql",
        "user": "<USUARIO>",
        "passwd": "<CONTRASEÑA>",
        "host": "<HOST>",
        "port": "<PUERTO>",
        "db": "<NOMBRE_DE_LA_BD>",
        "schema": "public"
    }
}
```

## Archivos Incluidos
### Scripts Python
- `codigoprueba.py`: Script principal que realiza el procesamiento y carga de datos.

### Archivos SQL
- `add_geometry_to_table.sql`: Crea y añade columnas geométricas a las tablas en la base de datos.
- `calculate_zones.sql`: Realiza cálculos necesarios para zonas específicas.

### Archivos de Configuración
- `config.json`: Archivo para configurar las credenciales de la base de datos.

## Datos de Ejemplo
Incluye archivos SHP de ejemplo en la carpeta `entradas/`. Estos archivos pueden ser usados para poblar la base de datos y probar la funcionalidad del script.

## Ejecución del Proyecto
1. Configura las rutas de los archivos SHP y el archivo `config.json` según lo indicado anteriormente.

2. Ejecuta el script principal:
   ```bash
   python codigoprueba.py
   ```

3. Verifica en tu base de datos que las tablas procesadas han sido creadas y pobladas correctamente.

## Ejemplo de Uso
### Entrada
Archivos SHP ubicados en la carpeta `entradas/`:
- `Manzanas.shp`
- `PRC.shp`
- `DPA.shp`

### Proceso
El script:
1. Convierte las geometrías a WKT.
2. Carga los datos en la base de datos PostgreSQL.
3. Ejecuta las consultas SQL necesarias para procesar las zonas.

### Salida
Tablas procesadas en la base de datos con las geometrías y cálculos necesarios, entregando así una tabla con las geometrías seleccionadas para la instalación de las canchas de basketball.

## Consideraciones Finales
- Asegúrate de que la extensión PostGIS esté habilitada en tu base de datos.
- Si encuentras errores, verifica la configuración de las rutas y credenciales en los archivos mencionados.


