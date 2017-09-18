
# Select directory with Conquest files
wd = "/homes/jbaker/Documents/programming/Conquest/optTests/SZP_tet"
# Path to desired Conquest binary
binPath = "~jbaker/bin/Conquest_latest"
# Number of MPI processes
numProc = 5


optAtomPos = True
optCell = False
optMethod = "BFGS"
enTol = 1e-9
maxIter = 50
gradTol = 1e-4

# L-BFGS-B parameters
lbfgsb_factr = 1e6
