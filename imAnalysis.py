# Image analysis script

import glob
import time
import datetime
import pickle
import sys
import os
import numpy as np

r2asec = 206264.806

targetCoord = ['09h22m37.56797s', '+50d36m13.4818s']
pointingCenter = ['09h22m37.570001s', '+50d37m13.50001s']
pointingCenterD = [9*15+22/60+37.570001/3600, 50+37/60+13.50001/3600]

# Other sources in the field from the 4C catalog:
field = {'4C50.29':{'coord':['139.4073','50.0883'], 'Flux': 2.8}, '4C52.21':{'coord':['141.705','52.0779'], 'Flux': 2.3}, '4C48.24':{'coord':['138.6787','48.6623'], 'Flux': 3.8}, '4C53.18':{'coord':['140.7102','53.0159'], 'Flux': 7.4}, '4C48.25': {'coord':['142.5715','48.5119'], 'Flux': 2.8}, '4C52.2': {'coord':['138.045','52.6578'], 'Flux': 3.6}, '4C53.19': {'coord':['142.0939','53.2384'], 'Flux': 3.8}, '4C50.28': {'coord':['135.9575','50.2414'], 'Flux': 2.9}, '4C48.26': {'coord':['142.8906','47.8309'], 'Flux': 2.9}, '4C47.3': {'coord':['139.3607','47.3618'], 'Flux': 2}, '4C51.27': {'coord':['135.2382','51.0822'], 'Flux': 2}, '4C48.23': {'coord':['135.4292','48.7015'], 'Flux': 2.9}}

# Get list of images to process
ims=glob.glob('timesteps*tp?.image')
nims=len(ims)

# Set up variables to hold results
imvals = {}
imfits = {}
allrms = np.array(np.zeros((nims,1)))
targresRMS = np.array(np.zeros((nims,1)))
beamsize = np.array(np.zeros((nims,3)))
pixsize = np.array(np.zeros((nims,1)))
pixperbeam = np.array(np.zeros((nims,2)))
compfits = np.array(np.zeros((nims, len(field))))
targfits = np.array(np.zeros((nims,1)))
# Loop through list
for idx, im in enumerate(ims):
	fnroot = im.rsplit('.', 1)[0]  # Get root file name (w/o .image)
	print fnroot
	imfits[fnroot] = {}
	# Get full image information (beam size, pixel size)
	imheadtmp = imhead(imagename=im, mode='list')
	imMaxRA = pointingCenterD[0]+np.abs(imheadtmp['cdelt1'])*r2asec*imheadtmp['shape'][0]/3600
	imMaxDec = pointingCenterD[1]+np.abs(imheadtmp['cdelt1'])*r2asec*imheadtmp['shape'][1]/3600
	imMinRA = pointingCenterD[0]-np.abs(imheadtmp['cdelt1'])*r2asec*imheadtmp['shape'][0]/3600
	imMinDec = pointingCenterD[1]-np.abs(imheadtmp['cdelt1'])*r2asec*imheadtmp['shape'][0]/3600
	# Beam size (major/minor axes, arcsecs) and position angle (degrees)
	beamsize[idx,:] = np.array([imheadtmp['beammajor']['value'], imheadtmp['beamminor']['value'], imheadtmp['beampa']['value']])
	# Pixel size in arcseconds:
	pixsize[idx] = np.round(np.abs(imheadtmp['cdelt1']*r2asec))
	# Pixels per beam (in each direction)
	pixperbeam[idx,:] = np.array([beamsize[idx,0:2]/pixsize[idx]])
	# Get image statisics (from residual), save RMS
	imstattmp = imstat(fnroot+'.residual')
	allrms[idx] = imstattmp['rms'][0]
	
	# Do target first
	# Region is a box centered on the target, 10 beams (major axis) across
	rgn = 'centerbox[ [ ' + targetCoord[0] + ', ' + targetCoord[1] + '], [' +str(10*np.ceil(beamsize[idx,0])) +'arcsec, '+str(10*np.ceil(beamsize[idx,0]))+'arcsec ] ]'
	# Grab actual target subimage:
	imnm=fnroot+'_subHD80606.image'
	imsubimage(imagename=im, outfile=imnm, region=rgn, dropdeg=True, overwrite=True)
	# Grab residual image in location of target:
	resnm = fnroot+'_subHD80606.residual'
	imsubimage(imagename=fnroot+'.residual', outfile=resnm, region=rgn, dropdeg=True, overwrite=True)
	# Try to fit Gaussian to target:
	imfits[fnroot]['HD80606'] = imfit(imagename=imnm)
	# Get stats on residual at location of target
	tmpres = imstat(fnroot+'_subHD80606.residual')
	targresRMS[idx] = tmpres['rms'][0]
	
	if imfits[fnroot]['HD80606'] is not None and imfits[fnroot]['HD80606']['results']['nelements'] >0:
		targfits[idx] = np.array(imfits[fnroot]['HD80606']['results']['component0']['flux']['value'][0])
		""", imfits[fnroot]['HD80606']['results']['component0']['shape']['direction']['m0']['value'], imfits[fnroot]['HD80606']['results']['component0']['shape']['direction']['m1']['value'], imfits[fnroot]['HD80606']['results']['nelements'])
	#imval()
"""
	# Loop through regions
	
	for idx2, r in enumerate(field):
		print r
		if imMaxRA < float(field[r]['coord'][0]) or imMaxDec < float(field[r]['coord'][1]) or imMinRA > float(field[r]['coord'][0]) or imMinDec > float(field[r]['coord'][1]):
			print 'Object '+r+' ('+field[r]['coord'][0]+', '+field[r]['coord'][1]+') is outside the FOV (Max = ['+str(imMaxRA)+', '+str(imMaxDec)+'], Min = ['+str(imMinRA)+', '+str(imMinDec)+']), skipping...'
			continue
		else: 
			# Region is a box centered on the target, 10 beams (major axis) across
			# !!!!!Need to check if BOX is within image and adjust size if not!!!!!
			rgnf = 'centerbox[ [ '+field[r]['coord'][0]+'deg, '+field[r]['coord'][1]+'deg], ['+str(10*np.ceil(beamsize[idx,0]))+'arcsec, '+str(10*np.ceil(beamsize[idx,0]))+'arcsec ] ]'
			print rgnf
			# Grab actual target subimage:
			rname = fnroot+'_sub'+r+'.image'
			print rname
			imsubimage(imagename = im, outfile=rname, region=rgnf, dropdeg=True, overwrite=True)
			# Grab residual image in location of target:
			rrname = fnroot+'_sub'+r+'.residual'
			imsubimage(imagename = im, outfile=rrname, region=rgn, dropdeg=True, overwrite=True)
			# Try to fit Gaussian to target:
			imfits[fnroot][r] = imfit(imagename=rname)
			if imfits[fnroot][r] is not None and imfits[fnroot][r]['results']['nelements'] >0:
				compfits[idx,idx2] = np.array(imfits[fnroot][r]['results']['component0']['flux']['value'][0]) 

outfilename='imAnalysisRun_'+datetime.datetime.strftime(datetime.datetime.now(), '%m-%d-%Y-%H-%M-%S')+'.pickle'
of = open(outfilename, 'w')
pickle.dump((imvals, imfits, allrms, targresRMS, beamsize, pixsize, pixperbeam, compfits, ims)
, of)
of.close()
print 'All done. Image data saved to '+outfilename
