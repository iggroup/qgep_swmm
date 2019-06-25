DROP VIEW IF EXISTS qgep_swmm.vw_infiltration;

--------
-- View for the swmm module class junction
-- 20190329 qgep code sprint SB, TP
--------

CREATE OR REPLACE VIEW qgep_swmm.vw_infiltration AS

SELECT 
	replace(ca.obj_id, ' ', '_')  as Subcatchment,
	3 as MaxRate,
	0.5 as MinRate,
	4 as Decay,
	7 as DryTime,
	0 as MaxInfil
FROM qgep_od.catchment_area as ca
