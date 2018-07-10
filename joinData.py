import sys
from fuzzywuzzy import process

if len(sys.argv)!=3:
    print('.py list.tsv data.tsv')
    exit(-1)


#metro   country region  ismetro location.code   gdpusc_2000
data={}
names=[]
header=[]
with open(sys.argv[2],'r') as f:
    for line in f:
        vals=[x.strip() for x in line.strip().split('\t')]        
        if not header:
            header=vals[5:]
            continue
        metro=vals[0]
        data[metro]=vals[5:]
        names.append(metro)




regions={}
pos={}
first=True
with open(sys.argv[1],'r') as f:
    for line in f:
        vals=line.split('\t')
        if first:
            first=False
            pos={k.strip():i for i,k in enumerate(vals)}
        else:
            mrid=vals[pos['MR_ID']]
            if mrid not in regions:
                regions[mrid]=[]
            regions[mrid].append(vals[pos['METRO']].strip())

for mrid in regions:
    vals=[0.0,]*len(header)
    for m in regions[mrid]:
        maybe=process.extractOne(m,names)
        if maybe and maybe[1]>=90:
            pass
            # print('+',m,'->',maybe[0])
        else:
            print('-',m)#,'->',maybe[0],maybe[1])



        