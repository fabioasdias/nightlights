import sys
from fuzzywuzzy import process

if len(sys.argv)!=4:
    print('.py list.tsv data.tsv out.tsv')
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


with open(sys.argv[3],'w') as f:
    f.write('MR_ID\tN_METROS\tMISSING\t'+'\t'.join(header)+'\n')
    for mrid in regions:
        vals=[0.0,]*len(header)
        missing=0
        for m in regions[mrid]:
            maybe=process.extractOne(m,names)
            if maybe and maybe[1]>=90:
                vals=[v+float(data[maybe[0]][i]) for i,v in enumerate(vals)]
                # print('+',m,'->',maybe[0])
            else:
                missing+=1
                # print('-',m)#,'->',maybe[0],maybe[1])
        f.write('\t'.join(['{0}'.format(x) for x in [mrid,len(regions[mrid]),missing,*vals]])+'\n')


        