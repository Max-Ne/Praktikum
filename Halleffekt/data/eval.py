#!/usr/bin/env python
from ROOT import *

import csv

import numpy as np

gROOT.Reset();


###entries:
Ts = np.array([], dtype=np.float)
IAs = np.array([], dtype=np.float)
UAleit = np.array([], dtype=np.float)
UAHplus = np.array([], dtype=np.float)
UAHminus = np.array([], dtype=np.float)
IBs = np.array([], dtype=np.float)
UBleit = np.array([], dtype=np.float)
UBHplus = np.array([], dtype=np.float)
UBHminus = np.array([], dtype=np.float)

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

UAH = (UAHplus - UAHminus) / 2;
UBH = (UBHplus - UBHminus) / 2;


