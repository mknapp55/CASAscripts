import numpy as np
import scipy as sp
import scipy.constants as const
import time
import datetime
import os

# MS file to use:
vis = 'L85562_all_flagged.MS'

# Create logfile:
fname = 'logfile_Ptimesteps_test3.txt'
lf = open(fname, 'a')
lf.write('# Log for timesteps processing (param testing 3) of HD80606b LOFAR data\n')
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

# Briggs 0.5 vs 0.0
test1 = {'npix': 2048, 'its': 5000, 'wp': 512, 'fac': 1, 'spw': '15~105', 'wt': 'briggs', 'robust': 0.0, 'majcyc': 5, 'pixsize': str(synthbeamasec[60])+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'IV', 'gain': 0.1, 'alg':'clark', 'msk':'', 'pbcor': False}
test2 = {'npix': 2048, 'its': 5000, 'wp': 512, 'fac': 1, 'spw': '15~105', 'wt': 'briggs', 'robust': 0.25, 'majcyc': 5, 'pixsize': str(synthbeamasec[60])+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'IV', 'gain': 0.1, 'alg':'clark', 'msk':'', 'pbcor': False}
test3 = {'npix': 2048, 'its': 5000, 'wp': 512, 'fac': 1, 'spw': '15~105', 'wt': 'briggs', 'robust': 0.5, 'majcyc': 5, 'pixsize': str(synthbeamasec[60])+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'IV', 'gain': 0.1, 'alg':'clark', 'msk':'', 'pbcor': False}
test4 = {'npix': 2048, 'its': 5000, 'wp': 512, 'fac': 1, 'spw': '15~105', 'wt': 'briggs', 'robust': 0.75, 'majcyc': 5, 'pixsize': str(synthbeamasec[60])+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'IV', 'gain': 0.1, 'alg':'clark', 'msk':'', 'pbcor': False}

# Pixel size:
test5 = {'npix': 2048, 'its': 5000, 'wp': 512, 'fac': 1, 'spw': '15~105', 'wt': 'briggs', 'robust': 0.5, 'majcyc': 5, 'pixsize': str(round(synthbeamasec[60])*1)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'IV', 'gain': 0.1, 'alg':'clark', 'msk':'', 'pbcor': False}
test6 = {'npix': 2048, 'its': 5000, 'wp': 512, 'fac': 1, 'spw': '15~105', 'wt': 'briggs', 'robust': 0.5, 'majcyc': 5, 'pixsize': str(round(synthbeamasec[60])/2)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'IV', 'gain': 0.1, 'alg':'clark', 'msk':'', 'pbcor': False}
test7 = {'npix': 2048, 'its': 5000, 'wp': 512, 'fac': 1, 'spw': '15~105', 'wt': 'briggs', 'robust': 0.5, 'majcyc': 5, 'pixsize': str(round(synthbeamasec[60])/3)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'IV', 'gain': 0.1, 'alg':'clark', 'msk':'', 'pbcor': False}
test8 = {'npix': 2048, 'its': 5000, 'wp': 512, 'fac': 1, 'spw': '15~105', 'wt': 'briggs', 'robust': 0.5, 'majcyc': 5, 'pixsize': str(round(synthbeamasec[60])/4)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'IV', 'gain': 0.1, 'alg':'clark', 'msk':'', 'pbcor': False}

# Pixel size (2x pixels):
test9 = {'npix': 4096, 'its': 5000, 'wp': 512, 'fac': 1, 'spw': '15~105', 'wt': 'briggs', 'robust': 0.5, 'majcyc': 5, 'pixsize': str(round(synthbeamasec[60])*1)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'IV', 'gain': 0.1, 'alg':'clark', 'msk':'', 'pbcor': False}
test10 = {'npix': 4096, 'its': 5000, 'wp': 512, 'fac': 1, 'spw': '15~105', 'wt': 'briggs', 'robust': 0.5, 'majcyc': 5, 'pixsize': str(round(synthbeamasec[60])/2)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'IV', 'gain': 0.1, 'alg':'clark', 'msk':'', 'pbcor': False}
test11 = {'npix': 4096, 'its': 5000, 'wp': 512, 'fac': 1, 'spw': '15~105', 'wt': 'briggs', 'robust': 0.5, 'majcyc': 5, 'pixsize': str(round(synthbeamasec[60])/3)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'IV', 'gain': 0.1, 'alg':'clark', 'msk':'', 'pbcor': False}
test12 = {'npix': 4096, 'its': 5000, 'wp': 512, 'fac': 1, 'spw': '15~105', 'wt': 'briggs', 'robust': 0.5, 'majcyc': 5, 'pixsize': str(round(synthbeamasec[60])/4)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'IV', 'gain': 0.1, 'alg':'clark', 'msk':'', 'pbcor': False}

# Try the masks:
test13 = {'npix': 2048, 'its': 5000, 'wp': 512, 'fac': 1, 'spw': '15~105', 'wt': 'briggs', 'robust': 0.5, 'majcyc': 5, 'pixsize': str(synthbeamasec[60])+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'IV', 'gain': 0.1, 'alg':'clark', 'msk':'VLSSrgn_2Jy.rgn', 'pbcor': False}
test14 = {'npix': 2048, 'its': 5000, 'wp': 512, 'fac': 1, 'spw': '15~105', 'wt': 'briggs', 'robust': 0.5, 'majcyc': 5, 'pixsize': str(synthbeamasec[60])+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'IV', 'gain': 0.1, 'alg':'clark', 'msk':'VLSSrgn_1Jy.rgn', 'pbcor': False}
test15 = {'npix': 2048, 'its': 5000, 'wp': 512, 'fac': 1, 'spw': '15~105', 'wt': 'briggs', 'robust': 0.5, 'majcyc': 5, 'pixsize': str(synthbeamasec[60])+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'IV', 'gain': 0.1, 'alg':'clark', 'msk':'VLSSrgn_all.rgn', 'pbcor': False}
test16 = {'npix': 2048, 'its': 5000, 'wp': 512, 'fac': 1, 'spw': '15~105', 'wt': 'briggs', 'robust': 0.5, 'majcyc': 5, 'pixsize': str(synthbeamasec[60])+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'IV', 'gain': 0.1, 'alg':'clark', 'msk':'mask500mJy2px2.box', 'pbcor': False}

# Full stokes:
test17 = {'npix': 2048, 'its': 5000, 'wp': 512, 'fac': 1, 'spw': '15~105', 'wt': 'briggs', 'robust': 0.5, 'majcyc': 5, 'pixsize': str(synthbeamasec[60])+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'IQUV', 'gain': 0.1, 'alg':'clark', 'msk':'', 'pbcor': False}

# Multiscale algorithm:
test18 = {'npix': 2048, 'its': 5000, 'wp': 512, 'fac': 1, 'spw': '15~105', 'wt': 'briggs', 'robust': 0.5, 'majcyc': 5, 'pixsize': str(synthbeamasec[60])+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'IV', 'gain': 0.1, 'alg':'multiscale', 'msk':'', 'pbcor': False}

# Primary beam correction:
test19 = {'npix': 2048, 'its': 5000, 'wp': 512, 'fac': 1, 'spw': '15~105', 'wt': 'briggs', 'robust': 0.5, 'majcyc': 5, 'pixsize': str(synthbeamasec[60])+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'IV', 'gain': 0.1, 'alg':'clark', 'msk':'', 'pbcor': True}


testlist = [test1, test2, test3, test4, test5, test6, test7, test8, ttest9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19]
'''

npix = 1024
its = 10000
wp = 512
fac=8
spwrange = '15~105'
cl = str(synthbeamasec[15]*2.5)+'arcsec'
majcyc = 5
th = '0.0Jy'
'''
rmst = []
rt_t = []
rtout = []

# Time chunks:
dt = ['0:05:37.5']#, '0:11:15', '0:15:00', '0:22:30', '0:30:00', '0:45:00', '1:00:00', '1:30:00','2:00:00', '3:00:00', '6:00:00']
ndt = [64]#,32,24,16,12,8,6,4,3,2,1]
tstart = '21:37:11.0'
tstartday = '24-Jan-2013'
tst = tstartday+'-'+tstart
tstartdt = datetime.datetime.strptime(tst, '%d-%b-%Y-%H:%M:%S.%f')
tbegin = time.time()
for idx, t in enumerate(dt):
    ts_outer = time.time()
    print 'Starting clean for set with dt = '+t+'...'
    for n in range(0, ndt[idx], 32):
      ts_inner = time.time()
      splitdelt = t.split(':')
      tdelta = datetime.timedelta(hours=int(splitdelt[0]),minutes=int(splitdelt[1]),seconds=float(splitdelt[2]))
      tstartn = tstartdt+tdelta*n
      trange=tstartn.strftime('%Y/%m/%d/%H:%M:%S.%f')+'+'+t
      print 'Cleaning '+trange+'... ('+str(n)+'/'+str(ndt[idx])+')'
      for idxt, tlist in enumerate(testlist):
        #if idxt < 10 or n == 0:
		#print 'Skipping (%d, %d)' % (idxt, n)
		#continue
		ts_inin = time.time()
		print 'Cleaning with test params '+str(idxt + 1)+'...'
        print tlist 
        name = 'Ptimesteps_flg1_dt'+splitdelt[0]+'-'+splitdelt[1]+'-'+splitdelt[2]+'_tpz'+idxt+'_n'+str(n)+'_it'+str(tlist['its'])+'_wp'+str(tlist['wp'])+'_facets'+str(tlist['fac'])
        try:
			pclean(vis, spw=tlist['spw'], timerange=trange, field='0', mode='continuum', ftmachine='wproject', alg=tlist['alg'], wprojplanes=tlist['wp'], facets=tlist['fac'], majorcycles=tlist['majcyc'], imagename=name, niter=tlist['its'], interactive=False, imsize=[tlist['npix'], tlist['npix']], cell=tlist['pixsize'], uvrange='', weighting=tlist['wt'], robust=tlist['robust'], stokes=tlist['stokes'], threshold=tlist['th'], nterms=tlist['nterms'], gain=tlist['gain'], mask=tlist['msk'])

			tmp = imstat(name+'.image')
			print name+'.image'
			tmp2 = [tmp['max'][0], tmp['min'][0], tmp['mean'][0], tmp['sigma'][0], tmp['rms'][0], tmp['median'][0], tmp['maxpos'][0],tmp['maxpos'][1], tmp['minpos'][0], tmp['minpos'][1]]
			rmst.append(tmp['rms'][0])
			print 'Clean finished for time range %s, RMS = %f.' % (trange, tmp['rms'][0])
			print 'Results of imstat: '
			print tmp2
			tf_inin = time.time()
			rt_t.append(tf_inin-ts_inin)
			print 'Run time: '+str(rt_t[-1])
			lf = open(fname, 'a')
			lf.write(name+'\n')
			lf.write(datetime.datetime.today().strftime('%m/%d/%Y %H:%M:%S')+','+trange+','+str(rt_t[-1])+','+str(tmp['rms'][0])+'\n')
			lf.close()
			tmp = []
			tmp2 = []
		except:
			print 'There was a problem running this block of code (idx='+str(idx)+', n='+str(n)+', idxt='+str(idxt)+')'
			lf=open(fname, 'a')
			lf.write('There was a problem with this iteration (testparams '+tstring+', idx='+str(idx)+', n='+str(n)+', idxt='+str(idxt)+')\n')
			lf.close()
			continue
		tf_inner = time.time()
		rt_inner = tf_inner-ts_inner
		print 'Runtime for n='+str(n)+' : '+str(rt_inner)+' sec'
		lf.open(fname, 'a')
		lf.write('Runtime for n='+str(n)+' : '+str(rt_inner)+' sec\n')
		lf.close()
    tf_outer = time.time()
    rtout.append(tf_outer-ts_outer)
    print 'Outer loop run time '+ str(idx)+': '+str((tf_outer-ts_outer)/60)+' minutes'
    lf = open(fname, 'a')
    lf.write('Total runtime: '+str((tf_outer-ts_outer)/60)+' minutes \n')
    lf.close()
tend = time.time()
print 'Runtime for all '+str(ndt[idx])+' '+t+' chunks: '+str(tf_outer-ts_outer)
lf = open(fname, 'a')
lf.write('Run finished successfully at '+datetime.datetime.today().strftime('%m/%d/%Y %H:%M:%S')+'\n')
lf.write('Total runtime: '+str((tend-tbegin)/60)+' minutes \n')
lf.close()
