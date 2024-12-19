-----CAMBIAR GEOMETRIA A TABLA MANZANAS
ALTER TABLE "Entradas"."Manzanas"
ADD COLUMN geom geometry(Geometry, 4326);

-- Ajusta el SRID si no es 4326
UPDATE "Entradas"."Manzanas"
SET geom = ST_PolygonFromText(geometry, 4326);

-- Elimina la columna de texto
ALTER TABLE "Entradas"."Manzanas"
DROP COLUMN geometry;

---AGREGA PK A MANZANAS PARA SU MANIPULACIÓN
ALTER TABLE "Entradas"."Manzanas"
ADD COLUMN id SERIAL PRIMARY KEY;

-----CAMBIAR GEOMETRIA A TABLA DPA
ALTER TABLE "Entradas"."DPA"
ADD COLUMN geom geometry(Geometry, 4326);

-- Ajusta el SRID si no es 4326
UPDATE "Entradas"."DPA"
SET geom = ST_PolygonFromText(geometry, 4326);

-- Elimina la columna de texto
ALTER TABLE "Entradas"."DPA"
DROP COLUMN geometry;

-----CAMBIAR GEOMETRIA A TABLA PRC
ALTER TABLE "Entradas"."PRC"
ADD COLUMN geom geometry(Geometry, 4326);

-- Ajusta el SRID si no es 4326
UPDATE "Entradas"."PRC"
SET geom = ST_PolygonFromText(geometry, 4326);

-- Elimina la columna de texto
ALTER TABLE "Entradas"."PRC"
DROP COLUMN geometry;

