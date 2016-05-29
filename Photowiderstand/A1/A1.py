from ROOT import *
import csv
import numpy as np

gROOT.Reset()

U_V = []
I_A = []

filenames=["A1dunkel.csv","A1_549nm.csv","A1_647nm.csv"]

for i in range(len(filenames)):
  U_V.append([])
  I_A.append([])
  dataf = open(filenames[i], 'r');
  for line in dataf:
    if line.startswith("#") or line.startswith(" "):
      continue;
    
    line = line.split(' ',1)
  
    U_V[i].append(float(line[0][:-2].replace(',','.')))
    I_A[i].append(float(line[1][:-2].replace(',','.')))

  dataf.close()
#  print np.array(U_V[i])
#  print np.array(I_A[i])
  
U_V = np.array(U_V)
I_A = np.array(I_A)

print "Spannungen: dunkel, 549nm, 647nm"
print U_V
print "Stromstaerken"
print I_A

errU = [0.1]*len(U_V[0])
errI = [0.01]*len(I_A[0])

#print errU

mg = TMultiGraph();

graph_dunkel = TGraphErrors(len(U_V[0]),np.array(U_V[0]),np.array(I_A[0]),np.array(errU),np.array(errI))
graph_gr = TGraphErrors(len(U_V[1]),np.array(U_V[1]),np.array(I_A[1]),np.array(errU),np.array(errI))
graph_r = TGraphErrors(len(U_V[2]),np.array(U_V[2]),np.array(I_A[2]),np.array(errU),np.array(errI))
#graph_r = TGraphErrors(len(U_V[2]),U_V[2],I_A[2])
mg.SetTitle("Strom-Spannungs-Kennlinien;U in V;I in mA")

graph_dunkel.SetMarkerStyle(kOpenCircle)
graph_dunkel.SetMarkerColor(kBlack)
graph_dunkel.SetLineColor(kBlack);

graph_gr.SetMarkerStyle(kOpenCircle)
graph_gr.SetMarkerColor(kGreen)
graph_gr.SetLineColor(kGreen);

graph_r.SetMarkerStyle(kOpenCircle)
graph_r.SetMarkerColor(kRed)
graph_r.SetLineColor(kRed);
graph_dunkel.SetMaximum(1.8)

f_dunkel = TF1("Linear Law","[0]+x*[1]")
f_dunkel.SetLineColor(kBlack);
f_dunkel.SetLineStyle(1);


f_gr = TF1("Linear Law2","[0]+x*[1]")
f_gr.SetLineColor(kGreen);
f_gr.SetLineStyle(1);

f_r = TF1("Linear Law3","[0]+x*[1]")
f_r.SetLineColor(kRed);
f_r.SetLineStyle(1);

print "----FITS----"
print "param[0] = y-Abschn"
print "param[1] = Steigung"
print "------------"
print ""

print "1) ohne Licht"
graph_dunkel.Fit(f_dunkel);
print ""
print "1) gruen"
graph_gr.Fit(f_gr);
print ""
print "1) rot"
graph_r.Fit(f_r);

leg = TLegend(.1,.7,.3,.9,"Farben");
leg.SetFillColor(0);
graph_dunkel.SetFillColor(0);
graph_gr.SetFillColor(0);
graph_r.SetFillColor(0);
leg.AddEntry(f_gr,"549 nm");
leg.AddEntry(f_r,"647 nm");
leg.AddEntry(f_dunkel,"dunkel");


c1 = TCanvas( 'c1', 'The Fit Canvas', 200, 10, 700, 500 )
c1.SetGrid()

mg.Add(graph_dunkel)
mg.Add(graph_gr)
mg.Add(graph_r)

mg.Draw("AP")

"""
graph_dunkel.Draw("AP")
graph_gr.Draw("SAME")
graph_r.DrawClone("SAME")
"""
leg.Draw("Same");

c1.Update()

c1.SaveAs("A1.pdf")

raw_input()