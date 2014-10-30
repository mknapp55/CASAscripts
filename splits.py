# Split MS by time or frequency chunks

import numpy as np
import scipy as sp
import scipy.constants as const
import time
import datetime
import os

tb.open('L85562_all.MS/OBSERVATION')
startstop = tb.getcol('TIME_RANGE')
tb.close

startT = startstop[0,0]
stopT = startstop[1,0]  # These are unix dates
# Make them strings...
startS = 

def splitByFreq(nsb, vis):
	for n in range(0, 120, nsb):
		print n
		outname = 'L85562_SB'+str(n)+'~'+str(n+(nsb-1))+'.MS'
		print outname
		spws = str(n)+'~'+str(n+(nsb-1))
		split(vis, outname, datacolumn='all', field='', spw=spws, uvrange='>100lambda', scan='')

# Split MS in time chunks
def splitByTime(dt, vis):
	# dt should be in minutes
	# How many chunks? get start and stop time from ms
	