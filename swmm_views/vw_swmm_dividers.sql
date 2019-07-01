DROP VIEW IF EXISTS qgep_swmm.vw_dividers;


--------
-- View for the swmm module class dividers
-- 20190329 qgep code sprint SB, TP
-- Question attribute Diverted Link: Name of link which receives the diverted flow. overflow > fk_overflow_to
 
--------

CREATE OR REPLACE VIEW qgep_swmm.vw_dividers AS

SELECT
	wn.obj_id as Name,
	coalesce(wn.bottom_level,0) as InvertElevation,
	'default_qgep_diverted_link' as DivertedLink ,
	'CUTOFF' as Type,
	0 as CutoffFlow,
	(co.level-wn.bottom_level) as MaxDepth,
	0 as InitDepth,
	0 as SurchargeDepth,
	0 as PondedArea,
	--st_x(wn.situation_geometry) as X_coordinate,
	--st_y(wn.situation_geometry) as Y_coordinate,
	ws.identifier as description,
	ma.obj_id as tag,
	wn.situation_geometry as geom
FROM qgep_od.manhole ma
LEFT JOIN qgep_od.wastewater_structure ws ON ws.obj_id::text = ma.obj_id::text
LEFT JOIN qgep_od.wastewater_networkelement we ON we.fk_wastewater_structure::text = ws.obj_id::text
LEFT JOIN qgep_od.wastewater_node wn on wn.obj_id = we.obj_id
LEFT JOIN qgep_od.cover co on ws.fk_main_cover = co.obj_id
WHERE function = 4798 -- separating_structure
AND wn.obj_id is not null

UNION ALL

SELECT
	wn.obj_id as Name,
	coalesce(wn.bottom_level,0) as InvertElevation,
	'default_qgep_diverted_link' as DivertedLink,
	'CUTOFF' as Type,
	0 as CutoffFlow,
	(co.level-wn.bottom_level) as MaxDepth,
	0 as InitDepth,
	0 as SurchargeDepth,
	0 as PondedArea,
	--st_x(wn.situation_geometry) as X_coordinate,
	--st_y(wn.situation_geometry) as Y_coordinate,
	ws.identifier as description,
	ss.obj_id as tag,
	wn.situation_geometry as geom
FROM qgep_od.special_structure ss
LEFT JOIN qgep_od.wastewater_structure ws ON ws.obj_id::text = ss.obj_id::text
LEFT JOIN qgep_od.wastewater_networkelement we ON we.fk_wastewater_structure::text = ws.obj_id::text
LEFT JOIN qgep_od.wastewater_node wn on wn.obj_id = we.obj_id
LEFT JOIN qgep_od.cover co on ws.fk_main_cover = co.obj_id
WHERE function  = 4799 -- separating_structure
AND wn.obj_id is not null