import numpy as np
import scipy as sp
import scipy.constants as const
import time
import datetime
import os

# MS file to use:
vis = 'L85562_all_flagged.MS'

# Create logfile:
lf = open('logfile_timesteps.txt', 'a')
lf.write('# Log for timesteps processing of HD80606b LOFAR data\n')
lf.write('Run started at '+datetime.datetime.today().strftime('%m/%d/%Y %H:%M:%S')+'\n')
lf.write('# Timestamp, # Timerange, # Runtime, # RMS\n')
lf.close()

# Initial calculations:
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

# Step through increasing size time chunks (no overlap):
rmst = []
pixsize = []
npix = 1024
its = 10000
wp = 512
fac=8
spwrange = '15~105'
cl = str(synthbeamasec[15]*2.5)+'arcsec'
majcyc = 5
th = '0.0Jy'
rt_t = []

# Time chunks:
dt = ['0:05:37.5', '0:11:15', '0:15:00', '0:22:30', '0:30:00', '0:45:00', '1:00:00', '1:30:00','2:00:00', '3:00:00', '6:00:00']
ndt = [64,32,24,16,12,8,6,4,3,2,1]
tstart = '21:37:11.0'
tstartday = '24-Jan-2013'
tst = tstartday+'-'+tstart
tstartdt = datetime.datetime.strptime(tst, '%d-%b-%Y-%H:%M:%S.%f')
for idx, t in enumerate(dt):
    ts_outer = time.time()
    print 'Starting clean for set with dt = '+t+'...'
    for n in range(0,ndt[idx]):
      ts_inner = time.time()
      splitdelt = t.split(':')
      tdelta = datetime.timedelta(hours=int(splitdelt[0]),minutes=int(splitdelt[1]),seconds=float(splitdelt[2]))
      tstartn = tstartdt+tdelta*n
      trange=tstartn.strftime('%Y/%m/%d/%H:%M:%S.%f')+'+'+t
      print 'Cleaning '+trange+'... ('+str(n)+'/'+str(ndt[idx])+')'
      name = 'timesteps_flg1_dt'+splitdelt[0]+'-'+splitdelt[1]+'-'+splitdelt[2]+'_n'+str(n)+'_it'+str(its)+'_wp'+str(wp)+'_facets'+str(fac)+'_npix'+str(npix)
      pclean(vis, spw= spwrange, timerange=trange, field='0', mode='continuum', ftmachine='wproject', wprojplanes=wp, facets=fac, majorcycles=majcyc, imagename=name, niter=its, interactive=False, imsize=[npix, npix], cell=cl, uvrange='')
      tmp = imstat(name+'.image')
      tmp2 = [tmp['max'][0], tmp['min'][0], tmp['mean'][0], tmp['sigma'][0], tmp['rms'][0], tmp['median'][0], tmp['maxpos'][0],tmp['maxpos'][1], tmp['minpos'][0], tmp['minpos'][1]]
      rmst.append(tmp['rms'][0])
      print 'Clean finished for time range %s, RMS = %f.' % (trange, tmp['rms'][0])
      print 'Results of imstat: '
      print tmp2
      tf_inner = time.time()
      rt_t.append(tf_inner-ts_inner)
      print 'Run time: '+str(rt_t[-1])
      lf = open('logfile_timesteps.txt', 'a')
      lf.write(datetime.datetime.today().strftime('%m/%d/%Y %H:%M:%S')+','+trange+','+str(rt_t[-1])+','+str(tmp['rms'][0])+'\n')
      lf.close()
      tmp = []
      tmp2 = []
    tf_outer = time.time()
    print 'Runtime for all '+str(ndt[idx])+' '+t+' chunks: '+str(tf_outer-ts_outer)
