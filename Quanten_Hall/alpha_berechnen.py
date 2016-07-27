import numpy as np
from ROOT import *

gROOT.Reset()

U_H = np.array([0.08418,0.1369,0.2584,0.1315,0.2636,0.6459,1.306,0.6565,1.303])
U_H_err_stat = np.array([0.00026,0.0002,0.00008,0.0003,0.0002,0.0009,0.0003,0.0012,0.0003])
U_H_err_sys = 0.004

ff_i = np.array([6,4,2,4,2,4,2,4,2])

I = np.array([20,20,20,20,20,100,100,100,100])*(10**-6)
I_err_sys = 0.01*(10**-6)

c = 299792458.
mu0 = 4*np.pi*(10**(-7))

alpha = mu0 * c * I / (U_H * 2 * ff_i)
alpha_err_sys  = np.sqrt( ((mu0*c)/(2*ff_i))**2 * ( ((I* U_H_err_sys/(U_H**2)))**2 + ((I_err_sys/U_H))**2 ))
alpha_err_stat = np.sqrt( ((mu0*c)/(2*ff_i))**2 * ((I*U_H_err_stat/(U_H**2)) )**2 )

alpha_err_sys_compl = 0.

for i in range(len(alpha_err_sys)):
  alpha_err_sys_compl = np.sqrt(alpha_err_sys_compl**2 + alpha_err_sys[i]**2)

alpha_err_sys_compl = alpha_err_sys_compl / (len(alpha_err_sys)+1)


print alpha
print alpha_err_sys
print alpha_err_sys_compl
print alpha_err_stat
print 1/137.

x_a = np.array([0.,1.,2.,3.,4.,5.,6.,7.,8.])
x_err = np.array([0.,0.,0.,0.,0.,0.,0.,0.,0.])

graph = TGraphErrors(len(alpha),x_a,np.array(alpha),x_err,alpha_err_stat)
graph.SetTitle("Feinstrukturkonstante #alpha f#ddot{u}r die einzelnen Plateaus;Nummerierung;#alpha")

graph.SetMarkerStyle(kOpenCircle)
graph.SetMarkerColor(kBlue)
graph.SetLineColor(kBlue);


#graph.SetMaximum(1.2*graph.GetMaximum())
#graph.SetMaximum(0)

f = TF1("Linear Law","[0]")
f.SetLineColor(kRed);
f.SetLineStyle(1);

f_th = TF1("Linear Law","1/137.",0,9)
f_th.SetLineColor(kGreen);
f_th.SetLineStyle(2);


c1 = TCanvas( 'c1', 'The Fit Canvas', 200, 10, 700, 500 )
c1.SetGrid()

graph.Draw("APE")
graph.GetYaxis().SetNdivisions(505)
graph.GetYaxis().SetRangeUser(0.005,0.009)

graph.Fit(f)

leg = TLegend(.7,.1,.9,.3,"");
leg.SetFillColor(0);
graph.SetFillColor(0);
f.SetFillColor(0);
f_th.SetFillColor(0);
leg.AddEntry(graph,"gemessene Werte");
leg.AddEntry(f,"Fit");
leg.AddEntry(f_th,"th. Wert 1/137");


graph.Draw("AP")
f_th.Draw("SAME")
leg.Draw("SAME")

c1.SaveAs("plots/alpha.pdf")
raw_input()
