# Script to run rflag on all data
# This script (rflagraw.py) uses ntime=30min

import numpy as np
import scipy as sp
import scipy.constants as const
import glob
import os
import matplotlib.pyplot as plt
import time
from pprint import pprint

# Get statistics on the raw data, run flagger, get new statistics:
ists={}
iflagged = {}
ipct=[]
imaxs=[]
imeans=[]
istdevs=[]

fsts={}
fflagged = {}
fpct=[]
fmaxs=[]
fmeans=[]
fstdevs=[]
vis='L85562_all_flagged.MS'
for x in range(0,120):
	# Amplitude stats for each .MS:
	tmp=visstat(vis, spw=str(x))
	ists[x] = tmp.values()
	imaxs.append(tmp['DATA']['max'])
	imeans.append(tmp['DATA']['mean'])
	istdevs.append(tmp['DATA']['stddev'])	
	# Also get the current state of flags via flagdata summary:
	tmp2 = flagdata(vis, spw=str(x), mode='summary')
	iflagged[x] = tmp2
	ipct.append(tmp2['flagged']/tmp2['total'])
	
	# Now run rflag:
	print 'Flagging SB'+str(x)+'...'
	flagdata(vis, mode='rflag', ntime='30min', spw=str(x), timedevscale=10, winsize=5, action='apply', display='', flagbackup=True, savepars=True)
	
	tmp3=visstat(vis, spw=str(x))
	tmp4 = flagdata(vis, spw=str(x), mode='summary')
	
	fsts[x]=tmp2.values()
	fflagged[x]=tmp2
	
	fmaxs.append(tmp3['DATA']['max'])
	fmeans.append(tmp3['DATA']['mean'])
	fstdevs.append(tmp3['DATA']['stddev'])
	fpct.append(tmp4['flagged']/tmp2['total'])
	
change=np.array(fpct)-np.array(ipct)

# Save results:
fl = open('flaggingAug82014_a.txt', 'w')
fl.write('Pre/post flagging stats for raw data flagging:\n\n')
fl.write('ists =')
pprint(ists, fl)
fl.write('\niflagged=')
pprint(iflagged, fl)
fl.write('\nimaxs=')
pprint(imaxs, fl)
fl.write('\nimeans=')
pprint(imeans, fl)
fl.write('\nistdevs=')
pprint(istdevs, fl)
fl.write('\nipct=')
pprint(ipct, fl)
fl.write('\nfsts=')
pprint(fsts, fl)
fl.write('\nfflagged=')
pprint(fflagged, fl)
fl.write('\nfmaxs=')
pprint(fmaxs, fl)
fl.write('\nfmeans=')
pprint(fmeans, fl)
fl.write('\nfstdevs=')
pprint(fstdevs, fl)
fl.write('\nfpct=')
pprint(fpct, fl)
fl.write('\nchange=')
pprint(change, fl)
fl.close()