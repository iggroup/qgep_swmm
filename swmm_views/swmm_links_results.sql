DROP TABLE IF EXISTS qgep_swmm.links_results;


--------
-- View for the swmm module class junction
-- 20190329 qgep code sprint SB, TP
--------

CREATE TABLE qgep_swmm.links_results (
	id varchar,
	type varchar,
	maximum_flow REAL,
	time_max_day INTEGER,
	time_max_time varchar,
	maximum_velocity REAL,
	max_over_full_flow REAL,
	max_over_full_depth REAL
)