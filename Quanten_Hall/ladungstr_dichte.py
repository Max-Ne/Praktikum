import numpy as np
from ROOT import *

B = np.array([1.297,1.830,3.272,1.831,3.292,2.369,4.406,1.855,3.455])
B_err_stat = np.array([0.006,0.005,0.004,0.004,0.004,0.007,0.006,0.004,0.003])
B_err_sys = 0.004

U_H = np.array([0.08418,0.1369,0.2584,0.1315,0.2636,0.6459,1.306,0.6565,1.303])
U_H_err_stat = np.array([0.00026,0.0002,0.00008,0.0003,0.0002,0.0009,0.0003,0.0012,0.0003])
U_H_err_sys = 0.004

I = np.array([20,20,20,20,20,100,100,100,100])*10**-6
I_err_sys = 0.01*(10**-6)

e = 1.6021766*(10**-19)*10000

n_s = I*B/(U_H*e)
n_s_err_sys = np.sqrt((I_err_sys*B/(e*U_H))**2 + (I*B_err_sys/(e*U_H))**2 + (I*B/(e*U_H*U_H)* U_H_err_sys)**2)
n_s_err_stat = np.sqrt((I*B_err_stat/(e*U_H))**2 + (I*B/(e*U_H*U_H)* U_H_err_stat)**2)


print n_s/(10**11)
print n_s_err_sys/(10**11)
print n_s_err_stat/(10**11)
