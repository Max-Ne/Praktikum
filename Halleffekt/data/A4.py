#!/usr/bin/env python
#####################################
#
# Filename : A4.py
#
# Projectname : 
#
# Author : Oskar Taubert
#
# Creation Date : So 12 Jun 2016 17:47:49 CEST
#
# Last Modified : Mi 22 Jun 2016 18:17:35 CEST
#
#####################################
from ROOT import *

import csv

import numpy as np

gROOT.Reset();

###the other random shit
#Probe A Abmessungen
l = 19. # mm
b = 10. # mm
d = 1. # mm

B = 0.5 # T

b0 = 1.24553
db = 0.00107

e = 1.602176 * 10**-19 #C

###entries:
Ts = np.array([], dtype=np.float) # in degree Celsius
IAs = np.array([], dtype=np.float) # in mA
UAleit = np.array([], dtype=np.float) # V
UAHplus = np.array([], dtype=np.float) # mV
UAHminus = np.array([], dtype=np.float) # mV
IBs = np.array([], dtype=np.float) # muA
UBleit = np.array([], dtype=np.float) # mV
UBHplus = np.array([], dtype=np.float) # mV
UBHminus = np.array([], dtype=np.float) # mV

UAH = np.array([], dtype=np.float)
UBH = np.array([], dtype=np.float)


filename = "data.csv"

data = open(filename);

for line in data:
    if line.startswith("#") or line.startswith(" ") or line.startswith("\n"):
        continue;
    line = line.split()

    Ts = np.append(Ts, float(line[0]))
    IAs = np.append(IAs, float(line[1]))
    UAleit = np.append(UAleit, float(line[2]))
    UAHplus = np.append(UAHplus, float(line[3]))
    UAHminus = np.append(UAHminus, float(line[4]))

    if len(line) > 5:
        IBs = np.append(IBs, float(line[5]))
        UBleit = np.append(UBleit, float(line[6]))
        UBHplus = np.append(UBHplus, float(line[7]))
        UBHminus = np.append(UBHminus, float(line[8]))

data.close()
#preprocessing
UAH = (UAHplus - UAHminus) / 2;
UBH = (UBHplus - UBHminus) / 2;
Ts = Ts + 273.15

errU = []
errI = []
errT = 0.1 * np.ones(len(Ts))

#convert to SI units
l *= 1000 # m
b *= 1000 # m
d *= 1000 # m

IAs *= 1000 # A
UAH *= 1000 # V
IBs *= 1000000 # A
UBleit *= 1000 # V
UBH *= 1000 # V


#only look at intrinsic bit
origlen = len(Ts)
Tthresh = 310
Ts = np.fromiter((x for x in Ts if x > Tthresh), dtype = np.float)
#print(Ts)
IAs = IAs[origlen-len(Ts):]
UAleit = UAleit[origlen-len(Ts):]
UAH = UAH[origlen-len(Ts):]

#print(len(Ts), len(IAs), len(UAleit), len(UAH))
#TODO oskar R_Hs should be < 0, but it is not
R_Hs = - UAH * b / (IAs * B ) * 0.001 # cubic meters / coulomb
b = b0 + db*Ts

print(R_Hs)
print((1-b)/(1+b))

n = 1/(-R_Hs * e) * (1-b)/(1+b)
errn = np.zeros(len(Ts))

#write n_i to csv for protocol
with open('n_i.csv', 'wb') as csvfile:
    n_iwriter = csv.writer(csvfile, delimiter=' ')
    n_iwriter.writerow(['#T in K', '#n_i'])
    n_iwriter.writerows(zip(Ts, n))



g1 = TGraphErrors(len(Ts), Ts, n, errT, errn)

g1.SetMarkerStyle(kOpenCircle)
g1.SetMarkerColor(kBlue)
g1.SetLineColor(kBlue)

#leg = TLegend(.1,.8,.3,.9,"")
#leg.SetFillColor(0)
#leg.AddEntry(g1, "n_{i}")

mg = TMultiGraph()
mg.SetTitle("Ladungstr#ddot{a}gerkonzentration;T / K;n_{i} / m^{-3}")
mg.Add(g1)

c1 = TCanvas( 'c1', '', 200, 10, 700, 500)
c1.SetGrid()


mg.Draw("AP")
#leg.Draw("SAME")

c1.Update()

c1.SaveAs("A4.pdf")

#raw_input()
