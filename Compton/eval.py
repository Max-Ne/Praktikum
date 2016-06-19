from ROOT import *
import numpy as np

gROOT.Reset()

#####################
# VALUES FOR CALCULATION
#####################

d = 2.55 					# Durchmesser Kristall, cm
r = 21.5 					# Abstand Target Kristall, cm

Z_AL = 13. 					# Ordnungszahl
L = 6.022140857 * (10**23)	 		# mol**(-1) - Avogadro-Konstante
A_AL = 26.9815385 				# u
rho_AL = 2.70					# g/cm**3 (20 Celsius)
d_target = 1.					# cm
l_target = 1.					# cm

Phi_Null = 1.54 * (10**6)			# 1/(cm**2 s)
Phi_Null_err = 0.09 * (10**6)			# 1/(cm**2 s)
Delta_T = 2016 - 1971				# a
eps_inv = 2.08					# 1
eps_inv_err = 0.01				# 1
T_Half = 30.					# a

t = 300.					# s, Messzeit

Delta_Omega = np.pi * (d/2)*(d/2) / (r*r)	# 1

Phi = Phi_Null * (2**(-(Delta_T/T_Half)))			# 1/(cm**2 s)
Phi_err = Phi_Null_err * (2**(-(Delta_T/T_Half)))		# 1/(cm**2 s)

n = L/A_AL * Z_AL * rho_AL * np.pi * (d_target/2.)*(d_target/2.) * l_target	# 1


####################
# GET DATA -> LOOP
####################

#x - channels, y - number of events
x_bkg = []
y_bkg = []
x_tgt = []
y_tgt = []
x = []
y = []
y_err = []


filenames_bkg=[]
filenames_tgt=[]

for i in range(9):
  deg = i * 10 + 20 # deg = [20,30,...,100]
  filenames_bkg.append("CS137_"+str(deg)+"degree_bkg.txt")
  filenames_tgt.append("CS137_"+str(deg)+"degree_tgt.txt")

for i in range(len(filenames_bkg)):
  x_bkg.append([])
  y_bkg.append([])
  x_tgt.append([])
  y_tgt.append([])
  x.append([])
  y.append([])
  y_err.append([])
  
  # open target file 
  dataf = open("data/" + filenames_tgt[i], 'r');
  for line in dataf:
    if line.startswith("#") or line.startswith('\r') or line.startswith('\n'):
      continue;
    
    line = line.strip()
    line = line.split(' ',1)
    line[0] = line[0].strip()
    line[1] = line[1].strip()
    
    x_tgt[i].append(float(line[0].replace(',','.')))
    y_tgt[i].append(float(line[1].replace(',','.')))

  dataf.close()
  
  # open background file
  dataf = open("data/" + filenames_bkg[i], 'r');
  for line in dataf:
    if line.startswith("#") or line.startswith('\r') or line.startswith('\n'):
      continue;
    
    line = line.strip()
    line = line.split(' ',1)
    line[0] = line[0].strip()
    line[1] = line[1].strip()
    
    x_bkg[i].append(float(line[0].replace(',','.')))
    y_bkg[i].append(float(line[1].replace(',','.')))

  dataf.close()
  
  # subtract and do error calculation
  if not(x_tgt[i] == x_bkg[i]):
    print 'ERROR, CHANNEL NUMBER NOT THE SAME!'
  x[i] = x_tgt[i]
  for j in range(len(y_tgt[i])):
    y[i].append(y_tgt[i][j] - y_bkg[i][j])
    y_err[i].append( np.sqrt(y_tgt[i][j] + y_bkg[i][j]) )
    # poisson error: n = n_1 - n_2 -> sig_n = sqrt(sig_n_2 **2 + sig_n_1 **2) = sqrt(n_2 + n_1)
  
x = np.array(x)
y = np.array(y)
y_err = np.array(y_err)

#assume poisson error
x_err = np.zeros(x.shape)


#################
# PART I - DIF. XSEC with respect to solid angel
#################

R = np.zeros(9)
R_err = np.zeros(9)
dif_xsec = np.zeros(9)
dif_xsec_err = np.zeros(9)
angel_deg = np.zeros(9)

for i in range(9):
  angel_deg[i] = i*10 + 20
  
  R[i] = y[i].sum()
  R_err[i] = np.sqrt(sum(y_err[i]**2))
  
  dif_xsec[i] = float(R[i])/Delta_Omega * 1./(Phi * n * t) * eps_inv * (10**25)
  #units		1  /     1	  1./(cm**-2 s**-1 * s) * 1		= cm**(-1) * 10**25
  #error on: R, Phi, eps_inv

  dif_xsec_err[i] = np.sqrt( (dif_xsec[i]/R[i]*R_err[i])**2 + (dif_xsec[i]/Phi * Phi_err)**2 + (dif_xsec[i]/eps_inv * eps_inv_err)**2 )

print "angel in degree, dif_xsec, dif_xsec_err"
for a,xs,xse in zip(angel_deg, dif_xsec, dif_xsec_err):
  print a,xs,xse


############
# PART II - ENERGY SHIFT
############
#1. MAKE 10 PLOTS WITH GAUS FITS AND EXTRACT CHANNELS
fit_min = [226,209,183,161,131,114,97,81,77]
fit_max = [301,278,250,214,196,172,144,130,111]

channels, channels_err = np.zeros(9), np.zeros(9)
graphs = []
graphs_no_err = []
canvas = []
fit_functions = []
legs = []

for i in range(len(filenames_bkg)):
  graphs.append(TGraphErrors(len(x[i]),x[i],y[i],x_err[i],y_err[i]))
  graphs_no_err.append(TGraphErrors(len(x[i]),x[i],y[i]))
  canvas.append(TCanvas('c'+str(i+1), str(i+1), 200, 10, 700, 500 ))
  canvas[i].SetGrid();
  canvas[i].cd();
  
  fit_functions.append(TF1("f"+str(i+1),"gaus",fit_min[i],fit_max[i]))
  
  graphs_no_err[i].SetTitle("Polar Angle #Theta = " + str(i*10 + 20) + "#circ; channel; # Events")
  graphs_no_err[i].SetMinimum(0)
  graphs[i].Fit("f"+str(i+1),"R")  
  
  legs.append(TLegend(.6,.8,.9,.9,""));
  legs[i].SetFillColor(0);
  graphs_no_err[i].SetFillColor(0);
  legs[i].AddEntry(graphs_no_err[i],"data points", "p");
  legs[i].AddEntry(fit_functions[i],"gaus fit in given range");

  
  channels[i] = fit_functions[i].GetParameter(1)
  channels_err[i] = fit_functions[i].GetParameter(2)
  
  #graphs[i].Draw("AP")
  graphs_no_err[i].SetMarkerSize(2.0)
  graphs_no_err[i].Draw("AP")
  fit_functions[i].Draw("SAME")
  legs[i].Draw()
  
  canvas[i].Update();
  canvas[i].SaveAs("./plots/"+str(i*10 + 20)+"_deg.pdf")

#2. CHANNELS TO ENERGIES
calib_inters = -302.810
calib_slope = 3.64232
calib_inters_err = 148.205
calib_slope_err = 0.513385
# energy = calib_inters + calib_slope * channels

energies = calib_inters + calib_slope*channels
#energies_err = np.sqrt(channels_err**2 + calib_inters_err**2 + (channels - calib_inters)**2 * (calib_slope_err / calib_slope)**2) / calib_slope
energies_err = np.sqrt(calib_inters_err**2 + (channels*calib_slope_err)**2 + (channels_err*calib_slope)**2)

print channels
print channels_err
print energies
print energies_err



#3. LINEAR FIT ACCORDING TO FORMULAR IN PREP

# formular: 1/E' = 1/E + 1/(m_0 c**2) * (1 - cos \theta )

angel_pi = angel_deg *np.pi / 180.
one_m_cos_theta = 1. - np.cos(angel_pi)
one_m_cos_theta_err = np.zeros(one_m_cos_theta.shape)

graph_2 = TGraphErrors(len(angel_pi), one_m_cos_theta, 1./energies, one_m_cos_theta_err, energies_err/(energies**2))

graph_2.SetMarkerStyle(kOpenCircle)
graph_2.SetMarkerColor(kBlue)
graph_2.SetLineColor(kBlue);

graph_2.GetYaxis().SetNdivisions(502)

# fit function
f_lin = TF1("Linear Law","[0]+x*[1]")
f_lin.SetLineColor(kRed);
f_lin.SetLineStyle(1);

graph_2.Fit(f_lin)
graph_2.SetTitle("Linear Fit of inverse Energies;1 - cos (#theta);E^{-1} in keV^{-1}     ")

c2 = TCanvas('c_2', 'canvas_2', 200, 10, 700, 500 )
c2.SetGrid()
c2.cd()

last_leg = TLegend(.1,.8,.3,.9,"");
last_leg.SetFillColor(0);
graph_2.SetFillColor(0);
last_leg.AddEntry(graph_2,"data points");
last_leg.AddEntry(f_lin,"linear fit","l");

graph_2.Draw("AP")
last_leg.Draw("SAME")

c2.Update()
c2.SaveAs("./plots/inv_el_mass.pdf")

inters = f_lin.GetParameter(0)
inters_err = f_lin.GetParError(0)
slope = f_lin.GetParameter(1)
slope_err = f_lin.GetParError(1)
#print inters, inters_err, slope, slope_err 

inv_el_mass = 1./slope
inv_el_mass_err = slope_err/(slope**2)

print 'inv electron mass in keV: ',inv_el_mass, ' pm ', inv_el_mass_err

raw_input()
"""
#############
## PART I - FIT SPECIFIC RANGES IN DATA WITH GAUS
#############

# CO60, CS137, NA22, NA22.
# fitranges
fit_min = [325,255,188,360]
fit_max = [395,303,242,428]

caligraphs = []
caligraphs2 = []
calicanvas = []
fit_functions = []


# loop over different sources, each source has its own canvas. 2 fits for NA22 (i=2)
for i in range(len(filenames)):
  
  fit_functions.append(TF1("f"+str(i+1),"gaus",fit_min[i],fit_max[i]))
  
  if i == 0:
    canvasname = "{}^{60}Co"
    outn = "CO_60"
  elif i == 1:
    canvasname = "{}^{137}Cs"
    outn = "CS_137"
  elif i ==2:
    canvasname = "{}^{22}Na"
    outn = "NA_22"
    fit_functions.append(TF1("f"+str(i+1)+"_2","gaus",fit_min[i+1],fit_max[i+1]))
    
  
  calicanvas.append(TCanvas('c'+str(i+1), canvasname, 200, 10, 700, 500 ))
  calicanvas[i].SetGrid()
  
  caligraphs2.append(TGraphErrors(len(x[i]),x[i],y[i],x_err[i],y_err[i]))
  caligraphs.append(TGraphErrors(len(x[i]),x[i],y[i]))
  caligraphs[i].SetTitle(canvasname + ";channel;# Events")
  
  calicanvas[i].cd()
  
  caligraphs2[i].Fit("f"+str(i+1),"R")  
  if i == 2:
    caligraphs2[i].Fit("f"+str(i+1)+"_2","R")  
  
  caligraphs[i].Draw("AP")
  fit_functions[i].Draw("SAME")
  if i == 2:
    fit_functions[i+1].Draw("SAME")
  
  calicanvas[i].Update()
  calicanvas[i].SaveAs("./plots/calibration/" + outn + "_fit.pdf")

print ""
print "-------LINEAR FIT--------"
print ""


#############
## PART II - FIT ACQUIRED VALUES LINEARLLY
#############

# energies have to be changed (Mitschrieb!!)
energies = np.array([300.,250.,200.,350.])
energies_err = np.zeros(energies.shape)
channels = []
channels_err = []

# get mean of gaus and sigmas
for i in range(len(filenames) + 1):
  mean = fit_functions[i].GetParameter(1);
  sigma = fit_functions[i].GetParameter(2);
  channels.append(mean)
  channels_err.append(sigma)
  
channels = np.array(channels)
channels_err = np.array(channels_err)

# graph for lin fitting
graph_lin_fit = TGraphErrors(len(energies), energies, channels, energies_err, channels_err)

# cosmetics
graph_lin_fit.SetMarkerStyle(kOpenCircle)
graph_lin_fit.SetMarkerColor(kBlue)
graph_lin_fit.SetLineColor(kBlue);

# fit function
f_lin = TF1("Linear Law","[0]+x*[1]")
f_lin.SetLineColor(kBlack);
f_lin.SetLineStyle(1);

# fit
graph_lin_fit.Fit(f_lin);
graph_lin_fit.SetTitle("Linear Fit of Channels;Energy in keV;channel")

# plot
c4 = TCanvas( 'c4', 'The Fit Canvas', 200, 10, 700, 500 )
c4.SetGrid()

graph_lin_fit.Draw("AP")
c4.Update()

c4.SaveAs("./plots/calibration/lin_fit.pdf")

print "--------CO_60--------------"
print "fit range:  " + str(fit_min[0]) + " ... " + str(fit_max[0])
print "fit mean:  ", channels[0]
print "fit sigma: ", channels_err[0]
print "energy:    ", energies[0]

print "--------CS_137-------------"
print "fit range:  " + str(fit_min[1]) + " ... " + str(fit_max[1])
print "fit mean:  ", channels[1]
print "fit sigma: ", channels_err[1]
print "energy:    ", energies[1]

print "--------NA_22_FIT_I--------"
print "fit range:  " + str(fit_min[2]) + " ... " + str(fit_max[2])
print "fit mean:  ", channels[2]
print "fit sigma: ", channels_err[2]
print "energy:    ", energies[2]

print "--------NA_22_FIT_II--------"
print "fit range:  " + str(fit_min[3]) + " ... " + str(fit_max[3])
print "fit mean:  ", channels[3]
print "fit sigma: ", channels_err[3]
print "energy:    ", energies[3]


raw_input()
"""