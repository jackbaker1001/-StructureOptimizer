"""
INPUT FILE FOR CONQUEST STRUCTURE OPTIMIZER
Author: Jack Baker
Date: 22/09/17
Description: A file for specifying all of the parameters
             for a structure optimization run. See comments
             above input variable for a description.
"""



# Select directory with Conquest files
wd = "/homes/jbaker/Documents/programming/Conquest/optTests/LDA_tet_DZP_pto"
# Path to desired Conquest binary
binPath = "~jbaker/bin/Conquest_latest"
# Number of MPI processes if running on cluster (monoceros, hydra, petrof..)
numProc = 5
# Computing platform (cluster, Thomas)
platform = "cluster"
# Optimize atomic positions, simulation box or both
optAtomPos = False
optCell = True
sameTime = False
# Choose an optimization method (BFGS, L-BFGS-B, CG, NCG)
optMethod = "BFGS"
# L-BFGS-B convergence condition is enTol
enTol = 1e-8
# CG and BFGS convergence condition is gradTol (forces or stress...)
gradTol = 1e-3
# Newton CG  convergence condition is coordTol
# (relates to atomic tol precison or simulation box tol)
coordTol = 1e-3
# Maximum number of iterations for chosen optMethod
maxIter = 20
