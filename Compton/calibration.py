from ROOT import *
import numpy as np

gROOT.Reset()

############
# GET CALIBRATION DATA
############

#x - channels, y - number of events
x = []
y = []

filenames=["calibrationCO60.txt","calibrationCS137.txt","calibrationNA22.txt"]

for i in range(len(filenames)):
  x.append([])
  y.append([])
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

  dataf.close()

x = np.array(x)
y = np.array(y)

#assume poisson error
x_err = np.zeros(x.shape)
y_err = np.sqrt(y)


#############
## PART I - FIT SPECIFIC RANGES IN DATA WITH GAUS
#############

# CO60, CS137, NA22, NA22, CO60(2.)
# fitranges
fit_min = [325,255,188,360,440]
fit_max = [395,303,242,428,490]

caligraphs = []
caligraphs2 = []
calicanvas = []
fit_functions = []
legs = []


# loop over different sources, each source has its own canvas. 2 fits for NA22 (i=2)
for i in range(len(filenames)):
  
  fit_functions.append(TF1("f"+str(i+1),"gaus",fit_min[i],fit_max[i]))
  
  if i == 0:
    canvasname = "{}^{60}Co"
    outn = "CO_60"
    fit_cobalt_2 = TF1("f_CO_2","gaus",fit_min[-1],fit_max[-1])
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
  if i == 0:
    caligraphs2[i].Fit("f_CO_2","R")
  if i == 2:
    caligraphs2[i].Fit("f"+str(i+1)+"_2","R")  
    
  legs.append(TLegend(.6,.8,.9,.9,""));
  legs[i].SetFillColor(0);
  caligraphs[i].SetFillColor(0);
  legs[i].AddEntry(caligraphs[i],"data points", "p");
  legs[i].AddEntry(fit_functions[i],"gaus fit in given range");
  
  caligraphs[i].Draw("AP")
  fit_functions[i].Draw("SAME")
  if i == 0:
    fit_cobalt_2.Draw("SAME")
  if i == 2:
    fit_functions[i+1].Draw("SAME")
  
  legs[i].Draw("SAME")
  
  calicanvas[i].Update()
  calicanvas[i].SaveAs("./plots/calibration/" + outn + "_fit.pdf")

print ""
print "-------LINEAR FIT--------"
print ""


#############
## PART II - FIT ACQUIRED VALUES LINEARLLY
#############

# energies have to be changed (Mitschrieb!!)
# CO, CO, CS, NA, NA in keV
energies = np.array([1173.240,1332.508,661.659,511.0,1274.577])
energies_err = np.zeros(energies.shape)
channels = []
channels_err = []

# get mean of gaus and sigmas
for i in range(len(filenames) + 1):
  mean = fit_functions[i].GetParameter(1);
  sigma = fit_functions[i].GetParameter(2);
  channels.append(mean)
  channels_err.append(sigma)
  if i == 0:
    mean = fit_cobalt_2.GetParameter(1);
    sigma = fit_cobalt_2.GetParameter(2);
    channels.append(mean)
    channels_err.append(sigma)
  
channels = np.array(channels)
channels_err = np.array(channels_err)

#print channels
#print channels_err

# graph for lin fitting
graph_lin_fit = TGraphErrors(len(energies),  channels, energies, channels_err, energies_err)

# cosmetics
graph_lin_fit.SetMarkerStyle(kOpenCircle)
graph_lin_fit.SetMarkerColor(kBlue)
graph_lin_fit.SetLineColor(kBlue);

# fit function
f_lin = TF1("Linear Law","[0]+x*[1]")
f_lin.SetParameter(0,100.)
f_lin.SetParameter(1,200.)
f_lin.SetLineColor(kRed);
f_lin.SetLineStyle(1);

# fit
graph_lin_fit.Fit(f_lin);
graph_lin_fit.SetTitle("Linear Fit of Channels;channel;Energy in keV")
graph_lin_fit.GetYaxis().SetTitleOffset(1.2)

# plot
c4 = TCanvas( 'c4', 'The Fit Canvas', 200, 10, 700, 500 )
c4.SetGrid()

last_leg = TLegend(.1,.8,.3,.9,"");
last_leg.SetFillColor(0);
graph_lin_fit.SetFillColor(0);
last_leg.AddEntry(graph_lin_fit,"data points");
last_leg.AddEntry(f_lin,"linear fit","l");
  

graph_lin_fit.Draw("AP")
last_leg.Draw("SAME");
c4.Update()

c4.SaveAs("./plots/calibration/lin_fit.pdf")

print "--------CO_60--------------"
print "fit range:  " + str(fit_min[0]) + " ... " + str(fit_max[0])
print "fit mean:  ", channels[0]
print "fit sigma: ", channels_err[0]
print "energy:    ", energies[0]

print "--------CO_60_FIT_II-------"
print "fit range:  " + str(fit_min[1]) + " ... " + str(fit_max[1])
print "fit mean:  ", channels[1]
print "fit sigma: ", channels_err[1]
print "energy:    ", energies[1]

print "--------CS_137-------------"
print "fit range:  " + str(fit_min[2]) + " ... " + str(fit_max[2])
print "fit mean:  ", channels[2]
print "fit sigma: ", channels_err[2]
print "energy:    ", energies[2]

print "--------NA_22_FIT_I--------"
print "fit range:  " + str(fit_min[3]) + " ... " + str(fit_max[3])
print "fit mean:  ", channels[3]
print "fit sigma: ", channels_err[3]
print "energy:    ", energies[3]

print "--------NA_22_FIT_II--------"
print "fit range:  " + str(fit_min[4]) + " ... " + str(fit_max[4])
print "fit mean:  ", channels[4]
print "fit sigma: ", channels_err[4]
print "energy:    ", energies[4]


raw_input()
