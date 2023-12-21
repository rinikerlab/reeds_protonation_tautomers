#!/usr/bin/python3 -tt
import numpy as np

def dG(lambdas, charges, v):
    """
    Numerical integration based on Maria Reif 2014(?) article, eq. 12
    where v is written phi in the article
    """
    dG = 0
    for i in range(1,len(lambdas)):       
        delta_lambda = lambdas[i] - lambdas[i-1]
        delta_q = charges[len(lambdas)-1] - charges[0]         
        for atom in range(0, len(delta_q)):
            dG += delta_q[atom] * delta_lambda * (v[i][atom] + v[i-1][atom])/2 
    return dG

def parse_charges(path_dgslv_pbsolv):
    """
    extract data from the output of gromos++ dGslv_pbsolv calculations
    """
    data = np.loadtxt(path_dgslv_pbsolv, skiprows=1, dtype=str)
    return np.array(data.T[3], dtype=float)

def parse_potentials(path_dgslv_pbsolv):
    """
    extract data from the output of gromos++ dGslv_pbsolv calculations
    """
    
    data = np.loadtxt(path_dgslv_pbsolv, skiprows=1, dtype=str)
    return np.array(data.T[4:], dtype=float)

# To figure out, why are lambdas reversed compared to files here!!!!

n_snapshots = 50
n_pots = 6

lambdas = np.arange(0, 1.001, 0.1)
lambda_idx = np.arange(1, 12, 1)

all_data = np.zeros([n_snapshots, n_pots+1])

for k in range(n_snapshots):
    charges = np.array([parse_charges(f'dgsolv_lam_{lam}_{k+1}.out') for lam in lambda_idx])
    pot_energies = np.array([parse_potentials(f'dgsolv_lam_{lam}_{k+1}.out') for lam in lambda_idx])

    n_pots = 6
    pot_labels = ['DG_POL', 'NPBC_SLV', 'NPBC_VAC','PBC_SLV', 'PBC_VAC', 'FFT_LS_PBC', 'FFT_RF_PBC']
    
    for i in range(n_pots):
        all_data[k][i+1] = dG(lambdas, charges, pot_energies[:,i,:])
    all_data[k][0] = (all_data[k][1] - all_data[k][2]) - (all_data[k][3] - all_data[k][4]) + (all_data[k][5] - all_data[k][6])

np.save('deltaG_pol_all_dat.npy', all_data )
np.save('deltaG_pol.npy', all_data.T[0])

avg = np.round(np.average(all_data.T[0]),2)
std = np.round(np.std(all_data.T[0]),2)

print( f'DG_pol [kJ/mol]: {avg} +- {std}')

