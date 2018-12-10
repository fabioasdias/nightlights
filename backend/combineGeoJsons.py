import json
from glob import glob
import sys

print(len(sys.argv))
if len(sys.argv)!=3:
    print('.py "fileMask" out.geojson')
    exit(-1)

ret=[]
for gj in glob(sys.argv[1]):
    print(gj)
    with open(gj,'r') as fin:
        current=json.load(fin)
    if not ret:
        ret=current
    else:
        ret['features'].extend(current['features'])

with open(sys.argv[2],'w') as fout:
    json.dump(ret,fout)