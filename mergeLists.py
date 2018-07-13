import sys


def _read(fname):
    header=[]
    entries={}
    with open(fname) as f:
        for line in f:
            if (not header):
                header=line
                continue
            vals=line.split('\t')
            g=int(vals[0])
            if (g not in entries):
                entries[g]=[]
            entries[g].append(vals[1:])
    return(header,entries)

if len(sys.argv)<=4:
    print('.py L1.tsv L2.tsv (...) out.tsv')
    exit(-1)
fout=sys.argv[-1]
# NL=len(sys.argv)-2
h=[]
E=[]
for f in sys.argv[1:-1]:
    print(f)
    cH,cE=_read(f)
    h.append(cH)
    E.append(cE)

with open(fout,'w') as fout:
    fout.write(h[0])
    lastGroup=0
    for i in range(len(E)):
        for group in E[i]:
            lastGroup+=1                
            for entry in E[i][group]:
                fout.write('{0}\t'.format(lastGroup)+'\t'.join(entry))
                
        