from src.CQWriter import ConquestWriter
from src.CQReader import ConquestReader
from src.objFuncs import *
from input import *
from scipy.optimize import minimize
import numpy as np
import sys
import os

os.chdir(wd)
os.system("rm structureOptimizer.out")
sys.stdout = open("structureOptimizer.out", "a")

# Initialization requirements
CQr = ConquestReader(wd)
CQr.getCoords()
CQw = ConquestWriter()
CQr.close(closeCQOut=False)
coordInit = CQr.coordArray
boxDimsInit = np.array([CQr.rCellX, CQr.rCellY, CQr.rCellZ])
coord = coordInit*boxDimsInit
coordInit = []
# Initial selective dynamics
for iatom in range(CQr.numAtoms):
    for ipos in range(3):
        if CQr.dynamics[iatom, ipos] == True:
            coordInit.append(coord[iatom, ipos])
coordInit = np.array(coordInit, dtype=np.float64)
boxDimsInit = [CQr.rCellX, CQr.rCellY, CQr.rCellZ]

print("\n CONQUEST STRUCTURE OPTIMIZER \n")
print("\n By Jack S. Baker - London Centre for Nanotechnology - 2017 \n")
print("\n Optimize box dimensions: %s  Optimize coordinates: %s \n" % (optCell, optAtomPos))
print("\n Beginning %s optimization with tolerance: %.10f... \n" % (optMethod, enTol))
sys.stdout.flush()

# Selecting Objective function to minimize and initial conditions
if optCell and not optAtomPos:
    objFunc = E_boxDims
    initCondit = boxDimsInit
elif not optCell and optAtomPos:
    objFunc = E_atomPos
    initCondit = coordInit
elif optCell and optAtomPos:
    coordInit = coordInit.tolist()
    coordInit.extend(boxDimsInit)
    coordBoxDimsInit = np.array(coordInit, dtype=np.float64)
    initCondit = coordBoxDimsInit
    objFunc = E_atomPosBoxDim

# Select method options
if optMethod == "L-BFGS-B":
    methodOptions = {"factr": lbfgsb_factr, "ftol": enTol, "gtol": gradTol,
                     "disp": True, "maxiter": maxIter}
elif optMethod == "BFGS" or optMethod == "CG":
    methodOptions = {"gtol": gradTol, "disp": True, "maxiter": maxIter}
elif optMethod == "Newton-CG":
    methodOptions = {"xtol": coordTol, "disp": True, "maxiter": maxIter}
elif optMethod == "debug": 
    pass

# Enter scipy wrapper for minimizers
if optMethod != "debug":
    opt = minimize(fun = objFunc, x0=initCondit, jac=True,
                   method=optMethod, options=methodOptions)
    print("minimization terminated")

