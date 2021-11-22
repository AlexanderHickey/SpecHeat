# -*- coding: utf-8 -*-
"""
Created on Sun Nov 21 21:21:49 2021

@author: Alex Hickey
"""
import numpy as np
import pandas
import os, subprocess
import sys

time = '00:29:00' #Run time
memory = '100M' #Memory per core required, this is NOT shared between jobs


#Load Onose data
H0, H5, H9 = pandas.read_csv('H _ 0T.csv'), pandas.read_csv('H _ 5T.csv'), pandas.read_csv('H _ 9T.csv')
T0, T5, T9 = [H0['Temp^1.5'][j] for j in range(len(H0))], [H5['Temp^1.5'][j] for j in range(len(H5))], [H9['Temp^1.5'][j] for j in range(len(H9))]
C0, C5, C9 = [H0['C'][j] for j in range(len(H0))], [H5['C'][j] for j in range(len(H5))], [H9['C'][j] for j in range(len(H9))]



preamble = ["#!/bin/bash\n",
            "#SBATCH --account=def-gingras\n",
            "#SBATCH --time={}\n".format(time),
            "#SBATCH --nodes=1\n",
            "#SBATCH --ntasks=1\n",
            "#SBATCH --mem={}\n".format(memory),
            "#SBATCH --mail-user=alexander.hickey@uwaterloo.ca\n",
            "#SBATCH --mail-type=FAIL\n",
            "\n",
            "module load scipy-stack\n"]

def execute(T32,H,read = False):

    
    #Generate shell file
    with open('run.sh','w') as shell:

        shell.write("".join(preamble))
        shell.write("python main.py {} {}".format(T32,H))
        
    #Print out contents of shell file
    if read:
        with open('run.sh','r') as file:    
            print(file.read())
    
    #Submit job to scheduler
    result = subprocess.run(['sbatch run.sh'], stdout=subprocess.PIPE, shell=True)
    print(result.stdout.decode('utf-8'))
    
    #Delete shell file
    os.remove('run.sh')
    
def main():

    for j in range(len(T0)):
        
        H = 1e-13
        T32 = T0[j]

        execute(T32,H,read = False)
    
    for j in range(len(T5)):
    
        H = 5+1e-13
        T32 = T5[j]

        execute(T32,H,read = False)
    
    for j in range(len(T9)):
    
        H = 9+1e-13
        T32 = T9[j]

        execute(T32,H,read = False)
        
if __name__ == "__main__":

    main()
    