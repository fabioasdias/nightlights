all: outData.tsv 
	echo 'ok'
clean: 
	-rm *.geojson
	-rm *.tsv
outData.tsv: list.tsv data/data.tsv joinData.py
	python3 joinData.py list.tsv data/data.tsv outData.tsv
	sed 's/,/ /g' outData.tsv | sed 's/\t/,/g' > outData.csv
list.tsv: mergeLists.py LA.tsv LB.tsv LC.tsv LD.tsv LE.tsv LF.tsv
	python3 mergeLists.py LA.tsv LB.tsv LC.tsv LD.tsv LE.tsv LF.tsv list.tsv
	sed 's/,/ /g' list.tsv | sed 's/\t/,/g' > list.csv
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

A.geojson: getAreas.py 
	python3 getAreas.py "*_75N180W_*rade9*" A.geojson
B.geojson: getAreas.py 
	python3 getAreas.py "*_75N060W_*rade9*" B.geojson
C.geojson: getAreas.py 
	python3 getAreas.py "*_75N060E_*rade9*" C.geojson
D.geojson: getAreas.py 
	python3 getAreas.py "*_00N180W_*rade9*" D.geojson
E.geojson: getAreas.py 
	python3 getAreas.py "*_00N060W_*rade9*" E.geojson
F.geojson: getAreas.py 
	python3 getAreas.py "*_00N060E_*rade9*" F.geojson
