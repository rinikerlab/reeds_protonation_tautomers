# reeds_protonation_tautomers

## Description

This directory contains the analysis scripts and data (e.g. to reproduce figures) for the preprint [ADD LINK TO PREPRINT]

Input files to reproduce the RE-EDS simulations shown in this work are given in: `input_files`

The jupyter notebooks to reproduce the figures in the manuscript can be found in: `paper_programs/notebooks`

## Installation

The analysis scripts are all written in Python. A conda environment file is provided with `reeds_environment.yml`. To install the environment, run the following command in the terminal:

```bash
mamba env create -f reeds_environment.yml
```

Additionally, the code relies on a few functions from the ''reeds pipeline'' which can be downloaded from:
```bash
git clone --recurse-submodules https://github.com/rinikerlab/reeds.git
export PYTHONPATH=$PYTHONPATH:/path/to/reeds
```

This will create a conda environment called `reeds_tautomers`. To activate the environment, run:

```bash
conda activate reeds_tautomers
```
