# Script to run several clean operations to test out multi-SB imaging and discrete time segments
# Only SB in the ~middle of the band are used since either end is messier/noisier

import numpy as np
import scipy as sp
import scipy.constants as const
import time
import os

# Initial calculations:
r2asec = 206264.806
vall = '/Users/Shared/MS_dir\(LOFAR\)/L85562_all.MS'
# Get list of subband center frequencies
tb.open(vall+'/SPECTRAL_WINDOW')
centerfqs = tb.getcol('REF_FREQUENCY')
tb.close()
# Convert to wavelength
centerlambda = const.c/centerfqs
# Get station diameter
tb.open(vall+'/ANTENNA')
diams = tb.getcol('DISH_DIAMETER')
tb.close()
diamsavg = np.mean(diams)

# Get max baseline
baselinesm = au.getBaselineLengths(vall, sort=True)
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
vis = glob.glob('L85562_SB*.MS')
for v, idx in vis:
	print n
	ts = time.time()
	print 'Starting clean for '+v+'...'
	name = 'clean2SB_flag1_SB'+idx+'_it'+str(its)+'_wp'+str(wp)+'_facets'+str(fac)+'_npix'+str(npix)+'nsb100'
	clean(vis, spw='', field='0', mode='mfs', gridmode='widefield', wprojplanes=wp, facets=fac, imagename=name, niter=its, interactive=False, imsize=[npix, npix], cell=ceil(synthbeamasec[sbstart+n-1]))
	tmp = imstat(name+'.image')
	tmp2 = [tmp['max'][0], tmp['min'][0], tmp['mean'][0], tmp['sigma'][0], tmp['rms'][0], tmp['median'][0], tmp['maxpos'][0],tmp['maxpos'][1], tmp['minpos'][0], tmp['minpos'][1]]
	rms.append(tmp['rms'][0])
	pixsize.append(ceil(synthbeamasec[sbstart+n-1]))
	print 'Clean finished for SB %s, RMS = %f, pixel size = %d, image width = %d degrees.' % (idx, rms[-1], pixsize[-1], npix*pixsize[-1]/3600)
	tf = time.time()
	rt.append(tf-ts)
	print 'Run time: '+str(rt[-1])
print rms
print rt
	

	