all: list.tsv
	echo 'ok'
list.tsv: mergeLists.py LA.tsv LB.tsv LC.tsv LD.tsv LE.tsv LF.tsv
	python3 mergeLists.py LA.tsv LB.tsv LC.tsv LD.tsv LE.tsv LF.tsv list.tsv
LA.tsv: A.geojson metros.shp
	python3 genList.py A.geojson metros.shp LA.tsv
LB.tsv: B.geojson metros.shp
	python3 genList.py B.geojson metros.shp LB.tsv
LC.tsv: C.geojson metros.shp
	python3 genList.py C.geojson metros.shp LC.tsv
LD.tsv: D.geojson metros.shp
	python3 genList.py D.geojson metros.shp LD.tsv
LE.tsv: E.geojson metros.shp
	python3 genList.py E.geojson metros.shp LE.tsv
LF.tsv: F.geojson metros.shp
	python3 genList.py F.geojson metros.shp LF.tsv

A.geojson: getAreas.py "*_75N180W_*.avg_rade9.tif"
	python3 getAreas.py "*_75N180W_*.avg_rade9.tif" A.geojson
B.geojson: getAreas.py "*_75N060W_*.avg_rade9.tif"
	python3 getAreas.py "*_75N060W_*.avg_rade9.tif" B.geojson
C.geojson: getAreas.py "*_75N060E_*.avg_rade9.tif"
	python3 getAreas.py "*_75N060E_*.avg_rade9.tif" C.geojson
D.geojson: getAreas.py "*_00N180W_*.avg_rade9.tif"
	python3 getAreas.py "*_00N180W_*.avg_rade9.tif" D.geojson
E.geojson: getAreas.py "*_00N060W_*.avg_rade9.tif"
	python3 getAreas.py "*_00N060W_*.avg_rade9.tif" E.geojson
F.geojson: getAreas.py "*_00N060E_*.avg_rade9.tif"
	python3 getAreas.py "*_00N060E_*.avg_rade9.tif" F.geojson
