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
# Last Modified : Di 05 Jul 2016 19:19:48 CEST
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

#data point graph
g = TGraphErrors(len(counts), vs, counts, np.zeros(len(counts)), count_err)

g.SetTitle("{}^{57}Fe;velocity / mm/s; # Events")
    
#fitting fun
n_peaks = 6
fs = []
fit_mins = [-7., -4.5, -2., 0., 2., 4.]
fit_maxs = [-4.5, -2., -0.5, 2., 4.5, 7.]
for i in range(n_peaks):
    fs.append(TF1("Peak" + str(i+1), "[0]*exp(-0.5*((x-[1])/[2])^2) + [3]", fit_mins[i], fit_maxs[i]))

fs[0].SetParameters(-300., (fit_mins[0] + fit_maxs[0])/2, 0.1, 1100.)
fs[1].SetParameters(-300., (fit_mins[1] + fit_maxs[1])/2, 0.1, 1100.)
fs[2].SetParameters(-200., (fit_mins[2] + fit_maxs[2])/2, 0.1, 1100.)
fs[3].SetParameters(-200., (fit_mins[3] + fit_maxs[3])/2, 0.1, 1100.)
fs[4].SetParameters(-300., (fit_mins[4] + fit_maxs[4])/2, 0.1, 1100.)
fs[5].SetParameters(-300., (fit_mins[5] + fit_maxs[5])/2, 0.1, 1100.)

for i in range(n_peaks):
    g.Fit("Peak" + str(i+1), 'R')

#legend
l = TLegend(.6,.8,.9,.9)
l.SetFillColor(0)
l.AddEntry(g, "data points", "p")
l.AddEntry(fs[0], "fits")

#draw all the shit
c1 = TCanvas('c1', "", 200, 10, 700, 500 )
c1.SetGrid()
c1.cd()

g.Draw("AP")
for f in fs:
    f.Draw("SAME")
l.Draw("SAME")

c1.Update()

c1.SaveAs("./plots/Fe57.pdf")
