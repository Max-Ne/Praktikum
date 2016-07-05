#!/usr/bin/env python
#####################################
#
# Filename : FeSO4.py
#
# Projectname : 
#
# Author : Oskar Taubert
#
# Creation Date : Di 05 Jul 2016 12:53:59 CEST
#
# Last Modified : Di 05 Jul 2016 19:19:44 CEST
#
#####################################

from ROOT import *
import numpy as np

#setup
filename = "FeSO4.txt"

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

g.SetTitle("FeSO4;velocity / mm/s; # Events")

#fitting fun
n_peaks = 2
fs = []
fit_mins = [-2., 1.]
fit_maxs = [1., 4.]

for i in range(n_peaks):
    fs.append(TF1("Peak" + str(i+1), "[0]*exp(-0.5*((x-[1])/[2])^2) + [3]", fit_mins[i], fit_maxs[i]))

fs[0].SetParameters(-300., (fit_mins[0] + fit_maxs[0])/2, 0.1, 1600.)
fs[1].SetParameters(-300., (fit_mins[1] + fit_maxs[1])/2, 0.1, 1600.)

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

c1.SaveAs("./plots/FeSO4.pdf")
