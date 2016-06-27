#!/usr/bin/env python
#####################################
#
# Filename : B12.py
#
# Projectname : 
#
# Author : Oskar Taubert
#
# Creation Date : So 19 Jun 2016 20:31:25 CEST
#
# Last Modified : So 26 Jun 2016 22:03:40 CEST
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

#Probe B Abmessungen

B = 0.5 # T

k_B = 8.617330 * 10**-5 # eV / K

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
TBs = Ts[:len(UBleit)]

print(IBs)
IBs = IBs / 1000.
print(IBs)

errU = []
errI = []
errT = 0.1 * np.ones(len(Ts))


################################################

errSigma = np.zeros(len(Ts))
errR_H = np.zeros(len(Ts))

sigmas = l * IAs / (b * d * UAleit) # S / m # as should be
R_Hs = - UAH * b / (IAs * B ) * 0.001# cubic meters / coulomb

sigmaBs = (np.log(2) / np.pi) * (IBs / UBleit)
R_HBs = UBH / (IBs * B)

errTB = np.zeros(len(TBs))
errSigmaB = np.zeros(len(TBs))


###B1
with open('mobility_B.csv', 'wb') as csvfile:
    sigmaR_Hwriter = csv.writer(csvfile, delimiter=' ')
    sigmaR_Hwriter.writerow(['#T in K', '#R_H in m**3 / C'])
    sigmaR_Hwriter.writerows(zip(TBs, sigmaBs*np.abs(R_HBs)))

###B2


g1 = TGraphErrors(len(Ts), Ts, sigmas * np.abs(R_Hs), errT, errR_H)
g2 = TGraphErrors(len(TBs), TBs, sigmaBs * np.abs(R_HBs), errTB, errSigmaB)

g1.SetMarkerStyle(kOpenCircle)
g1.SetMarkerColor(kBlue)
g1.SetLineColor(kBlue)

g2.SetMarkerStyle(kOpenCircle)
g2.SetMarkerColor(kRed)
g2.SetLineColor(kRed)

leg = TLegend(.1,.1,.3,.2,"")
leg.SetFillColor(0)
leg.AddEntry(g1, "Probe A")
leg.AddEntry(g2, "Probe B")

mg = TMultiGraph()
mg.SetTitle("Beweglichkeit: 2DEG und Volumenkristall; T / K; #mu / (1/T)")
mg.Add(g1)
mg.Add(g2)

##########################################
### phonon phun
##########################################


AcousticPhononScattering = TF1("Acoustic", "[0] * 1/x", 90, 430)
OpticPhononScattering = TF1("Optic", "[0] * (exp([1]/x) - 1)", 90, 430)

AcousticPhononScattering.SetParameter(0, 100.)
OpticPhononScattering.SetParameter(0, 10.)
OpticPhononScattering.SetParameter(1, 50.)

mu_tot = TF1("Total", "1/(1/Optic + 1/Acoustic)", 90, 430)
mu_tot.SetLineColor(kGreen)

mu_tot.SetParameters(1000,1000,1000)
#print(mu_tot.GetParameter(0))
#print(mu_tot.GetParameter(1))
#print(mu_tot.GetParameter(2))
print("[0] = phonon[0], [1] = phonon[1], [2] = acoustic[0]")

g2.Fit(mu_tot)

#print(AcousticPhononScattering.GetParameter(0))
#print(OpticPhononScattering.GetParameter(0))

leg.AddEntry(mu_tot, "Fit: Phononstreuung")

c1 = TCanvas( 'c1', '', 200, 10, 700, 500)
c1.SetGrid()
c1.SetLogy(1)

mg.Draw("AP")
leg.Draw("SAME")
mu_tot.Draw("SAME")

c1.Update()
c1.SaveAs("B2.pdf")


