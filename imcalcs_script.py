# Script for CASA to determine number of w-planes, pixel size, and image size for each LOFAR subband.

import numpy as np
import scipy as sp
import scipy.constants as const
import glob
import os
import matplotlib.pyplot as plt
import time

scriptmode=True

vis = 'L85562_all_flagged.MS'

r2asec = 206264.806

# Get list of subband center frequencies
tb.open(vis+'/SPECTRAL_WINDOW')
centerfqs = tb.getcol('REF_FREQUENCY')
tb.close()
# Convert to wavelength
centerlambda = const.c/centerfqs
# Get station diameter
tb.open(vis+'/ANTENNA')
diams = tb.getcol('DISH_DIAMETER')
tb.close()
diamsavg = np.mean(diams)
# Get uvw coords
"""tb.open(vis)
uvw = tb.getcol('UVW')
tb.close()
#uvw_col = uvw.transpose()"""

# Get max baseline
baselinesm = au.getBaselineLengths(vis, sort=True)
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

"""
npix = AprimeB/Apix
npixsq = sqrt(npix)

## Iterate through all SB:

# Get vis file names
vis = glob.glob('L85562*.dppp.MS')

rms = []
pixsize = []
npix = 3000
its = 1000
wp = 256
fac=8
rt = []

for x in range(63,100):
	ts = time.time()
	if x<10:
		num='00'+str(x)
	elif x>=10 and x<100:
		num='0'+str(x)
	else:
		num=str(x)
	print 'Starting clean for SB'+num+'...'
	name='DIwproj_SB'+num
	# Dirty images:
	clean(vis[x], gridmode='widefield', wprojplanes=512, facets=1, imagename=name, niter=0, interactive=False, cell=floor(dbpixsz[x]), imsize=[3000, 3000])    
	# Cleaned images:
	name2='cleanedSB'+num+'-it'+str(its)+'-'+str(fac)+'facets-'+str(wp)+'wp-'+str(npix)+'pix'
	clean(vis[x], gridmode='widefield', field ='0', spw='', wprojplanes=wp, facets=fac, imagename=name2, niter=its, interactive=False, cell=ceil(dbpixsz[x]*3), imsize=[npix, npix])
	tmp = imstat(name2+'.image')
	tmp2 = [tmp['max'][0], tmp['min'][0], tmp['mean'][0], tmp['sigma'][0], tmp['rms'][0], tmp['median'][0], tmp['maxpos'][0],tmp['maxpos'][1], tmp['minpos'][0], tmp['minpos'][1]]
	rms.append(tmp['rms'][0])
	
	pixsize.append(ceil(dbpixsz[-1]*3))
	print 'Clean finished for SB %d, RMS = %d, Pixel size = %d, image width = %d degrees.' % (x, rms[-1], pixsize[-1], npix*pixsize[-1]/3600)
	tf = time.time()
	rt.append(tf-ts)
	print 'Run time for SB'+num+': '+str(rt[-1])

	
	
#Get values from images
ims = glob.glob('cleane*.residual')
stats = []
rms = []
for y in range(0,41):
	tmp = imstat(ims[y])
	tmp2 = [tmp['max'][0], tmp['min'][0], tmp['mean'][0], tmp['sigma'][0], tmp['rms'][0], tmp['median'][0], tmp['maxpos'][0],tmp['maxpos'][1], tmp['minpos'][0], tmp['minpos'][1]]
	rms.append(tmp['rms'][0])
	stats.append(tmp2)
	
	
stat = np.array(stats)
rmss = np.array(rms)
figure()
plot(rms)
show()



# Get pix size from calc above??
# Does the beam match what I calculated?  How is the beam size calculated in CLEAN??

 Clean on a single subband (SB100):

# Run CLEAN on each subband (dirty image)
clean(vis='L85562_SB100_uv.dppp.MS', gridmode='widefield', wprojplanes=512, facets=1, imagename='wproj_SB100_di2',
 niter=0, interactive=False, cell=['8.0arcsec'], imsize=[3000, 3000])

# Attempt some actual cleaning
clean(vis='L85562_SB100_uv.dppp.MS', gridmode='widefield', wprojplanes=256, facets=1, imagename='wproj_SB100_cl1000',
 niter=1000, interactive=False, cell=['8.0arcsec'], imsize=[3000, 3000])

# Try cleaning test data set using 100, 200, 400, and 800 iterations:

its = [100, 200, 400, 800]
for y in its:
	print y
	nm = 'cleantest_SB060_it'+str(y)
	clean(vis='L85562_SB060_uv.dppp.MS', gridmode='widefield', wprojplanes=256, facets=1, imagename=nm, niter=y, interactive=False, cell=['4.0arcsec'], imsize=[3000, 3000])


# Try different numbers of w-planes:

wplns = [64, 128, 256, 512, 1024]
for w in wplns:
	nm = 'cleantest_SB060_it100_w'+str(w)
	clean(vis='L85562_SB060_uv.dppp.MS', gridmode='widefield', wprojplanes=w, facets=1, imagename=nm, niter=100, interactive=False, cell=['4.0arcsec'], imsize=[3000, 3000])"""



"""
