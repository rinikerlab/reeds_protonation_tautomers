import os
import reeds
from pygromos.euler_submissions import FileManager as fM
from pygromos.utils import bash

name = "GSK3b_complex_sharedR"
root_dir = os.getcwd()

input_folder =    root_dir+"/0_input"
in_cnf_file =     input_folder+"/GSK3b_complex_hybrid.cnf"
in_top_file =     input_folder+"/GSK3b_sharedR_complex_ions.top"
in_pert_file =    input_folder+"/GSK3b_sharedR.ptp"

in_disres_file =  None 
in_posres_file = None
in_refpos_file = None

gromosXX_bin = "/cluster/home/cchampion/work/programs/gromosXX_2023/bin/"
gromosPP_bin = "/cluster/home/cchampion/work/programs/gromos++/bin/"
ene_ana_lib =  input_folder +"/ene_ana.md++.lib"

in_template_eds_imd = input_folder+"/template_md.imd"

undersampling_frac_thresh = 0.90
