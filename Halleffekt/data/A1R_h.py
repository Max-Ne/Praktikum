#!/usr/bin/env python
#/*************************************
#  *
#  * Filename : A1R_h.py
#  *
#  * Projectname : 
#  *
#  * Author : Oskar Taubert
#  *
#  * Creation Date : So 12 Jun 2016 15:24:47 CEST
#  *
#  * Last Modified : So 19 Jun 2016 18:03:39 CEST
#  *
#  *************************************/
#
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
errT = 0.1 * np.ones(len(Ts))
############################
### calc Hallkoeff R_H
############################
#TODO: oskar have to put the actual error in
errR_H = np.zeros(len(Ts))
R_Hs = - UAH * b / (IAs * B ) * 0.001 # cubic meters / coulomb

#write R_Hs to csv for protocol
with open('R_H.csv', 'wb') as csvfile:
    R_Hwriter = csv.writer(csvfile, delimiter=' ')
    R_Hwriter.writerow(['#T in K', '#R_H in m**3 / C'])
    R_Hwriter.writerows(zip(Ts, R_Hs))

gHallk = TGraphErrors(len(Ts), Ts, R_Hs, errT, errR_H)

mg = TMultiGraph()

mg.SetTitle("Hallkoeffizient #ddot{u}ber Temperatur;T / K;R_{H} / (m^{3} / C)")

gHallk.SetMarkerStyle(kOpenCircle)
gHallk.SetMarkerColor(kBlue)
gHallk.SetLineColor(kBlue)


leg = TLegend(.1,.8,.3,.9,"Hallkoeffizient")
leg.SetFillColor(0)
leg.AddEntry(gHallk, "Messdaten")


c1 = TCanvas( 'c1', '', 200, 10, 700, 500)
c1.SetGrid()


mg.Add(gHallk)
mg.Draw("AP")
leg.Draw("SAME")

c1.Update()

c1.SaveAs("A1R_h.pdf")

#raw_input()

