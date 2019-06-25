DROP VIEW IF EXISTS qgep_swmm.vw_subareas;


--------
-- View for the swmm module class junction
-- 20190329 qgep code sprint SB, TP
-- A pump in qgep is a node but a link in SWMM
-- -> The pump is attached to the reach which goes out from the pump
-- -> inlet node is the water node where the QGEP pump is located
-- -> outlet node is the water node at the end of the reach going out of the pump
--------

CREATE OR REPLACE VIEW qgep_swmm.vw_subareas AS

SELECT 
	ca.obj_id as Subcatchment,
	0.01 as NImperv,
	0.1 as NPerv,
	0.05 as SImperv,
	0.05 as SPerv,
	25 as PctZero,
	'OUTLET'::varchar as RouteTo,
	NULL::float as PctRouted,
	ca.identifier as description,
	'catchment_area'::varchar as tag
FROM qgep_od.catchment_area as ca
