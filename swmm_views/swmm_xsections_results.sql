DROP TABLE IF EXISTS qgep_swmm.xsections_results;


--------
-- View for the swmm module class junction
-- 20190329 qgep code sprint SB, TP
--------

CREATE TABLE qgep_swmm.xsections_results (
	id varchar,
	shape varchar,
	full_depth REAL,
	full_area REAL,
	hyd_rad REAL,
	max_width REAL,
	no_of_barrels REAL,
	full_flow REAL
)
