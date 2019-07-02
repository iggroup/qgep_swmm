
# Installation demo data
* Créer BD qgqep_demo_data en local
* Restorer `https://github.com/QGEP/datamodel/releases/download/1.3.0/qgep_v1.3.0_structure_and_demo_data.backup`


# QGEP-SWMM installation

## Installation of a postgreSQL service

In `pg_service.conf` create a service. You can also use an existing service.

```
[pg_qgep_demo_data]
host=localhost
port=5432
dbname=qgep_demo_data
user=postgres
password=postgres
```

## Installation of QGEP-SWMM schema, views and tables

Launch `.\scripts\install_swmm_views.bat`. This script:
* Create the schema `qgep_swmm`
* Create views of qgep tables for correspondances with SWMM tables
* Copies data in the views in tables (record a state of the qgep database)

## Installation of python scripts
The script require `psycopg2` to connect to the database.

[Installation](https://pypi.org/project/psycopg2/)

# QGEP - SWMM workflow

## Generate .INP file
The .inp file is the input file format for SWMM. It contains the wastewater network AND simulation parameters.

The wastewater network is extracted from QGEP tables. The simulation parameters are copied from a provided .inp file.

```
TITLE = 'title simulation'
PGSERVICE = 'pg_qgep_demo_data'
INPFILE = 'S:\\2_INTERNE_SION\\0_COLLABORATEURS\\PRODUIT_Timothee\\02_work\\qgep_swmm\\input\\qgep_swmm.inp'
INPTEMPLATE = 'S:\\2_INTERNE_SION\\0_COLLABORATEURS\\PRODUIT_Timothee\\02_work\\qgep_swmm\\simulation_parameters\\default_qgep_swmm_parameters.inp'
OUTFILE = ''
qs = qgep_swmm(TITLE, PGSERVICE, INPFILE, INPTEMPLATE, OUTFILE)
qs.write_input()
```

## Open .INP with SWMM

### I/O Error 103 
The .inp file is still open in Python. Close Python.

### Import errors

`Undefined Node`
The node doesn't exist in junctions, outfalls, dividers, storages

`Undefined Link`
The link doesn't exist im conduits, pumps, orifices, weirs, outlets