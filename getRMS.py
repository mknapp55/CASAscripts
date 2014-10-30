#Script to find and then plot the RMS values for a set of images

import numpy as np
import scipy as sp
import scipy.constants as const
import glob
import os
import matplotlib.pyplot as plt
import time

scriptmode=True

ims1 = glob.glob('cleanAllFQdt*.residual')
ims2 = glob.glob('cleanMFQ_flg2*.residual')
stats1 = []
rms1 = []
stats2 = []
rms2 = []
for y in range(0,len(ims1)):
	# Flag 1:
	print y
	tmp = imstat(ims1[y])
	tmp2 = [tmp['max'][0], tmp['min'][0], tmp['mean'][0], tmp['sigma'][0], tmp['rms'][0], tmp['median'][0], tmp['maxpos'][0],tmp['maxpos'][1], tmp['minpos'][0], tmp['minpos'][1]]
	rms1.append(tmp['rms'][0])
	stats1.append(tmp2)
	# Flag 2:
	tmp = imstat(ims2[y])
	tmp2 = [tmp['max'][0], tmp['min'][0], tmp['mean'][0], tmp['sigma'][0], tmp['rms'][0], tmp['median'][0], tmp['maxpos'][0],tmp['maxpos'][1], tmp['minpos'][0], tmp['minpos'][1]]
	rms2.append(tmp['rms'][0])
	stats2.append(tmp2)
	
	
stat1 = np.array(stats1)
rmss1 = np.array(rms1)
stat2 = np.array(stats2)
rmss2 = np.array(rms2)
plt.figure()
plt.plot(np.arange(61.,100.), rmss1*1000, 'b:.')
plt.plot(np.arange(61.,100.), rmss2*1000, 'r:.')
plt.xlabel('NSB')
plt.ylabel('RMS (mJy)')
plt.legend(['Flagging 1', 'Flagging 2'])
