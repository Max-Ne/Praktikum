#!/usr/bin/env python
#####################################
#
# Filename : Fe57.py
#
# Projectname : 
#
# Author : Oskar Taubert
#
# Creation Date : Mo 04 Jul 2016 19:37:08 CEST
#
# Last Modified : Di 05 Jul 2016 16:45:25 CEST
#
#####################################

from ROOT import *
import numpy as np

#setup
filename = "Fe57.txt"

#init
gROOT.Reset()

#reading and plotting and fun
#velocities
vs = []
with open ("data/velocities.csv", 'r') as vf:
    for line in vf:
        if line[0] == '#':
            continue
        line = line.strip()
        line = line.split(' ', 1)
        vs.append(float(line[1]))

vs = np.array(vs[2:], dtype=float)

#counts
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

g = TGraphErrors(len(counts), vs, counts, np.zeros(len(counts)), count_err)

c1 = TCanvas('c1', "", 200, 10, 700, 500 )
c1.SetGrid()
c1.cd()

g.Draw("AP")

c1.Update()

raw_input()
