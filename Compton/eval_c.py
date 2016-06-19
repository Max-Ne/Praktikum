from ROOT import *
import numpy as np

gROOT.Reset()


####################
# GET DATA -> LOOP
####################

#x - channels, y - number of events
x = []
y = []
y_err = []

filenames=["CS137_AL_20degree_tgt.txt","CS137_CU_20degree_tgt.txt","CS137_FE_20degree_tgt.txt","CS137_PB_20degree_tgt.txt","CS137_20degree_bkg.txt"]

for i in range(len(filenames)):
  x.append([])
  y.append([])
  y_err.append([])
  
  # open target file 
  dataf = open("data/" + filenames[i], 'r');
  for line in dataf:
    if line.startswith("#") or line.startswith('\r') or line.startswith('\n'):
      continue;
    
    line = line.strip()
    line = line.split(' ',1)
    line[0] = line[0].strip()
    line[1] = line[1].strip()
    
    x[i].append(float(line[0].replace(',','.')))
    y[i].append(float(line[1].replace(',','.')))
    y_err[i].append(np.sqrt(float(line[1].replace(',','.'))))

  dataf.close()
  
    
x = np.array(x)
y = np.array(y)
y_err = np.array(y_err)

# subtract and do error calculation
for i in range(len(filenames) - 1):
  if not (x[i][j] == x[-1][j] for j in range(len(x[i]))):
    print 'ERROR: CHANNEL NUMBER NOT THE SAME. FILE: ' + str(i)
  y[i] = y[i] - y[-1]
  y_err[i] = np.sqrt(y_err[i]**2 + y_err[-1]**2)
  

#assume poisson error
x_err = np.zeros(x.shape)


#########################
### CALCULATION
#########################
# AL, CU, FE, PB

# meassured data in t = 300s
R = np.array([y[0].sum(),y[1].sum(),y[2].sum(),y[3].sum()])
R_err = np.sqrt(np.array([(y[0]**2).sum(),(y[1]**2).sum(),(y[2]**2).sum(),(y[3]**2).sum()]))
print R
print R_err

#desities, atomic weights, atomic numbers
rho = np.array([2.70,8.92,7.874,11.342])
at_weight = np.array([26.9815385,63.546,55.845,207.2])
at_number = np.array([13,29,26,82])

#dif xsec propto
dif_xsec = R * at_weight / rho / at_number
dif_xsec_err = dif_xsec / R * R_err

print dif_xsec
print dif_xsec_err


