DROP TABLE IF EXISTS qgep_swmm.nodes_results;


--------
-- View for the swmm module class junction
-- 20190329 qgep code sprint SB, TP
--------
CREATE TABLE qgep_swmm.nodes_results (
	id varchar,
	type varchar,
	average_depth REAL,
	maximum_depth REAL,
	maximum_HGL REAL,
	time_max_day INTEGER,
	time_max_time varchar,
	reported_max_depth REAL
)