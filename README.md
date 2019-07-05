
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

Launch `.\scripts\install_swmm_views.bat`. 

This script:
* Creates the schema `qgep_swmm`
* Creates views of qgep tables for correspondances with SWMM tables
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

### Solve import errors

`Undefined Node`
The node doesn't exist in junctions, outfalls, dividers, storages

`Undefined Link`
The link doesn't exist im conduits, pumps, orifices, weirs, outlets

You have to solve the errors in the order they appear in the report. Some errors are interrelated (i.e. a node in a conduit is not defined => the conduit is not imported => Undefined link error)

## Change parameters

### Title/Notes:
* Set by the user as a QGEP_SWMM option 
* update title if necessary.

### Options: 
* Copied from the template input file if exists.
* set / update simulation parameters.

### Climatology:
* Copied from the template input file if exists.
* set / update climatology parameters

### Hydrology:
#### Rain Gages: 
QGEP_SWMM creates one raingage for each subcatchment. 

By default:
* Time serie: Each raingage is related to a default rain time serie called `default_qgep_raingage_timeserie`. The time serie must be created and the value Series Name update accordingly.
* Other parameters have default SWMM values

#### Aquifers:
QGEP_SWMM creates an aquifer for each qgep aquifiers.

By default:
* An aquifer is created for each qgep aquifiers
* The bottom elevation is set to the minimal_groundwater_level
* The water table elevation is set to the average_groundwater_level
* Other parameters have default SWMM values

#### Subcatchment:
QGEP_SWMM creates a subcatchment for each QGEP catchment area
By default:
* a subcatchment is created for each QGEP catchment area
* it is linked to a rain gage. 
* The width is computed from the mean of the minimal / maximal distance between the outlet and the catchment area contour. If the outlet is unknow the centroid is used rather thant the outlet.
* The coverages (attribute land uses) are computed from the intersection between the catchment area and the planning zone
* Other parameters have default SWMM values

The subcatchment can be linked to an aquifer via the groundwater attribute.



#### Snow Packs
* Copied from the template input file if exists.

#### Unit hydrographs
* Copied from the template input file if exists.

#### LID Controls
* Copied from the template input file if exists.

### Hydraulics

#### Junctions
* QGEP_SWMM creates a junction for each QGEP manhole and some kind of special structures.

* See `vw_swmm_junctions.sql` for details.

#### Outfalls
* QGEP_SWMM creates an outfall for each QGEP discharge_point.

* See `vw_swmm_outfalls.sql` for details.

#### Dividers
* Are not created from QGEP objects.

* Copied from the template input file if exists.

#### Storage Units
* QGEP_SWMM creates a storage for some kind of QGEP infiltration installations and some kind of QGEP special structures.

* See `vw_swmm_storages.sql` for details.

#### Conduits
* QGEP_SWMM creates a conduit for each QGEP reach.

* See `vw_swmm_conduits.sql` for details.

#### Pumps
* QGEP_SWMM creates a pump for each QGEP pump.

* See `vw_swmm_pumps.sql` for details.

#### Orifices
* Are not created from QGEP objects.

* Copied from the template input file if exists.

#### Weirs
* Are not created from QGEP objects.

* Copied from the template input file if exists.

#### Outlets
* Are not created from QGEP objects.

* Copied from the template input file if exists.

#### Transects
* Are not created from QGEP objects.

* Copied from the template input file if exists.

#### Controls
* Are not created from QGEP objects.

* Copied from the template input file if exists.

### Quality

#### Land uses
* QGEP_SWMM creates a land use for each QGEP planning zone kind.

#### Pollutants
* Are not created from QGEP objects.

* Copied from the template input file if exists.

### Curves
* Are not created from QGEP objects.

* Copied from the template input file if exists.

### Time series
* Are not created from QGEP objects.

* Copied from the template input file if exists.

### Time patterns
* Are not created from QGEP objects.

* Copied from the template input file if exists.

### Labels
* Are not created from QGEP objects.

* Copied from the template input file if exists.

## Run a simulation
Use the *lightning* button

### Solve running errors
[Errors explanation](https://swmm5.org/2016/09/05/swmm-5-1-and-infoswmm-error-and-warning-messages/)

`ERROR 211: invalid number -XXX at line XXX of [JUNC] section:`

A negative number is provided for the depth => change the value in QGEP or in the .inp file.

## Run current state simulation

## Run aimed state simulation
* Inflows increase
* Impervious areas increase

## Run variants (network is modified)
* New links and new nodes are created
