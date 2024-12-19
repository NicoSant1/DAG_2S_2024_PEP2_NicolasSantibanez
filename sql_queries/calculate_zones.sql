-- Crear un nuevo esquema llamado "resultados"
CREATE SCHEMA IF NOT EXISTS resultados;

-- Crear una tabla para almacenar las manzanas que cumplen con las condiciones
CREATE TABLE resultados.manzanas_filtradas AS
WITH manzanas_prc AS (
    -- Intersección de la capa PRC con las manzanas
    SELECT 
        m.id AS manzana_id,
        m.geom AS manzana_geom,
        p."UPERM",
        m."TOTAL_PERS"
    FROM 
        "Entradas"."Manzanas" m
    JOIN 
        "Entradas"."PRC" p
    ON 
        ST_Intersects(m.geom, p.geom)
),
manzanas_cerca_areas_verdes AS (
    -- Identificar manzanas a menos de 200 metros de áreas verdes
    SELECT DISTINCT
        m.manzana_id
    FROM 
        manzanas_prc m
    JOIN 
        "Entradas"."PRC" p
    ON 
        ST_DWithin(m.manzana_geom, p.geom, 200)
    WHERE 
        p."UPERM" = 'Áreas verdes'
),
manzanas_final AS (
    -- Filtrar manzanas que cumplen con todas las condiciones
    SELECT 
        mp.manzana_id,
        mp.manzana_geom,
        mp."TOTAL_PERS"
    FROM 
        manzanas_prc mp
    WHERE 
        mp.manzana_id IN (SELECT manzana_id FROM manzanas_cerca_areas_verdes)
        AND mp."TOTAL_PERS" < 20
)
-- Insertar los resultados en la tabla del esquema "resultados"
SELECT 
    manzana_id,
    manzana_geom,
    "TOTAL_PERS"
FROM 
    manzanas_final;