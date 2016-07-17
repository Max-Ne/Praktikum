#!/usr/bin/env python
#####################################
#
# Filename : QHE.py
#
# Projectname : 
#
# Author : Oskar Taubert
#
# Creation Date : Sa 16 Jul 2016 19:14:31 CEST
#
# Last Modified : Mo 18 Jul 2016 00:35:06 CEST
#
#####################################

import numpy as np
from ROOT import *

#init
gROOT.Reset()

T = 0. #K
I = 0. #muA

U_unit = ''

Us = []
Bs = []

Bread = False
Uread = False

plotname = ""



Bss = []
Uss = []

Is = []
Ts = []
Udirections = []

gs = []
filenames = []

with open("data/index.txt", 'r') as indexf:
    for line in indexf:
        if (Bread and Uread):
            Bs = np.array(Bs, dtype=float)
            Bs = Bs * 6. / Bs.max()
            Us = np.array(Us, dtype=float)

            Bss.append(Bs)
            Uss.append(Us)
            Ts.append(T)
            Is.append(I)
            Udirections.append(plotname[:4])
            
            g = TGraph(len(Bs), Bs, Us)

            filename = "plots/" + plotname + ".pdf"
            filenames.append(filename)

            g.SetTitle(plotname[:4] + " mit T = " + str(T) + " K und I = " + str(int(I)) + " #mu A;B / T;" + plotname[:4] + " / " + U_unit)
            gs.append(g)


#            plt.plot(Bs, Us, 'ro')
#            plt.xlabel("B / T")
#            plt.ylabel(plotname[:4] + " / " + U_unit)
#            plt.tight_layout()
#
#
#
#            plt.savefig("plots/" + plotname + ".pdf")
#            plt.show()

            Bread = False
            Uread = False
            plotname = ""

        if line[0] == 'R':
            pass
        if line[0] == 'T':
            line = line.strip()
            line = line.split()
            T = float(line[2])
            print("T = ", T)
        if line[0] == 'I':
            line = line.strip()
            line = line.split()
            I = float(line[2])
            print("I = ", I)

        if line[0] == 'B':
            print('B')
            line = line.strip()
            line = line.split()
            f = line[2]
            with open("data/" + f, 'r') as dataf:
                Bs = []
                #skip first line
                dline = dataf.readline()
                #check channel
                dline = dataf.readline()
                dline = dline.split()
                if dline[2] != '1':
                    print("shit happened")
                #check units
                dline = dataf.readline()
                dline = dline.strip()
                dline = dline.split(';')
                dline = dline[1]
                dline = dline.split()
                if dline[2] != 'V':
                    print("different shit happened")
                
                dline = dataf.readline()
                while dline:
                    dline = dline.strip()
                    dline = dline.split(';')
                    Bs.append(float(dline[1]))
                    dline = dataf.readline()
                Bread = True
        if line[0] == 'U':
            print('U')
            plotname = line[:4] + '_' + str(int(I)) + 'muA_' + str(int(1000*T)) + 'mK'
            line = line.strip()
            line = line.split()
            f = line[2]
            with open("data/" + f, 'r') as dataf:
                Us = []
                #skip first line
                dline = dataf.readline()
                #check channel
                dline = dataf.readline()
                dline = dline.split()
                if dline[2] != '2':
                    print("more shit happened")
                #check units
                dline = dataf.readline()
                dline = dline.strip()
                dline = dline.split(';')
                dline = dline[1]
                dline = dline.split()
                U_unit = dline[2]
               
                dline = dataf.readline()
                while dline:
                    dline = dline.strip()
                    dline = dline.split(';')
                    Us.append(float(dline[1]))
                    dline = dataf.readline()
                Uread = True



#fitting
print(Ts)
print(Is)
print(Udirections)


fit_minss = [[2., 4.],[1.6, 3.], [2.2, 4.], [1.6, 3.2], [1.4, 2.3, 3.7], [2.1, 4.], [2.2, 4.2]]

fit_maxss = [[2.7, 5.3], [2.1, 3.7], [2.4, 5.2], [2.1, 3.7], [1.6, 2.7, 5.5], [2.3, 5.3], [2.7, 4.6]]

initvals = [[0.13, 0.27], [0.025, 0.05], [0.7, 1.3], [0.11, 0.2], [0.1, 0.14, 0.26], [0.65, 1.3]]

for i,g in enumerate(gs):

    if(Ts[i] < 3. and Is[i] == 20.):
        nfits = 3
    else:
        nfits = 2

    fs = []
    if Udirections[i] == "U_26":
#        fitstr = "[0]*exp(-0.5*((x-[1])/[2])^2) + [3]"
        fitstr = "[0]*exp(-0.5*((x-[1])/[2])^2)"
    elif Udirections[i] == "U_34":
        fitstr = "[0]"
       
    for j in range(nfits):
        fs.append(TF1("Fit" + str(i+1), fitstr, fit_minss[i][j], fit_maxss[i][j]))
#    for j in range(nfits):
        if Udirections[i] == "U_26":
#            fs[j].SetParameters(0.01, (fit_minss[i][j] + fit_maxss[i][j])/2, 0.5, 0.1)
            fs[j].SetParameters(0.01, (fit_minss[i][j] + fit_maxss[i][j])/2, 0.5)
        elif Udirections[i] == "U_34":
            fs[j].SetParameter(0, initvals[i][j])

#    for j in range(nfits):
        gs[i].Fit("Fit" + str(i+1), 'R')

        print("======================")
        if Udirections[i] == "U_26":
            print(fs[j].GetParameter(1))
            print(fs[j].Eval(fs[j].GetParameter(1)))
        elif Udirections[i] == "U_34":
            print(fs[j].GetParameter(0))
        print("======================")

    c1 = TCanvas("c1", "", 200, 10, 700, 500 )
    c1.SetGrid()
    c1.cd()
    g.Draw("AP")
    for f in fs:
        f.Draw("SAME")

    c1.Update()

    c1.SaveAs(filenames[i])

