# Script to run several clean operations to test out multi-SB imaging and discrete time segments
# Only SB in the ~middle of the band are used since either end is messier/noisier

import numpy as np
import scipy as sp
import scipy.constants as const
import time
import os

# Initial calculations:
r2asec = 206264.806

# Get list of subband center frequencies
tb.open('L85562_all.MS/SPECTRAL_WINDOW')
centerfqs = tb.getcol('REF_FREQUENCY')
tb.close()
# Convert to wavelength
centerlambda = const.c/centerfqs
# Get station diameter
tb.open('L85562_all.MS/ANTENNA')
diams = tb.getcol('DISH_DIAMETER')
tb.close()
diamsavg = np.mean(diams)

# Get max baseline
baselinesm = au.getBaselineLengths('L85562_all.MS', sort=True)
baselinesm1 = np.array(tuple(x[1] for x in baselinesm))
# Convert to wavelength
maxbaselines = baselinesm1.max()*np.ones((np.shape(centerlambda)[0], 1))/centerlambda

# Number of w-planes
dA = 0.5
nwplanes = (0.31/dA)*baselinesm1.max()*centerlambda/diamsavg

# Expected beamsize

FOV = centerlambda/diamsavg
FOVasec = FOV*r2asec
FOVamin = FOVasec/60
FOVdeg = FOVamin/60
synthbeam = centerlambda/baselinesm1.max()
synthbeamasec = synthbeam*r2asec

# How many pixels across primary beam?
dbpixsz = synthbeamasec/3

AprimeB = (FOVasec/2)**2*np.pi
Apix = (dbpixsz/2)**2*np.pi

# Start by increasing number of SB, using full time
# One at a time for now (results more quickly), iterate for fuller coverage later

rms = []
pixsize = []
npix = 2048
its = 1000
wp = 256
fac=8
rt = []

nsb = np.array([2,4,8,16,32])
sbstart = 40
vis = 'L85562_all_flagged2.MS'
for n in nsb:
	print n
	ts = time.time()
	spwr = str(sbstart)+'~'+str(sbstart+n-1)
	print 'Starting clean for SB'+spwr+'...'
	name = 'cleanMFQ_flg2_SB'+spwr+'_it'+str(its)+'_wp'+str(wp)+'_facets'+str(fac)+'_npix'+str(npix)
	clean(vis, spw=spwr, field='0', mode='mfs', gridmode='widefield', wprojplanes=wp, facets=fac, imagename=name, niter=its, interactive=False, imsize=[npix, npix], cell=ceil(synthbeamasec[sbstart+n-1]))
	tmp = imstat(name+'.image')
	tmp2 = [tmp['max'][0], tmp['min'][0], tmp['mean'][0], tmp['sigma'][0], tmp['rms'][0], tmp['median'][0], tmp['maxpos'][0],tmp['maxpos'][1], tmp['minpos'][0], tmp['minpos'][1]]
	rms.append(tmp['rms'][0])
	pixsize.append(ceil(synthbeamasec[sbstart+n-1]))
	print 'Clean finished for SB %s, RMS = %f, pixel size = %d, image width = %d degrees.' % (spwr, rms[-1], pixsize[-1], npix*pixsize[-1]/3600)
	tf = time.time()
	rt.append(tf-ts)
	print 'Run time: '+str(rt[-1])
	
# Now with time (let's try with all SB and see what happens):
rmst = []
pixsize = []
npix = 2048
its = 1000
wp = 512
fac=8
rt_t = []

# Use middle part of the array
dt = ['0:03:45','0:07:30','0:15:00','0:30:00','1:00:00','2:00:00']
tstart = '22:30:00'
for t in dt:
	ts = time.time()
	trange=tstart+'+'+t
	print 'Starting clean for dt = '+t+'...'
	name = 'cleanAllFQdt_flg2_'+str(t)+'_it'+str(its)+'_wp'+str(wp)+'_facets'+str(fac)+'_npix'+str(npix)
	clean(vis, spw='40~72', timerange=trange, field='0', mode='mfs', gridmode='widefield', wprojplanes=wp, facets=fac, imagename=name, niter=its, interactive=False, imsize=[npix, npix], cell=ceil(synthbeamasec[-1]))
	tmp = imstat(name+'.image')
	tmp2 = [tmp['max'][0], tmp['min'][0], tmp['mean'][0], tmp['sigma'][0], tmp['rms'][0], tmp['median'][0], tmp['maxpos'][0],tmp['maxpos'][1], tmp['minpos'][0], tmp['minpos'][1]]
	rmst.append(tmp['rms'][0])
	pixsize.append(ceil(synthbeamasec[119]))
	print 'Clean finished for time range %s, RMS = %f, pixel size = %d, image width = %d degrees.' % (trange, rmst[-1], pixsize[-1], npix*pixsize[-1]/3600)
	tf = time.time()
	rt_t.append(tf-ts)
	print 'Run time: '+str(rt_t[-1])
