# -*- coding: utf-8 -*-
"""
Created on Sun Nov 21 21:21:49 2021

@author: Alex Hickey
"""
#This implementation relies on the sys.argv variable to contain the relevant
#coarse graining information.
#sys.argv should take the form: ScriptName T32 H
#where T32 is the temperature^3/2 in Kelvin and H is the applied magnetic field in Tesla.



#Password stuff:
#import getpass
#user = getpass.getuser()
#passw = getpass.getpass('Password for '+user+': ')



import numpy as np
import spec_heat
import sys


#Temperature and magnetic field information
T32 = float(sys.argv[1]) #Input is temp^3/2
T = T32**(2/3)
H = float(sys.argv[2])

#File to save to
filename = 'H {}.txt'.format(int(H))

print('Calculating heat capacity for T^3/2={} and H={}'.format(T32,H))

#Calculate heat capacity in units of kB
res = spec_heat.Cmag(T,H)

print('Heat capacity integral converged with error: {}'.format(res[1]))
print('Writing to file....')

with open(filename, "a") as file:
    
    file.write("{} {} {} {}\n".format(T32,H,res[0],res[1]))
        
print('Successfully written to file.')
    
 




