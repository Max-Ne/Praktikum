#!/usr/bin/env python
#####################################
#
# Filename : A2in.py
#
# Projectname : 
#
# Author : Oskar Taubert
#
# Creation Date : So 12 Jun 2016 17:16:56 CEST
#
# Last Modified : So 19 Jun 2016 18:57:51 CEST
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


############################
### leitwertbereiche finden intrinsisch
############################

errSigma = np.zeros(len(Ts))
errR_H = np.zeros(len(Ts))

sigmas = l * IAs / (b * d * UAleit) # S / m # as should be
R_Hs = - UAH * b / (IAs * B ) * 0.001 # cubic meters / coulomb

#write sigma * |R_Hs| to csv for protocol
with open('sigmaR_H.csv', 'wb') as csvfile:
    sigmaR_Hwriter = csv.writer(csvfile, delimiter=' ')
    sigmaR_Hwriter.writerow(['#T in K', '#R_H in m**3 / C'])
    sigmaR_Hwriter.writerows(zip(Ts, R_Hs*np.abs(R_Hs)))


g1 = TGraphErrors(len(Ts), Ts, sigmas * np.abs(R_Hs), errT, errR_H)
l = TLine(310., 1., 310., 5.)
l.SetLineColor(kGreen)

g1.SetMarkerStyle(kOpenCircle)
g1.SetMarkerColor(kBlue)
g1.SetLineColor(kBlue)

leg = TLegend(.1,.1,.3,.2,"")
leg.SetFillColor(0)
leg.AddEntry(g1, "#sigma R_{H}")
leg.AddEntry(l, "Grenztemperatur")

mg = TMultiGraph()
mg.SetTitle("Grenztemperatur: intrinsisch;T / K;#sigma |R_{H}| / (1/T)")
mg.Add(g1)

c1 = TCanvas( 'c1', '', 200, 10, 700, 500)
c1.SetGrid()
c1.SetLogy(1)
c1.SetLogx(1)

mg.Draw("AP")
leg.Draw("SAME")
l.Draw("SAME")

c1.Update()
c1.SaveAs("A2in.pdf")

#raw_input()

