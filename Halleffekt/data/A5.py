#!/usr/bin/env python
#####################################
#
# Filename : A5.py
#
# Projectname : 
#
# Author : Oskar Taubert
#
# Creation Date : Fr 17 Jun 2016 09:41:04 CEST
#
# Last Modified : So 19 Jun 2016 19:29:55 CEST
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

alpha = 4 * 10**-4 # eV / K

#grenztemperaturen
T_e = 270.
T_i = 310.

kB = 8.61173303 * 10**-5 # eV / K


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
###
############################

origlen = len(Ts)
Ts = np.fromiter((x for x in Ts if x > T_i), dtype = np.float)

IAs = IAs[origlen-len(Ts):]
UAleit = UAleit[origlen-len(Ts):]
UAH = UAH[origlen-len(Ts):]

R_Hs = - UAH * b / (IAs * B ) * 0.001 # cubic meters / coulomb
b = b0 + db*Ts

n = 1/(-R_Hs * e) * (1-b)/(1+b)
errn = np.zeros(len(Ts))
print(n)

print(n/Ts**1.5)

#TODO oskar: tgrapherrors fucks it up for some reason
g1 = TGraph(len(Ts), 1/Ts, np.log(n/Ts**1.5))
#g1 = TGraphErrors(len(Ts), 1/Ts, np.log(n/Ts**1.5), errT, errn)

g1.SetMarkerStyle(kOpenCircle)
g1.SetMarkerColor(kBlue)
g1.SetLineColor(kBlue)


#f1 = TF1("fit", '[0]*exp([1]*x)', 0., 1.)
f1 = TF1("Linear Law", "[0]+[1] * x", Ts[0], Ts[-1])
f1.SetLineColor(kRed);
f1.SetLineStyle(1);

g1.Fit(f1)

leg = TLegend(.1,.1,.3,.2,"")
leg.SetFillColor(0)
leg.AddEntry(g1, "Messdaten")
leg.AddEntry(f1, "fit")

mg = TMultiGraph()
mg.SetTitle("Arrhenius;1/T / (1/K); ln(n_{i}/T^{3/2})")
mg.Add(g1)

c1 = TCanvas( 'c1', '', 200, 10, 700, 500)
c1.SetGrid()

mg.Draw("AP")
f1.Draw("SAME")
leg.Draw("SAME")

c1.Update()

c1.SaveAs("A5.pdf")

#raw_input()

yachs = f1.GetParameter(0)

E_G0 = -2 * kB * f1.GetParameter(1) # eV
print('E_G0 = ', E_G0)

E_G300 = E_G0 - alpha * 300 # eV
print('E_G300 = ', E_G300)


ni300 = 300**1.5 * np.exp(yachs - E_G0 / ( 2 * kB * 300))
print('ni300 = ', ni300)
