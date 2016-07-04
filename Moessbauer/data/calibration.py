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
# Last Modified : Sa 02 Jul 2016 13:19:38 CEST
#
#####################################

from ROOT import *
import numpy as np
import csv

#setup
filename = "velocity_cal.txt"

wvlen = 632.8 #nm

#init

gROOT.Reset()

#################################################

#channels = []
counts = []

with open(filename, 'r') as dataf:
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

#channel_min1 = np.argmin(counts[:len(counts)/2])
#channel_min2 = np.argmin(counts[channel_min1+1:]) + channel_min1+1
#
#channel_max = np.argmax(counts[channel_min1:channel_min2]) + channel_min1 + 1

#g = TGraphErrors(len(counts), np.array(range(len(counts)), dtype=float), counts, np.zeros(len(counts)), count_err)
#
#
#c1 = TCanvas('c1', "", 200, 10, 700, 500 )
#c1.SetGrid()
#c1.cd()
#
#
#g.Draw("AP")
#
#c1.Update()
#
#raw_input()
BZ = channel2 # in mu s

vs = wvlen / 2 * counts / BZ # in mm / s


## just write out the velocities

with open('velocities.csv', 'wb') as csvfile:
    vwriter = csvwriter(csvfile, delimiter = ' ')
    vwriter.writerow(['# channel #', '#velocity in mm/s'])
    vwriter.writerow([1, channel1])
    vwriter.writerow([2, channel2])
    vwriter.writerow(zip(np.array(range(len(counts)), dtype=float)+2, counts))

