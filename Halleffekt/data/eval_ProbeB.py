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

Ts_B = Ts[:len(IBs)]

errU = []
errI = []
errT = 0.1 * np.ones(len(Ts))
errT_B = 0.1 * np.ones(len(Ts_B))

sigmaB = (np.log(2)/np.pi) * (IBs/UBleit)	# muA/mV = mA/V
R_Hb = (UBH/IBs) / B				# mV/muA /T = V/(mA * T)

bewegl_B = sigmaB * np.absolute(R_Hb)		# 1/T
errBeweg_B = np.zeros(len(IBs))

sigmaA = (l/(b*d)) * (IAs/UAleit)		# 1/mm * mA/V = A/V * 1/m
R_Ha =  (d/B) * (UAH/IAs)			# mm/T * mV/mA = m/T * V/A / 1000

bewegl_A = sigmaA * np.absolute(R_Ha)/100		# 1/T
errBeweg_A = np.zeros(len(Ts))


gBeweg_A = TGraphErrors(len(Ts), Ts, bewegl_A, errT, errBeweg_A)
gBeweg_A.SetMarkerStyle(kOpenCircle)
gBeweg_A.SetMarkerColor(kBlue)
gBeweg_A.SetLineColor(kBlue)
gBeweg_A.SetFillColor(0)

gBeweg_B = TGraphErrors(len(Ts_B), Ts_B, bewegl_B, errT_B, errBeweg_B)
gBeweg_B.SetMarkerStyle(kOpenCircle)
gBeweg_B.SetMarkerColor(kRed)
gBeweg_B.SetLineColor(kRed)
gBeweg_B.SetFillColor(0)

mg = TMultiGraph()
mg.SetTitle("Beweglichkeit der Proben A und B im Vergleich;T in K;#mu in T^{-1}")
mg.Add(gBeweg_A)
mg.Add(gBeweg_B)

leg = TLegend(.7,.8,.9,.9,"Leitf#ddot{a}higkeit")
leg.SetFillColor(0)
leg.AddEntry(gBeweg_A, "Probe A")
leg.AddEntry(gBeweg_B, "Probe B")

c1 = TCanvas( 'c1', '', 200, 10, 700, 500)
c1.SetGrid()
c1.SetLogy();
c1.cd()

mg.Draw("AP")
leg.Draw("SAME")

c1.Update()

raw_input()


""" OSKAR
############################
### calc Leitfaehigkeit sigma
############################

#TODO: oskar have to calc the error of conductivity
errSigma = np.zeros(len(Ts))
#errsigma = 0.0 * np.ones(len(Ts))
sigmas = l * IAs / (b * d * UAleit) # S / m # as should be

gLeit = TGraphErrors(len(Ts), Ts, sigmas, errT, errSigma)
gLeit.SetMarkerStyle(kOpenCircle)
gLeit.SetMarkerColor(kBlue)
gLeit.SetLineColor(kBlue)
gLeit.SetFillColor(0)


##############
### PLOT CONDUCTIVITY OVER TEMPERATURE
##############

mg = TMultiGraph()
mg.SetTitle("Leitf#ddot{a}higkeit /(mA/V) #ddot{u}ber Temperatur/K;T in K;#sigma in mA/V")
mg.Add(gLeit)

leg = TLegend(.1,.8,.3,.9,"Leitf#ddot{a}higkeit")
leg.SetFillColor(0)
leg.AddEntry(gLeit, "Messdaten")

c1 = TCanvas( 'c1', '', 200, 10, 700, 500)
c1.SetGrid()
c1.cd()

mg.Draw("AP")
leg.Draw("SAME")

c1.Update()

raw_input()


############################
### calc Hallkoeff R_H
############################
errR_H = np.zeros(len(Ts))
R_Hs = np.absolute(UAH * d / (IAs * B))

gHall = TGraphErrors(len(Ts), Ts, 1./R_Hs, errT, errR_H)

gHall.SetMarkerStyle(kOpenCircle)
gHall.SetMarkerColor(kBlack)
gHall.SetLineColor(kBlack)
gHall.SetFillColor(0)


##############
### plot log(sigma) and log(1/RH) over temperature (A2.1)
### and add a vertical line (extrinsischer Bereich links davon)
### TO DO: Achsenbeschriftung und Titel
##############

mg2 = TMultiGraph();
mg2.SetTitle("Leitf#ddot{a}higkeit /(mA/V) #ddot{u}ber Temperatur/K;T in K;#sigma in mA/V")
mg2.Add(gLeit)
mg2.Add(gHall)

leg2 = TLegend(.1,.8,.4,.9, "Messdaten")
leg2.SetFillColor(0)
leg2.AddEntry(gLeit, "Leitf#ddot{a}higkeit")
leg2.AddEntry(gHall, "inverser Hallkoeffizient")

c2 = TCanvas( 'c2', '', 200, 10, 700, 500)
c2.SetGrid()
c2.SetLogy();
c2.cd()

mg2.Draw("AP")
leg2.Draw("SAME")
c2.Update()

x2 = 250
vertical2 = TLine (x2,gPad.GetUymin(),x2,100*gPad.GetUymax())
vertical2.SetLineColor(kRed)
vertical2.SetLineStyle(1)
vertical2.SetLineWidth(2)
vertical2.Draw("SAME")
c2.Update()

raw_input();


##############
### plot log(sigma * R_H) over log(T) (A2.2)
### TO DO: labels + title
##############
err_Hall_Leit = np.zeros(len(Ts))
for i in range(len(err_Hall_Leit)):
  err_Hall_Leit[i] = np.sqrt(R_Hs[i]*R_Hs[i] * errSigma[i]*errSigma[i] + sigmas[i]*sigmas[i] * errSigma[i]*errSigma[i])
  
gHall_Leit = TGraphErrors(len(Ts), Ts, R_Hs * sigmas, errT, err_Hall_Leit)

gHall_Leit.SetMarkerStyle(kOpenCircle)
gHall_Leit.SetMarkerColor(kBlue)
gHall_Leit.SetLineColor(kBlue)
gHall_Leit.SetFillColor(0)
gHall_Leit.GetXaxis().SetTickLength(10.)

mg3 = TMultiGraph();
mg3.SetTitle("Leitf#ddot{a}higkeit /(mA/V) #ddot{u}ber Temperatur/K;T in K;#sigma in mA/V")
mg3.Add(gHall_Leit)


c3 = TCanvas( 'c3', '', 200, 10, 700, 500)
c3.SetGrid()
c3.SetLogy();
c3.SetLogx();
c3.cd()

mg3.Draw("AP")
c3.Update()

x3 = 320;
vertical3 = TLine (x3,49,x3,745);
vertical3.SetLineColor(kRed);
vertical3.SetLineStyle(1);
vertical3.SetLineWidth(2);
vertical3.Draw("SAME");
c3.Update()

leg3 = TLegend(.6,.8,.9,.9)
leg3.SetFillColor(0)
leg3.AddEntry(gHall_Leit, "Leitf#ddot{a}higk. * Hallkoeff. ")
leg3.AddEntry(vertical3, "y = 320")
leg3.Draw("SAME")
c3.Update();

raw_input();

"""