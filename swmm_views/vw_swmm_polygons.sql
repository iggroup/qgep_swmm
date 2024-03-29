DROP VIEW IF EXISTS qgep_swmm.vw_polygons;

--------
-- View for the swmm module class junction
-- 20190329 qgep code sprint SB, TP
--------

CREATE OR REPLACE VIEW qgep_swmm.vw_polygons AS

SELECT 
	Subcatchment, 
	round(ST_X((dp).geom)::numeric,2) as X_Coord,
	round(ST_Y((dp).geom)::numeric,2) as Y_Coord
FROM (
	SELECT 
		Name As Subcatchment, 
		ST_DumpPoints(geom) AS dp, 
		ST_NPoints(geom) as nvert 
	FROM qgep_swmm.vw_subcatchments
	) as foo
WHERE (dp).path[2] != nvert	-- dont select last vertice