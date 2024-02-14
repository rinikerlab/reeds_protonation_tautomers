#!/usr/bin/env python3
import os, sys, glob
sys.path.append(os.getcwd())

from global_definitions import fM, bash
from global_definitions import name, root_dir
from global_definitions import gromosXX_bin, gromosPP_bin, ene_ana_lib
from global_definitions import in_top_file, in_pert_file, in_disres_file
from global_definitions import undersampling_frac_thresh

from reeds.modules import do_RE_EDS_mixedOptimisation as mixedOpt


#Paths
in_name = name+"_mixed_opt_long"
out_sopt_dir = root_dir+"/d_mixed_opt_long"
next_sopt_dir = root_dir+"/c_eoff_estim/analysis/next/"
optimized_states_dir = root_dir + "/a_optimizedStates/analysis/next"
lower_bound_dir = root_dir + "/b_lowerBound/analysis/next"

##make folder
out_sopt_dir = bash.make_folder(out_sopt_dir)

template_imd = next_sopt_dir +"/next.imd"

#In-Files
topology = fM.Topology(top_path=in_top_file, disres_path=in_disres_file, perturbation_path=in_pert_file)
coords = glob.glob(next_sopt_dir+"/*cnf")
system =fM.System(coordinates=coords,name=in_name,    top=topology)
print(system)

#Additional Options
## Simulation Params
job_duration="24:00:00"
nmpi_per_replica = 8
iterations = 10
memory = 1000

## EoffRB - Params
learningFactors = None
individualCorrection = False
### Pseudocount
intensity_factor = 5

# S-opt options
run_NGRTO = True
run_NLRTO = False
sOpt_add_replicas = 0

# Here the trials_per_run and prod_runs options can be tweaked to 
# get simulations of the appropriate length. (they are split up to fit in the 24h queue on the cluster)

# 2500 * 4 = 10'000 exchange trials (every 100fs) => 1ns of simulation

last_jobID = mixedOpt.do(out_root_dir=out_sopt_dir,
                         in_simSystem=system,
                         in_ene_ana_lib_path=ene_ana_lib, 
                         nmpi_per_replica=nmpi_per_replica,
                         duration_per_job = job_duration,
                         iterations=iterations,
                         learningFactors=learningFactors,
                         individualCorrection=individualCorrection,
                         verbose= True,
                         memory = memory,
                         trials_per_run = 2500, 
                         run_NGRTO = run_NGRTO, 
                         run_NLRTO = run_NLRTO,
                         sOpt_add_replicas = sOpt_add_replicas,
                         optimized_states_dir = optimized_states_dir,
                         lower_bound_dir = lower_bound_dir,
                         intensity_factor = intensity_factor,
                         in_gromosPP_bin_dir=gromosPP_bin,
                         in_gromosXX_bin_dir=gromosXX_bin, 
                         submit = True, 
                         equil_runs = 0,
                         prod_runs = 4, 
                         in_template_imd = template_imd
                      )

