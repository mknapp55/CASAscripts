import numpy as np
import scipy as sp
import scipy.constants as const
import time
import datetime
import os

# MS file to use:
vis = 'L85562_all_flagged.MS'

# Create logfile:
fname = 'logfile_Ptimesteps.txt'
lf = open(fname, 'a')
lf.write('# Log for timesteps processing (param testing) of HD80606b LOFAR data\n')
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
# Bandwidth:
test1 = {'npix': 1024, 'its': 5000, 'wp': 512, 'fac': 1, 'spw': '15~38', 'wt': 'natural', 'robust': 0.0, 'majcyc': 5, 'pixsize': str(synthbeamasec[15]*2)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'I', 'gain': 0.1}
test1b = {'npix': 1024, 'its': 5000, 'wp': 512, 'fac': 1, 'spw': '15~38', 'wt': 'briggs', 'robust': 0.5, 'majcyc': 5, 'pixsize': str(synthbeamasec[15]*2)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'I', 'gain': 0.1}
test2 = {'npix': 1024, 'its': 5000, 'wp': 512, 'fac': 1, 'spw': '15~60', 'wt': 'natural', 'robust': 0.0, 'majcyc': 5, 'pixsize': str(synthbeamasec[15]*2)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'I', 'gain': 0.1}
test2b = {'npix': 1024, 'its': 5000, 'wp': 512, 'fac': 1, 'spw': '15~60', 'wt': 'briggs', 'robust': 0.5, 'majcyc': 5, 'pixsize': str(synthbeamasec[15]*2)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'I', 'gain': 0.1}
test3 = {'npix': 1024, 'its': 5000, 'wp': 512, 'fac': 1, 'spw': '15~105', 'wt': 'natural', 'robust': 0.0, 'majcyc': 5, 'pixsize': str(synthbeamasec[15]*2)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'I', 'gain': 0.1}
test3b = {'npix': 1024, 'its': 5000, 'wp': 512, 'fac': 1, 'spw': '15~105', 'wt': 'briggs', 'robust': 0.5, 'majcyc': 5, 'pixsize': str(synthbeamasec[15]*2)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'I', 'gain': 0.1}

# Change w-planes
test4 = {'npix': 1024, 'its': 5000, 'wp': 512, 'fac': 1, 'spw': '15~105', 'wt': 'natural', 'robust': 0.0, 'majcyc': 5, 'pixsize': str(synthbeamasec[15]*2)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'I', 'gain': 0.1}
test4b = {'npix': 1024, 'its': 5000, 'wp': 512, 'fac': 1, 'spw': '15~105', 'wt': 'briggs', 'robust': 0.5, 'majcyc': 5, 'pixsize': str(synthbeamasec[15]*2)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'I', 'gain': 0.1}
test5 = {'npix': 1024, 'its': 5000, 'wp': 1024, 'fac': 1, 'spw': '15~105', 'wt': 'natural', 'robust': 0.0, 'majcyc': 5, 'pixsize': str(synthbeamasec[15]*2)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'I', 'gain': 0.1}
test5b = {'npix': 1024, 'its': 5000, 'wp': 1024, 'fac': 1, 'spw': '15~105', 'wt': 'briggs', 'robust': 0.5, 'majcyc': 5, 'pixsize': str(synthbeamasec[15]*2)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'I', 'gain': 0.1}
test6 = {'npix': 1024, 'its': 5000, 'wp': 2048, 'fac': 1, 'spw': '15~105', 'wt': 'natural', 'robust': 0.0, 'majcyc': 5, 'pixsize': str(synthbeamasec[15]*2)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'I', 'gain': 0.1}
test6b = {'npix': 1024, 'its': 5000, 'wp': 2048, 'fac': 1, 'spw': '15~105', 'wt': 'briggs', 'robust': 0.5, 'majcyc': 5, 'pixsize': str(synthbeamasec[15]*2)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'I', 'gain': 0.1}

# Facets:
test7 = {'npix': 1024, 'its': 5000, 'wp': 512, 'fac': 1, 'spw': '15~105', 'wt': 'natural', 'robust': 0.0, 'majcyc': 5, 'pixsize': str(synthbeamasec[15]*2)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'I', 'gain': 0.1}
test7b = {'npix': 1024, 'its': 5000, 'wp': 512, 'fac': 1, 'spw': '15~105', 'wt': 'briggs', 'robust': 0.5, 'majcyc': 5, 'pixsize': str(synthbeamasec[15]*2)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'I', 'gain': 0.1}
test8 = {'npix': 1024, 'its': 5000, 'wp': 512, 'fac': 3, 'spw': '15~105', 'wt': 'natural', 'robust': 0.0, 'majcyc': 5, 'pixsize': str(synthbeamasec[15]*2)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'I', 'gain': 0.1}
test8b = {'npix': 1024, 'its': 5000, 'wp': 512, 'fac': 3, 'spw': '15~105', 'wt': 'briggs', 'robust': 0.5, 'majcyc': 5, 'pixsize': str(synthbeamasec[15]*2)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'I', 'gain': 0.1}
test9 = {'npix': 1024, 'its': 5000, 'wp': 512, 'fac': 5, 'spw': '15~105', 'wt': 'natural', 'robust': 0.0, 'majcyc': 5, 'pixsize': str(synthbeamasec[15]*2)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'I', 'gain': 0.1}
test9b = {'npix': 1024, 'its': 5000, 'wp': 512, 'fac': 5, 'spw': '15~105', 'wt': 'briggs', 'robust': 0.5, 'majcyc': 5, 'pixsize': str(synthbeamasec[15]*2)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'I', 'gain': 0.1}

# Number of pixels
test10 = {'npix': 1024, 'its': 5000, 'wp': 512, 'fac': 1, 'spw': '15~105', 'wt': 'natural', 'robust': 0.0, 'majcyc': 5, 'pixsize': str(synthbeamasec[15]*2)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'I', 'gain': 0.1}
test10b = {'npix': 1024, 'its': 5000, 'wp': 512, 'fac': 1, 'spw': '15~105', 'wt': 'briggs', 'robust': 0.5, 'majcyc': 5, 'pixsize': str(synthbeamasec[15]*2)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'I', 'gain': 0.1}
test11 = {'npix': 2048, 'its': 5000, 'wp': 512, 'fac': 1, 'spw': '15~105', 'wt': 'natural', 'robust': 0.0, 'majcyc': 5, 'pixsize': str(synthbeamasec[60]*2)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'I', 'gain': 0.1}
test11b = {'npix': 2048, 'its': 5000, 'wp': 512, 'fac': 1, 'spw': '15~105', 'wt': 'briggs', 'robust': 0.5, 'majcyc': 5, 'pixsize': str(synthbeamasec[60]*2)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'I', 'gain': 0.1}

# Iterations:
test12 = {'npix': 1024, 'its': 1000, 'wp': 512, 'fac': 1, 'spw': '15~105', 'wt': 'natural', 'robust': 0.0, 'majcyc': 5, 'pixsize': str(synthbeamasec[15]*2)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'I', 'gain': 0.1}
test12b = {'npix': 1024, 'its': 1000, 'wp': 512, 'fac': 1, 'spw': '15~105', 'wt': 'briggs', 'robust': 0.5, 'majcyc': 5, 'pixsize': str(synthbeamasec[15]*2)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'I', 'gain': 0.1}
test13 = {'npix': 1024, 'its': 5000, 'wp': 512, 'fac': 1, 'spw': '15~105', 'wt': 'natural', 'robust': 0.0, 'majcyc': 5, 'pixsize': str(synthbeamasec[15]*2)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'I', 'gain': 0.1}
test13b = {'npix': 1024, 'its': 5000, 'wp': 512, 'fac': 1, 'spw': '15~105', 'wt': 'briggs', 'robust': 0.5, 'majcyc': 5, 'pixsize': str(synthbeamasec[15]*2)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'I', 'gain': 0.1}
test14 = {'npix': 1024, 'its': 10000, 'wp': 512, 'fac': 1, 'spw': '15~105', 'wt': 'natural', 'robust': 0.0, 'majcyc': 5, 'pixsize': str(synthbeamasec[15]*2)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'I', 'gain': 0.1}
test14b = {'npix': 1024, 'its': 10000, 'wp': 512, 'fac': 1, 'spw': '15~105', 'wt': 'briggs', 'robust': 0.5, 'majcyc': 5, 'pixsize': str(synthbeamasec[15]*2)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'I', 'gain': 0.1}

# Pixel size:
test15 = {'npix': 2048, 'its': 5000, 'wp': 512, 'fac': 1, 'spw': '15~105', 'wt': 'natural', 'robust': 0.0, 'majcyc': 5, 'pixsize': str(synthbeamasec[15]*1)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'I', 'gain': 0.1}
test15b = {'npix': 2048, 'its': 5000, 'wp': 512, 'fac': 1, 'spw': '15~105', 'wt': 'briggs', 'robust': 0.5, 'majcyc': 5, 'pixsize': str(synthbeamasec[15]*1)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'I', 'gain': 0.1}
test16 = {'npix': 2048, 'its': 5000, 'wp': 512, 'fac': 1, 'spw': '15~105', 'wt': 'natural', 'robust': 0.0, 'majcyc': 5, 'pixsize': str(synthbeamasec[15]*1.5)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'I', 'gain': 0.1}
test16b = {'npix': 2048, 'its': 5000, 'wp': 512, 'fac': 1, 'spw': '15~105', 'wt': 'briggs', 'robust': 0.5, 'majcyc': 5, 'pixsize': str(synthbeamasec[15]*1.5)+'arcsec', 'th': '0.0mJy', 'nterms': 1, 'stokes': 'I', 'gain': 0.1}

testlist = [test1, test1b, test2, test2b, test3, test3b, test4, test4b, test5, test5b, test6, test6b, test7, test7b, test8, test8b, test9, test9b, test10, test10b, test11, test11b, test12, test12b, test13, test13b, test14, test14b, test15, test15b, test16, test16b]
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
        print 'Cleaning with test params '+str(idxt + 1)+'...'
        print tlist 
        if idxt % 2 == 0:
          tstring = '_tp'+str(int(idxt/2+1))
        else:
          tstring = '_tp'+str(int (floor(idxt/2)+1))+'b'
        name = 'Ptimesteps_flg1_dt'+splitdelt[0]+'-'+splitdelt[1]+'-'+splitdelt[2]+tstring+'_n'+str(n)+'_it'+str(tlist['its'])+'_wp'+str(tlist['wp'])+'_facets'+str(tlist['fac'])
        try:
		if tlist['wt'] == 'natural':
			print 'Natural weighting'
			pclean(vis, spw=tlist['spw'], timerange=trange, field='0', mode='continuum', ftmachine='wproject', alg='clark', wprojplanes=tlist['wp'], facets=tlist['fac'], majorcycles=tlist['majcyc'], imagename=name, niter=tlist['its'], interactive=False, imsize=[tlist['npix'], tlist['npix']], cell=tlist['pixsize'], uvrange='', weighting=tlist['wt'], stokes=tlist['stokes'], threshold=tlist['th'], nterms=tlist['nterms'], gain=tlist['gain'])
		else:
			print 'Briggs weighting'
			pclean(vis, spw=tlist['spw'], timerange=trange, field='0', mode='continuum', ftmachine='wproject', alg='clark', wprojplanes=tlist['wp'], facets=tlist['fac'], majorcycles=tlist['majcyc'], imagename=name, niter=tlist['its'], interactive=False, imsize=[tlist['npix'], tlist['npix']], cell=tlist['pixsize'], uvrange='', weighting=tlist['wt'], robust=tlist['robust'], stokes=tlist['stokes'], threshold=tlist['th'], nterms=tlist['nterms'], gain=tlist['gain'])

		tmp = imstat(name+'.image')
		print name+'.image'
		tmp2 = [tmp['max'][0], tmp['min'][0], tmp['mean'][0], tmp['sigma'][0], tmp['rms'][0], tmp['median'][0], tmp['maxpos'][0],tmp['maxpos'][1], tmp['minpos'][0], tmp['minpos'][1]]
		rmst.append(tmp['rms'][0])
		print 'Clean finished for time range %s, RMS = %f.' % (trange, tmp['rms'][0])
		print 'Results of imstat: '
		print tmp2
		tf_inner = time.time()
		rt_t.append(tf_inner-ts_inner)
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
