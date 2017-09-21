
# Select directory with Conquest files
wd = "/home/ucapjsb/Scratch/SmallSurfaceDefects/BulkTests/TMPPs/DZP/DZP_opt_cubic"
# Path to desired Conquest binary
binPath = "/home/ucapjsb/Scratch/bin/Conquest_latest"
# Number of MPI processes (does nothing on thomas. Defined in .sh script)
numProc = 5
# Computing platform
platform = "Thomas"


optAtomPos = True
optCell = False
optMethod = "BFGS"
enTol = 1e-8
maxIter = 200
gradTol = 1e-5

# L-BFGS-B parameters
lbfgsb_factr = 1e5

# Newton CG parameters
coordTol = 1e-3
