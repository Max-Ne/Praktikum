#!/usr/bin/env python3
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
# Last Modified : Sa 16 Jul 2016 22:13:38 CEST
#
#####################################

import numpy as np
import matplotlib.pyplot as plt

#setup
T = 0. #K
I = 0. #muA

U_unit = ''

Us = []
Bs = []

Bread = False
Uread = False


with open("data/index.txt", 'r') as indexf:
    for line in indexf:
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

        if (Bread and Uread):
            #TODO convert channel1 to magnetic field and  render all the shit
            Bs = np.array(Bs, dtype=float)
            Us = np.array(Us, dtype=float)
            plt.plot(Bs, Us, 'ro')
            plt.show()
            Bread = False
            Uread = False




