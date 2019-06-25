DROP VIEW IF EXISTS qgep_swmm.vw_subcatchments;


--------
-- View for the swmm module class junction
-- 20190329 qgep code sprint SB, TP
--------

CREATE OR REPLACE VIEW qgep_swmm.vw_subcatchments AS

SELECT 
	replace(ca.obj_id, ' ', '_') as Name,
	'*'::varchar as RainGage,
	coalesce(fk_wastewater_networkelement_ww_current, '*') as Outlet,
	surface_area as Area,
	25 as percImperv,
	500 as Width,
	0.5 as percSlope,
	0 as CurbLen,
	NULL as SnowPack,
	ca.identifier as description,
	'catchment_area'::varchar as tag,
	ST_Simplify(ST_CurveToLine(perimeter_geometry), 20, TRUE) as geom
FROM qgep_od.catchment_area as ca
