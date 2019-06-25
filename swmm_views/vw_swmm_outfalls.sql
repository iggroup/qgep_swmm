DROP VIEW IF EXISTS qgep_swmm.vw_outfalls;


--------
-- View for the swmm module class outfalls
-- 20190329 qgep code sprint SB, TP
--------

CREATE OR REPLACE VIEW qgep_swmm.vw_outfalls AS

SELECT
	dp.obj_id as Name,
	coalesce(wn.bottom_level,0) as InvertElev,
	'FREE'::varchar as Type,
	NULL as StageData,
	'NO'::varchar as tide_gate,
	NULL::varchar as RouteTo,
	--st_x(wn.situation_geometry) as X_coordinate,
	--st_y(wn.situation_geometry) as Y_coordinate,
	dp.identifier as description,
	'discharge point'::varchar as tag,
	wn.situation_geometry as geom
FROM qgep_od.vw_discharge_point as dp
LEFT JOIN qgep_od.wastewater_node wn on wn.obj_id = dp.obj_id
LEFT JOIN qgep_od.wastewater_networkelement we ON we.obj_id::text = wn.obj_id::text;
