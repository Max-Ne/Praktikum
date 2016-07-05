#!/usr/bin/env python
#####################################
#
# Filename : calibration.py
#
# Projectname : 
#
# Author : Oskar Taubert
#
# Creation Date : Do 30 Jun 2016 12:48:32 CEST
#
# Last Modified : Di 05 Jul 2016 16:48:43 CEST
#
#####################################

import numpy as np
import csv
from ROOT import *

#setup
filename = "velocity_cal.txt"

wvlen = 632.8 #nm

#init

gROOT.Reset()

#################################################

#channels = []
counts = []

with open("data/" + filename, 'r') as dataf:
    for line in dataf:
        line = line.strip()
        line = line.split(' ', 1)
        line[0] = line[0].strip()
        line[1] = line[1].strip()

        counts.append(float(line[1].replace(',','.')))

channel1 = counts[0]
channel2 = counts[1]

counts = np.array(counts[2:], dtype=float)

#poisson
count_err = np.sqrt(counts, dtype=float)

###TODO why do we need these fits??

channel_min1 = np.argmin(counts[:len(counts)/2])
channel_min2 = np.argmin(counts[channel_min1+1:]) + channel_min1+1

channel_max = np.argmax(counts[channel_min1:channel_min2]) + channel_min1 + 1

BZ = channel2 * 10. # in mu s

#TODO this gives +/- 12 mm/s should be 6
vs = (wvlen / 2) * (counts / BZ) # in mm / s

vs[channel_min1:channel_min2] = -vs[channel_min1:channel_min2]

verr = (wvlen / 2) * (count_err / BZ)

g = TGraphErrors(len(counts), np.array(range(len(counts)), dtype=float), vs, np.zeros(len(counts)), verr)


c1 = TCanvas('c1', "", 200, 10, 700, 500 )
c1.SetGrid()
c1.cd()


g.Draw("AP")

c1.Update()

c1.SaveAs("plots/velocities.pdf")

## just write out the velocities

with open("data/velocities.csv", 'wb') as csvfile:
    csvfile.write('# channel || velocity in mm/s')
    vwriter = csv.writer(csvfile, delimiter = ' ')
    vwriter.writerow([1.0, channel1])
    vwriter.writerow([2.0, channel2])
    vwriter.writerows(zip(np.array(range(len(counts)), dtype=float)+3, vs))

