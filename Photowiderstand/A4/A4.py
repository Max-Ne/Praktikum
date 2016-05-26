from ROOT import *
import csv
import numpy as np

gROOT.Reset()

x = []
y = []
z = []

filenames=["A4.csv"]

for i in range(len(filenames)):
  x.append([])
  y.append([])
  z.append([])
  dataf = open(filenames[i], 'r');
  for line in dataf:
    if line.startswith("#") or line.startswith(" ") or line.startswith('\r') or line.startswith('\n'):
      continue;
    
    line = line.split(' ',2)
    
    #if (float(line[0][:-2].replace(',','.')) == 0. or float(line[1][:-2].replace(',','.')) == 0):
    #  continue
    
    x[i].append(float(line[0][:-2].replace(',','.')))
    y[i].append(float(line[1][:-2].replace(',','.')))
    z[i].append(float(line[1][:-2].replace(',','.')))

  dataf.close()
#  print np.array(U_V[i])
#  print np.array(I_A[i])
  
x = np.array(x)
y = np.array(y)
z = np.array(z)

print x
print y
print z


graph_1 = TGraphErrors(len(x[0]),np.log(x[0]),np.log(y[0]))
graph_beg = TGraphErrors(4,np.log(x[0][:4]),np.log(y[0][:4]))
graph_end = TGraphErrors(7,np.log(x[0][-7:]),np.log(y[0][-7:]))
graph_2 = TGraphErrors(len(x[0]),x[0],np.tan(z[0]))

graph_1.SetMarkerStyle(kOpenCircle)
graph_1.SetMarkerColor(kBlack)
graph_1.SetLineColor(kBlack);
#graph_1.SetMaximum(1.8)

#mg.GetXaxis().SetTitleOffset(0);

f_beg = TF1("horiz.","[0]",0,8)
f_beg.SetLineColor(kBlue);
f_beg.SetLineStyle(2);


f_end = TF1("Linear Law","[0]+x*[1]",0,8.5)
f_end.SetLineColor(kBlue);
f_end.SetLineStyle(2);

graph_beg.Fit(f_beg);
graph_end.Fit(f_end);


c1 = TCanvas( 'c1', 'The Fit Canvas', 200, 10, 700, 500 )
c1.SetGrid()

mg = TMultiGraph();
mg.Add(graph_1)
mg.SetTitle("Amplitude #ddot{u}ber Frequenz;log (#omega / Hz);log (A / #muA)")



#mg.GetXaxis().SetTitle("aaa");
mg.Draw("AP")
f_beg.Draw("SAME")
f_end.Draw("SAME")
c1.Update()

x = (f_beg.GetParameter(0) - f_end.GetParameter(0))/(f_end.GetParameter(1))
vertical = TLine (x,gPad.GetUymin(),x,gPad.GetUymax())
vertical.SetLineColor(kRed)
vertical.SetLineStyle(1)
vertical.SetLineWidth(2)
vertical.Draw("SAME")
c1.Update()

leg = TLegend(.7,.7,.9,.9,"");
leg.SetFillColor(0);
graph_1.SetFillColor(0);
leg.AddEntry(graph_1,"Messdaten");
leg.AddEntry(f_beg,"lin. Fit 1");
leg.AddEntry(f_end,"lin. Fit 2");
leg.AddEntry(vertical,"Schnittpunkt","L");

leg.Draw("Same");

c1.Update()

c1.SaveAs("A4_2fits.pdf")

print "Intersect: ", x
"""
c2 = TCanvas( 'c1', 'The Fit Canvas', 200, 10, 700, 500 )
c2.SetGrid()
c2.cd()

graph_2.SetMarkerStyle(kOpenCircle)
graph_2.SetMarkerColor(kBlack)
graph_2.SetLineColor(kBlack);

graph_2.Draw()

c2.Update()
"""
raw_input()
