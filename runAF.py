#Script to run autoflagger on list of SB

import numpy as np
import scipy as sp
import scipy.constants as const
import glob
import os
import matplotlib.pyplot as plt
import time
from pprint import pprint

# First, let's get some statistics
print 'Getting visibility statistics...'
"""
sts={}
initflagged = {}
startpct=[]
maxs=[]
means=[]
stdevs=[]
vis=glob.glob('L85562_SB*.dppp.MS')
for x in range(0,len(vis)):
	# Amplitude stats for each .MS:
	tmp=visstat(vis[x])
	sts[x] = tmp.values()
	maxs.append(tmp['DATA']['max'])
	means.append(tmp['DATA']['mean'])
	stdevs.append(tmp['DATA']['stddev'])
	
	# Also get the current state of flags via flagdata summary:
	tmp2 = flagdata(vis[x], 'summary')
	initflagged[x] = tmp2
	startpct.append(tmp2['flagged']/tmp2['total'])

# Plot results:
plt.plot(np.array(maxs), 'r.')
plt.plot(np.array(means), 'g.')
plt.plot(np.array(stdevs), 'm.')
plt.plot(np.array(startpct), 'b.')

# Save results

"""

# Run autoflagger
postflagsts={}
postflg={}
fpct=[]
fmaxs=[]
fmeans=[]
fstdevs=[]
for y in range(0,len(vis)):
	print 'Flagging SB'+str(y)+'...'
	flagdata(vis[y], mode='rflag', ntime='16min', action='apply', display='', flagbackup=True, savepars=True)
	
	tmp3=visstat(vis[y])
	tmp4 = flagdata(vis[y], mode='summary')
	
	postflagsts[y]=tmp2.values()
	postflg[y]=tmp2
	
	fmaxs.append(tmp3['DATA']['max'])
	fmeans.append(tmp3['DATA']['mean'])
	fstdevs.append(tmp3['DATA']['stddev'])
	fpct.append(tmp4['flagged']/tmp2['total'])
	
change=np.array(startpct)-np.array(fpct)

# Now get statistics on the raw data:
osts={}
oflagged = {}
opct=[]
omaxs=[]
omeans=[]
ostdevs=[]
vis='L85562_all.MS'
for x in range(0,120):
	# Amplitude stats for each .MS:
	tmp=visstat(vis, spw=str(x))
	osts[x] = tmp.values()
	omaxs.append(tmp['DATA']['max'])
	omeans.append(tmp['DATA']['mean'])
	ostdevs.append(tmp['DATA']['stddev'])
	
	# Also get the current state of flags via flagdata summary:
	tmp2 = flagdata(vis, spw=str(x), mode='summary')
	oflagged[x] = tmp2
	opct.append(tmp2['flagged']/tmp2['total'])
	
# Save results:
fl = open('flaggingAug620142.txt', 'w')
fl.write('Post flagging MS stats:\n')
fl.write('postflagsts =')
pprint(postflagsts, fl)
fl.write('\nPost flagging flag stats:\n')
fl.write('postflg=')
pprint(postflg, fl)
fl.write('\nPost flagging MS maxes:\n')
fl.write('fmaxs=')
pprint(fmaxs, fl)
fl.write('\nPost flagging MS means:\n')
fl.write('fmeans=')
pprint(fmeans, fl)
fl.write('\nPost flagging MS standard devs:\n')
fl.write('fstdevs=')
pprint(fstdevs, fl)
fl.write('\nPost flagging flag percentage:\n')
fl.write('fpct=')
pprint(fpct, fl)
fl.write('\n\nOriginal data\n\nMS stats (by SB):\nosts=')
pprint(osts, fl)
fl.write('\noflagged=')
pprint(oflagged, fl)
fl.write('\nomaxs=')
pprint(omaxs, fl)
fl.write('\nomeans=')
pprint(omeans, fl)
fl.write('\nostdevs=')
pprint(ostdevs, fl)
fl.write('\nopct=')
pprint(opct, fl)
fl.close()
	
