all: list.tsv
	echo 'ok'
list.tsv: mergeLists.py LA.tsv LB.tsv LC.tsv LD.tsv LE.tsv LF.tsv
	python3 mergeLists.py LA.tsv LB.TSV LC.tsv LD.TSV LE.tsv LF.TSV list.tsv
LA.tsv: A.geojson metros.shp
	python3 genList A.geojson metros.shp LA.tsv
LB.tsv: B.geojson metros.shp
	python3 genList B.geojson metros.shp LB.tsv
LC.tsv: C.geojson metros.shp
	python3 genList C.geojson metros.shp LC.tsv
LD.tsv: D.geojson metros.shp
	python3 genList D.geojson metros.shp LD.tsv
LE.tsv: E.geojson metros.shp
	python3 genList E.geojson metros.shp LE.tsv
LF.tsv: F.geojson metros.shp
	python3 genList F.geojson metros.shp LF.tsv
A.geojson: getAreas.py SVDNB_npp_20150101-20151231_75N180W_vcm-orm-ntl_v10_c201701311200.avg_rade9.tif
	python3 getAreas.py SVDNB_npp_20150101-20151231_75N180W_vcm-orm-ntl_v10_c201701311200.avg_rade9.tif A.geojson
B.geojson: getAreas.py SVDNB_npp_20150101-20151231_75N060W_vcm-orm-ntl_v10_c201701311200.avg_rade9.tif
	python3 getAreas.py SVDNB_npp_20150101-20151231_75N060W_vcm-orm-ntl_v10_c201701311200.avg_rade9.tif B.geojson
C.geojson: getAreas.py SVDNB_npp_20150101-20151231_75N060E_vcm-orm-ntl_v10_c201701311200.avg_rade9.tif
	python3 getAreas.py SVDNB_npp_20150101-20151231_75N060E_vcm-orm-ntl_v10_c201701311200.avg_rade9.tif C.geojson
D.geojson: getAreas.py SVDNB_npp_20150101-20151231_00N180W_vcm-orm-ntl_v10_c201701311200.avg_rade9.tif
	python3 getAreas.py SVDNB_npp_20150101-20151231_00N180W_vcm-orm-ntl_v10_c201701311200.avg_rade9.tif D.geojson
E.geojson: getAreas.py SVDNB_npp_20150101-20151231_00N060W_vcm-orm-ntl_v10_c201701311200.avg_rade9.tif
	python3 getAreas.py SVDNB_npp_20150101-20151231_00N060W_vcm-orm-ntl_v10_c201701311200.avg_rade9.tif E.geojson
F.geojson: getAreas.py SVDNB_npp_20150101-20151231_00N060E_vcm-orm-ntl_v10_c201701311200.avg_rade9.tif
	python3 getAreas.py SVDNB_npp_20150101-20151231_00N060E_vcm-orm-ntl_v10_c201701311200.avg_rade9.tif F.geojson


#A 		
#SVDNB_npp_20150101-20151231_75N180W_v10_c201701311200.tgz
#https://data.ngdc.noaa.gov/instruments/remote-sensing/passive/spectrometers-radiometers/imaging/viirs/dnb_composites/v10//2015/SVDNB_npp_20150101-20151231_75N180W_v10_c201701311200.tgz

#B
#SVDNB_npp_20150101-20151231_75N060W_v10_c201701311200.tgz 
#https://data.ngdc.noaa.gov/instruments/remote-sensing/passive/spectrometers-radiometers/imaging/viirs/dnb_composites/v10//2015/SVDNB_npp_20150101-20151231_75N060W_v10_c201701311200.tgz
  
#C
#SVDNB_npp_20150101-20151231_75N060E_v10_c201701311200.tgz 
#https://data.ngdc.noaa.gov/instruments/remote-sensing/passive/spectrometers-radiometers/imaging/viirs/dnb_composites/v10//2015/SVDNB_npp_20150101-20151231_75N060E_v10_c201701311200.tgz
  
#D
#SVDNB_npp_20150101-20151231_00N180W_v10_c201701311200.tgz 
#https://data.ngdc.noaa.gov/instruments/remote-sensing/passive/spectrometers-radiometers/imaging/viirs/dnb_composites/v10//2015/SVDNB_npp_20150101-20151231_00N180W_v10_c201701311200.tgz
  
#E
#SVDNB_npp_20150101-20151231_00N060W_v10_c201701311200.tgz 
#https://data.ngdc.noaa.gov/instruments/remote-sensing/passive/spectrometers-radiometers/imaging/viirs/dnb_composites/v10//2015/SVDNB_npp_20150101-20151231_00N060W_v10_c201701311200.tgz

#F
#SVDNB_npp_20150101-20151231_00N060E_v10_c201701311200.tgz 
#https://data.ngdc.noaa.gov/instruments/remote-sensing/passive/spectrometers-radiometers/imaging/viirs/dnb_composites/v10//2015/SVDNB_npp_20150101-20151231_00N060E_v10_c201701311200.tgz
  
