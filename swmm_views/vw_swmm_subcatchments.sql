DROP VIEW IF EXISTS qgep_swmm.vw_subcatchments;


--------
-- View for the swmm module class junction
-- 20190329 qgep code sprint SB, TP
--------

CREATE OR REPLACE VIEW qgep_swmm.vw_subcatchments AS

SELECT 
	replace(ca.obj_id, ' ', '_') as Name,
	'default_qgep_raingage' as RainGage, --'*'::varchar as RainGage,
	coalesce(fk_wastewater_networkelement_ww_current, 'default_qgep_node') as Outlet,
	surface_area as Area,
	25 as percImperv,
	500 as Width,
	0.5 as percSlope,
	0 as CurbLen,
	NULL as SnowPack,
	ca.identifier as description,
	ca.obj_id as tag,
	ST_Simplify(ST_CurveToLine(perimeter_geometry), 5, TRUE) as geom
FROM qgep_od.catchment_area as ca
