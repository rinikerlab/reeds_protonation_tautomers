#!/usr/bin/python3 -tt
import numpy as np

def parse_file(path_dgdir):
    """
    extract data from the output of gromos++ dGslv_pbsolv calculations
    """
    return np.loadtxt(path_dgdir, skiprows=1, dtype=float).T[1]

lambdas = np.arange(0, 1.001, 0.1)
traj_indices = np.arange(1, 12, 1)

v_npbc = np.array([ parse_file(f'dgdir_lam_{i}.txt') for i in traj_indices])
v_pbc = np.array([ parse_file(f'dgdir_lam_{i}_withPBC.txt') for i in traj_indices])

dg_dir = np.trapz(v_npbc.T, x = lambdas) - np.trapz(v_pbc.T, x = lambdas)
np.save('deltaG_dir.npy', dg_dir, )
avg = np.round(np.average(dg_dir), 2)
std = np.round(np.std(dg_dir), 2)

print( f'DG_dir [kJ/mol]: {avg} +- {std}')
