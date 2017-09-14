from src.CQWriter import ConquestWriter
from src.CQReader import ConquestReader
from src.CQRun import ConquestWrapper
from src.objFuncs import *
from input import *
from scipy.optimize import minimize
import numpy as np
import sys
import os

os.system("rm structureOptimizer.out")
sys.stdout = open("structureOptimizer.out", "a")

# Initialization requirements
CQr = ConquestReader(wd)
CQw = ConquestWriter()
CQr.getCoords()
CQr.close(closeCQOut=False)
coordInit = CQr.coordArray
coordInit[:, 0] = coordInit[:, 0]*CQr.rCellX
coordInit[:, 1] = coordInit[:, 1]*CQr.rCellY
coordInit[:, 2] = coordInit[:, 2]*CQr.rCellZ
coordInit = coordInit.flatten()
boxDimsInit = [CQr.rCellX, CQr.rCellY, CQr.rCellZ]

print("\n CONQUEST STRUCTURE OPTIMIZER \n")
print("\n By Jack S. Baker - London Centre for Nanotechnology - 2017 \n")
print("\n Optimize box dimensions: %s  Optimize coordinates: %s \n" % (optCell, optAtomPos))
print("\n Beginning %s optimization with tolerance: %.10f... \n" % (optMethod, energyTol))

if optCell and not optAtomPos:
    opt = minimize(fun=E_boxDims, x0=boxDimsInit, method=optMethod,
                   jac=True, tol=energyTol,
                   options={"maxiter": maxIter, "disp": True, "iprint": 1 })
elif not optCell and optAtomPos:
    opt = minimize(fun=E_atomPos, x0=coordInit, method=optMethod,
                   jac=True, tol=energyTol,
                   options={"maxiter": maxIter, "disp": True, "iprint": 1})
elif optCell and optAtomPos:
    coordInit = coordInit.tolist()
    coordInit.extend(boxDimsInit)
    coordBoxDimsInit = np.array(coordInit, dtype=np.float64)
    opt = minimize(fun=E_atomPosBoxDim, x0=coordBoxDimsInit, method=optMethod,
                   jac=True, tol=energyTol,
                   options={"maxiter": maxIter, "disp": True, "iprint": 1})


print(opt.x)








