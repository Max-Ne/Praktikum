#!/usr/bin/env python
#####################################
#
# Filename : VC.py
#
# Projectname : 
#
# Author : Oskar Taubert
#
# Creation Date : Di 05 Jul 2016 12:51:33 CEST
#
# Last Modified : Di 05 Jul 2016 19:01:50 CEST
#
#####################################

from ROOT import *
import numpy as np

#setup
filename = "VC_2nd_try.txt"

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
g.SetTitle("Vacromium;velocity / mm/s; # Events")

#fitting fun
fit_min = -5.
fit_max = 5.
f = TF1("Peak", "[0]*exp(-0.5*((x-[1])/[2])^2) + [3]", fit_min, fit_max)
f.SetParameters(-300., 0., 0.1, 1300)

g.Fit("Peak", 'R')
#legend
l = TLegend(.6,.8,.9,.9)
l.SetFillColor(0)
l.AddEntry(g, "data points", "p")
l.AddEntry(f, "fit")

#draw all the shit
c1 = TCanvas('c1', "", 200, 10, 700, 500 )
c1.SetGrid()
c1.cd()

g.Draw("AP")
f.Draw("SAME")
l.Draw("SAME")

c1.Update()

c1.SaveAs("./plots/VC.pdf")
