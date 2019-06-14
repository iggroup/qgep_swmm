rem PARAMETERS
set DIR=S:\2_INTERNE_SION\0_COLLABORATEURS\PRODUIT_Timothee\02_work\qgep_swmm\swmm_views
set PGSERVICE=pg_qgep_demo_data

rem create schema
rem psql -v ON_ERROR_STOP=on -f "%DIR%\vw_swmm_create_schema.sql" "service=%PGSERVICE%" 

rem create views
rem psql -v ON_ERROR_STOP=on -f "%DIR%\vw_swmm_conduits.sql" "service=%PGSERVICE%" 
rem psql -v ON_ERROR_STOP=on -f "%DIR%\vw_swmm_dividers.sql" "service=%PGSERVICE%" 
rem psql -v ON_ERROR_STOP=on -f "%DIR%\vw_swmm_junctions.sql" "service=%PGSERVICE%" 
rem psql -v ON_ERROR_STOP=on -f "%DIR%\vw_swmm_outfalls.sql" "service=%PGSERVICE%" 
rem psql -v ON_ERROR_STOP=on -f "%DIR%\vw_swmm_pumps.sql" "service=%PGSERVICE%" 
rem psql -v ON_ERROR_STOP=on -f "%DIR%\vw_swmm_storages.sql" "service=%PGSERVICE%" 
rem psql -v ON_ERROR_STOP=on -f "%DIR%\vw_swmm_subcatchment.sql" "service=%PGSERVICE%" 
rem psql -v ON_ERROR_STOP=on -f "%DIR%\vw_swmm_xsections.sql" "service=%PGSERVICE%" 

rem drop copies if exists
psql -v ON_ERROR_STOP=on -c "DROP TABLE IF EXISTS qgep_swmm.conduits_copy" 
psql -v ON_ERROR_STOP=on -c "DROP TABLE IF EXISTS qgep_swmm.dividers_copy" 
psql -v ON_ERROR_STOP=on -c "DROP TABLE IF EXISTS qgep_swmm.junctions_copy" 
psql -v ON_ERROR_STOP=on -c "DROP TABLE IF EXISTS qgep_swmm.outfalls_copy" 
psql -v ON_ERROR_STOP=on -c "DROP TABLE IF EXISTS qgep_swmm.pumps_copy" 
psql -v ON_ERROR_STOP=on -c "DROP TABLE IF EXISTS qgep_swmm.storages_copy" 
psql -v ON_ERROR_STOP=on -c "DROP TABLE IF EXISTS qgep_swmm.subcatchment_copy" 
psql -v ON_ERROR_STOP=on -c "DROP TABLE IF EXISTS qgep_swmm.xsections_copy" 

rem copy data from the views into tables
psql -v ON_ERROR_STOP=on -c "CREATE TABLE qgep_swmm.conduits_copy AS TABLE qgep_swmm.vw_conduits" 
psql -v ON_ERROR_STOP=on -c "CREATE TABLE qgep_swmm.dividers_copy AS TABLE qgep_swmm.vw_dividers" 
psql -v ON_ERROR_STOP=on -c "CREATE TABLE qgep_swmm.junctions_copy AS TABLE qgep_swmm.vw_junctions" 
psql -v ON_ERROR_STOP=on -c "CREATE TABLE qgep_swmm.outfalls_copy AS TABLE qgep_swmm.vw_outfalls" 
psql -v ON_ERROR_STOP=on -c "CREATE TABLE qgep_swmm.pumps_copy AS TABLE qgep_swmm.vw_pumps" 
psql -v ON_ERROR_STOP=on -c "CREATE TABLE qgep_swmm.storages_copy AS TABLE qgep_swmm.vw_storages" 
psql -v ON_ERROR_STOP=on -c "CREATE TABLE qgep_swmm.subcatchment_copy AS TABLE qgep_swmm.vw_subcatchment" 
psql -v ON_ERROR_STOP=on -c "CREATE TABLE qgep_swmm.xsections_copy AS TABLE qgep_swmm.vw_xsections" 

pause