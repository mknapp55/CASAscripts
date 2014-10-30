# Script to divide the single massive MS into smaller timechunks

import datetime as dtm
from datetime import timedelta
import time
import glob
import sys
import os
import numpy as np

startT = '24-Jan-2013/21:37:16.0'
endT = '25-Jan-2013/03:37:06.0'

st = dtm.datetime.strptime(startT, '%d-%b-%Y/%H:%M:%S.%f')
et = dtm.datetime.strptime(endT, '%d-%b-%Y/%H:%M:%S.%f')

obsdur = et-st
obsdurS = str(obsdur)

dt = '00:10:00'
delt = dtm.datetime.strptime(dt, '%H:%M:%S')
nsecd = delt.hour*3600+delt.minute*60+delt.second
deltaT = timedelta(seconds=nsecd)

# How many iterations/MS files to create
steps=obsdur.seconds/deltaT.seconds

vis = 'L85562_all_flagged.MS'
pts = vis.split('.')
vroot = pts[0]

rt = []
for i in range(0,steps):
    ts = time.time()
    if i == 0:
        trange = dtm.datetime.strftime(st, '%H:%M:%S')+'+'+dt
    else:
        trange = dtm.datetime.strftime(st+deltaT*i, '%H:%M:%S')+'+'+dt
    print 'Starting trange '+trange+'...'
    sbname = 'tsplit-'+vroot+'-'+trange
    split(vis, outputvis=sbname, datacolumn='all', timerange='trange', spw='')
    tf = time.time()
    rt.append(tf-ts)
    print 'Runtime: '+str(rt[-1])

