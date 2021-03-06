from ROOT import *
import csv
import numpy as np

gROOT.Reset()

x = []
y = []

filenames=["A3.csv"]

for i in range(len(filenames)):
  x.append([])
  y.append([])
  dataf = open(filenames[i], 'r');
  for line in dataf:
    if line.startswith("#") or line.startswith(" ") or line.startswith('\r') or line.startswith('\n'):
      continue;
    
    line = line.split(' ',1)
    
    #if (float(line[0][:-2].replace(',','.')) == 0. or float(line[1][:-2].replace(',','.')) == 0):
    #  continue
    
    x[i].append(float(line[0][:-2].replace(',','.')))
    y[i].append(float(line[1][:-2].replace(',','.')))

  dataf.close()
#  print np.array(U_V[i])
#  print np.array(I_A[i])
  
x = np.array(x)
y = np.array(y)

print x
print y


graph_1 = TGraphErrors(len(x[0]),x[0],y[0])


graph_1.SetMarkerStyle(kOpenCircle)
graph_1.SetMarkerColor(kBlue)
graph_1.SetLineColor(kBlue);
#graph_1.SetMaximum(1.8)

#mg.GetXaxis().SetTitleOffset(0);

f_1 = TF1("Linear Law","[0]+x*[1]")
f_1.SetLineColor(kBlack);
f_1.SetLineStyle(1);

#graph_1.Fit(f_1);

leg = TLegend(.1,.8,.3,.9,"Photostrom");
leg.SetFillColor(0);
graph_1.SetFillColor(0);
leg.AddEntry(graph_1,"Messdaten");
#leg.AddEntry(f_1,"Fit");


c1 = TCanvas( 'c1', 'The Fit Canvas', 200, 10, 700, 500 )
c1.SetGrid()


mg = TMultiGraph();
mg.Add(graph_1)
mg.SetTitle("Photostrom #ddot{u}ber Wellenl#ddot{a}nge;#lambda in nm;I in mA")
#mg.GetXaxis().SetTitle("aaa");
mg.Draw("AP")
c1.Update()


leg.Draw("Same");

c1.Update()

c1.SaveAs("A3.pdf")

raw_input()
