#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# http://www.fieldtriptoolbox.org/development/realtime/buffer_python

import sys
import FieldTrip

hostname = 'localhost'
port = 1972

ftc = FieldTrip.Client()
print 'Trying to connect to buffer on %s:%i ...'%(hostname,port)

ftc.connect(hostname, port)    # might throw IOError

H = ftc.getHeader()
if H is None:
    print 'Failed to retrieve header!'
    sys.exit(1)

print H
print H.labels
print 'Chanels', H.nChannels
print 'fs:', H.fSample
print 'Data Type:', H.dType

"""
        H = Header()
        H.nChannels = nchans
        H.nSamples = nsamp
        H.nEvents = nevt
        H.fSample = fsamp
        H.dataType = dtype
"""

while True:

    if H.nSamples > 0:
        print 'Trying to read last sample...'
        index = H.nSamples - 1
        D = ftc.getData([index, index])
        print 'Data:', D

"""
        getData() # getData([indices]) -- retrieve data samples and return them as a
        Numpy array, samples in rows(!). The 'indices' argument is optional,
        and if given, must be a tuple or list with inclusive, zero-based
        start/end indices.
"""

if H.nEvents > 0:
    print 'Trying to read (all) events...'
    E = ftc.getEvents()
    for e in E:
        print e

ftc.disconnect()
