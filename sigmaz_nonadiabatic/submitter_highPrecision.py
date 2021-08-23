import subprocess as sub
import sys, json, copy
import itertools as it
import numpy as np


temp = [90, 200, 300, 400]
gList = [3500]
#stepNum = [1, 2, 4, 8]
numStep = [100] ## Toal Steps = numStep * stepNum, stepNum is acctually a further splliting
e = np.arange(-1500, 8501, 500)
gam_l = np.arange(50, 201, 50)
coup = [20,120]
coup = [20]
#gam_l = np.arange(10, 100, 20)
'''
#SBATCH --partition=scavenger
#SBATCH --exclude=dcc-fergusonlab-04,dcc-econ-[01-11]
'''
for c, ene, T, gam in it.product(coup, e, temp, gam_l):
    print(f"Submitting Job:")

    p = sub.Popen(['sbatch'], stdin=sub.PIPE)
    inp = f"""#!/bin/sh
#SBATCH --partition=scavenger
#SBATCH --exclude=dcc-aryalab-01,dcc-biostat-01,dcc-bragg-[01-04],dcc-compeb-[04,06,08,11-12],dcc-dhvi-[01,03-06],dcc-econ-[01,10],dcc-fergusonlab-[01-02,04],dcc-gcb-[02,05-09,62-64,66-67],dcc-kumarlab-01,dcc-tmolab-02,dcc-ultrasound-02,dcc-yoderlab-01,dcc-adrc-01,dcc-biodept-[01,03],dcc-biostat-[02-03],dcc-bragg-05,dcc-cagpm-[01-02],dcc-carin-[21-25],dcc-chg-[01-05],dcc-compeb-[03,05,07,09-10,13-14],dcc-dailabs-[01-05],dcc-delairelab-01,dcc-dhvi-[02,07-11],dcc-econ-[02-09,11],dcc-fergusonlab-[03,05-06],dcc-gcb-[01,03-04,65],dcc-hashimilab-02,dcc-liulab-[01-03],dcc-nicolab-01,dcc-noor-[01-02],dcc-pfister-01,dcc-rausherlab-[01-02],dcc-savageresearch-[01-02],dcc-tmolab-03,dcc-ultrasound-[01,03-11],dcc-wychem-01,dcc-yoderlab-03,dcc-carin-[01-25]
#SBATCH --mem=60G
#SBATCH --job-name=highPrecision_nonAdia_c{c}T{T}_E{ene}_G{gam}
#SBATCH --output=./highPrecision_output/sl_c{c}_{T}_{ene}_{gam}.out
#SBATCH --error=./highPrecision_output/sl_c{c}_{T}_{ene}_{gam}.err
#SBATCH -c 12
#SBATCH -t 12000
python -u  highPrecision_nonadiabatic.py {ene} {T} {gam} {c} | gzip > ./highPrecision_output/out_{c}_{T}_{ene}_{gam}.gz
    """
    p.communicate(inp.encode())
    print(f"Submitted")

