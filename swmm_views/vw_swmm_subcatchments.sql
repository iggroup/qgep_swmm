DROP VIEW IF EXISTS qgep_swmm.vw_subcatchments;


--------
-- View for the swmm module class junction
-- 20190329 qgep code sprint SB, TP
--------

CREATE OR REPLACE VIEW qgep_swmm.vw_subcatchments AS

SELECT 
	ca.obj_id as Name,
	'*'::varchar as RainGage,
	fk_wastewater_networkelement_ww_current as Outlet,
	surface_area as Area,
	25 as percImperv,
	500 as Width,
	0.5 as percSlope,
	0 as CurbLen,
	NULL as SnowPack,
	st_x(st_centroid(perimeter_geometry)) as X_coordinate,
	st_y(st_centroid(perimeter_geometry)) as Y_coordinate,
	ca.identifier as description,
	'catchment_area'::varchar as tag,
	ST_Simplify(ST_CurveToLine(perimeter_geometry), 20, TRUE) as geom
FROM qgep_od.catchment_area as ca