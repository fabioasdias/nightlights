import json

def convert(v):
    if (isinstance(v,str)):
        conv=True
        for c in v:
            if not (c.isdigit() or c=='.'):
                conv=False
        if conv:
            return(float(v))
    return(v)


data={}
header={}
with open('data.tsv','r') as fin:
    for line in fin:
        vals=line.strip().split('\t')
        if (len(header)==0):
            header={i:h for i,h in enumerate(vals)}
        else:
            data[int(vals[0])]=[convert(v) for v in vals]

with open('bright2p.geojson','r') as fin:
    geojson=json.load(fin)

for feat in geojson['features']:
    props=feat['properties']
    MRID=int(props['MR_ID'])
    for i in range(1,len(header)):
        props[header[i]]=data[MRID][i]
        
with open('data2p.geojson','w') as fout:
    json.dump(geojson,fout)
    

