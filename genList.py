import json
from shapely.geometry import shape, mapping
from rtree import index
import sys
import fiona
from util import indexedPols
import matplotlib.pylab as plt

minArea=1

if len(sys.argv)!=4:
    print('.py spots.geojson metros.shp list.tsv')
    exit(-1)

with open(sys.argv[1],'r') as f:
    spotsGJ = json.load(f)

spots=[]
for f in spotsGJ["features"]:
    spots.append(shape(f['geometry']))

# spots=[x for x in spots if x.area>=minArea]

pols=indexedPols()

with fiona.open(sys.argv[2]) as shp:
    for feat in shp:
        geom=shape(feat['geometry'])
        pols.insert(geom,props=dict(feat['properties']))

res={}
res["type"]="FeatureCollection"
res["features"]=[]        

with open(sys.argv[3],'w') as f:
    f.write('MR_ID\tCOUNTRY\tMETRO\tID_FUA\n')
    for i,s in enumerate(spots):
        I=pols.search(s)
        if (len(I)<=1): #only more than one region
            continue
        res["features"].append({
            "type": "Feature",
            "geometry": mapping(s),
            "properties": {}
            })

        for ii in I:
            props=pols.getProps(ii)
            f.write('{0}'.format(i)+'\t'+'\t'.join(['{0}'.format(props[x]) for x in ['Country','metro_broo','id_fua']])+'\n')


with open('filt_'+sys.argv[1],'w') as out:
    json.dump(res,out)
