import json
from shapely.geometry import shape
from rtree import index
import sys
import fiona
from util import indexedPols

import matplotlib.pylab as plt

minArea=1

if len(sys.argv)!=3:
    print('.py spots.geojson regions.shp')
    exit(-1)

with open(sys.argv[1],'r') as f:
    spotsGJ = json.load(f)

spots=[]
for f in spotsGJ["features"]:
    spots.append(shape(f['geometry']))

spots=[x for x in spots if x.area>=minArea]

pols=indexedPols()

with fiona.open(sys.argv[2]) as shp:
    for feat in shp:
        geom=shape(feat['geometry'])
        pols.insert(geom,props=dict(feat['properties']))


with open('out.tsv','w') as f:
    f.write('MR_ID\tUS_NAME\tUS_AFFGeoID\tCA_CSDNAME\tCA_CSDUID\n')
    for i,s in enumerate(spots):
        I=pols.search(s)
        for ii in I:
            props=pols.getProps(ii)
            f.write('{0}'.format(i)+'\t'+'\t'.join(['{0}'.format(props[x]) for x in ['NAME','AFFGEOID','CSDNAME','CSDUID']])+'\n')