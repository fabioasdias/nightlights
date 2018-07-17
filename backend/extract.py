from glob import glob
from subprocess import call

for f in glob('*.tgz'):
    print(f)
    call('tar -xf {0} --wildcards "*rade9*"'.format(f),shell=True)