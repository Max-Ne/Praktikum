#!/usr/bin/env python
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

#preprocessing
UAH = (UAHplus - UAHminus) / 2;
UBH = (UBHplus - UBHminus) / 2;
Ts = Ts + 273.15

############################
### calc Leitfaehigkeit sigma
############################

errU = []
errI = []
errT = 0.1 * np.ones(len(Ts))

#TODO: oskar have to calc the error of conductivity
errSigma = np.zeros(len(Ts))
#errsigma = 0.0 * np.ones(len(Ts))
sigmas = l * IAs / (b * d * UAleit) # S / m # as should be

mg = TMultiGraph()

gLeit = TGraphErrors(len(Ts), Ts, sigmas, errT, errSigma)

mg.SetTitle("Leitf#ddot{a}higkeit /(S/m) #ddot{u}ber Temperatur/K")

gLeit.SetMarkerStyle(kOpenCircle)
gLeit.SetMarkerColor(kBlue)
gLeit.SetLineColor(kBlue)

leg = TLegend(.1,.8,.3,.9,"Leitf#ddot{a}higkeit")
leg.SetFillColor(0)
leg.AddEntry(gLeit, "Messdaten")


c1 = TCanvas( 'c1', '', 200, 10, 700, 500)
c1.SetGrid()

mg.Add(gLeit)
mg.Draw("AP")
leg.Draw("SAME")

c1.Update()

raw_input()

############################
### calc Hallkoeff R_H
############################
errR_H = np.zeros(len(Ts))
R_Hs = - (UAH * b / (IAs * B )
