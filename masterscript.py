print 'Starting CLEANing....'
execfile('beamcalcs.py')
#execfile('timeClean_testing2.py')
print 'Finished CLEANing...'

print 'Starting PCLEANing...'
from simple_cluster import *
sc=simple_cluster()
sc.init_cluster('clusterconfig15.txt', 'mk15')

execfile('timePClean_testing2.py')
print 'Finished PCLEANing...'
