rem PARAMETERS
set DIR=S:\2_INTERNE_SION\0_COLLABORATEURS\PRODUIT_Timothee\02_work\qgep_swmm\swmm_views
set PGSERVICE=pg_qgep_demo_data

rem create schema
psql -v ON_ERROR_STOP=on -f "%DIR%\vw_swmm_create_schema.sql" "service=%PGSERVICE%" 

rem create views
psql -v ON_ERROR_STOP=on -f "%DIR%\vw_swmm_conduits.sql" "service=%PGSERVICE%" 
psql -v ON_ERROR_STOP=on -f "%DIR%\vw_swmm_dividers.sql" "service=%PGSERVICE%" 
psql -v ON_ERROR_STOP=on -f "%DIR%\vw_swmm_junctions.sql" "service=%PGSERVICE%" 
psql -v ON_ERROR_STOP=on -f "%DIR%\vw_swmm_outfalls.sql" "service=%PGSERVICE%" 
psql -v ON_ERROR_STOP=on -f "%DIR%\vw_swmm_pumps.sql" "service=%PGSERVICE%" 
psql -v ON_ERROR_STOP=on -f "%DIR%\vw_swmm_storages.sql" "service=%PGSERVICE%" 
psql -v ON_ERROR_STOP=on -f "%DIR%\vw_swmm_subcatchments.sql" "service=%PGSERVICE%"
psql -v ON_ERROR_STOP=on -f "%DIR%\vw_swmm_subareas.sql" "service=%PGSERVICE%"
psql -v ON_ERROR_STOP=on -f "%DIR%\vw_swmm_infiltration.sql" "service=%PGSERVICE%" 
psql -v ON_ERROR_STOP=on -f "%DIR%\vw_swmm_xsections.sql" "service=%PGSERVICE%" 
psql -v ON_ERROR_STOP=on -f "%DIR%\vw_swmm_losses.sql" "service=%PGSERVICE%"
psql -v ON_ERROR_STOP=on -f "%DIR%\vw_swmm_coordinates.sql" "service=%PGSERVICE%"
psql -v ON_ERROR_STOP=on -f "%DIR%\vw_swmm_vertices.sql" "service=%PGSERVICE%"
psql -v ON_ERROR_STOP=on -f "%DIR%\vw_swmm_polygons.sql" "service=%PGSERVICE%"

rem drop copies if exists
psql -v ON_ERROR_STOP=on -c "DROP TABLE IF EXISTS qgep_swmm.conduits" 
psql -v ON_ERROR_STOP=on -c "DROP TABLE IF EXISTS qgep_swmm.dividers" 
psql -v ON_ERROR_STOP=on -c "DROP TABLE IF EXISTS qgep_swmm.junctions" 
psql -v ON_ERROR_STOP=on -c "DROP TABLE IF EXISTS qgep_swmm.outfalls" 
psql -v ON_ERROR_STOP=on -c "DROP TABLE IF EXISTS qgep_swmm.pumps" 
psql -v ON_ERROR_STOP=on -c "DROP TABLE IF EXISTS qgep_swmm.storages" 
psql -v ON_ERROR_STOP=on -c "DROP TABLE IF EXISTS qgep_swmm.subcatchments"
psql -v ON_ERROR_STOP=on -c "DROP TABLE IF EXISTS qgep_swmm.subareas"
psql -v ON_ERROR_STOP=on -c "DROP TABLE IF EXISTS qgep_swmm.infiltration" 
psql -v ON_ERROR_STOP=on -c "DROP TABLE IF EXISTS qgep_swmm.xsections"
psql -v ON_ERROR_STOP=on -c "DROP TABLE IF EXISTS qgep_swmm.losses"
psql -v ON_ERROR_STOP=on -c "DROP TABLE IF EXISTS qgep_swmm.coordinates"
psql -v ON_ERROR_STOP=on -c "DROP TABLE IF EXISTS qgep_swmm.vertices" 
psql -v ON_ERROR_STOP=on -c "DROP TABLE IF EXISTS qgep_swmm.polygons" 

rem copy data from the views into tables
psql -v ON_ERROR_STOP=on -c "CREATE TABLE qgep_swmm.conduits AS TABLE qgep_swmm.vw_conduits" 
psql -v ON_ERROR_STOP=on -c "CREATE TABLE qgep_swmm.dividers AS TABLE qgep_swmm.vw_dividers" 
psql -v ON_ERROR_STOP=on -c "CREATE TABLE qgep_swmm.junctions AS TABLE qgep_swmm.vw_junctions" 
psql -v ON_ERROR_STOP=on -c "CREATE TABLE qgep_swmm.outfalls AS TABLE qgep_swmm.vw_outfalls" 
psql -v ON_ERROR_STOP=on -c "CREATE TABLE qgep_swmm.pumps AS TABLE qgep_swmm.vw_pumps" 
psql -v ON_ERROR_STOP=on -c "CREATE TABLE qgep_swmm.storage AS TABLE qgep_swmm.vw_storages" 
psql -v ON_ERROR_STOP=on -c "CREATE TABLE qgep_swmm.subcatchments AS TABLE qgep_swmm.vw_subcatchments" 
psql -v ON_ERROR_STOP=on -c "CREATE TABLE qgep_swmm.subareas AS TABLE qgep_swmm.vw_subareas"
psql -v ON_ERROR_STOP=on -c "CREATE TABLE qgep_swmm.infiltration AS TABLE qgep_swmm.vw_infiltration" 
psql -v ON_ERROR_STOP=on -c "CREATE TABLE qgep_swmm.xsections AS TABLE qgep_swmm.vw_xsections"
psql -v ON_ERROR_STOP=on -c "CREATE TABLE qgep_swmm.losses AS TABLE qgep_swmm.vw_losses"
psql -v ON_ERROR_STOP=on -c "CREATE TABLE qgep_swmm.coordinates AS TABLE qgep_swmm.vw_coordinates"
psql -v ON_ERROR_STOP=on -c "CREATE TABLE qgep_swmm.vertices AS TABLE qgep_swmm.vw_vertices" 
psql -v ON_ERROR_STOP=on -c "CREATE TABLE qgep_swmm.polygons AS TABLE qgep_swmm.vw_polygons" 