from src.CQWriter import ConquestWriter
from src.CQReader import ConquestReader
from src.CQRun import ConquestWrapper
from input import *
import numpy as np

"""
Author: Jack Baker
Date 13/09/17
Contains: Objective functions to minimize 
"""

funcEvals = 0

def E_boxDims(boxDims):
    CQr = ConquestReader(wd)
    CQw = ConquestWriter()
    simulation = ConquestWrapper(binPath, numProc, wd)
    CQw.writeCoord(writeAtomPos=False, latVec=boxDims)
    CQw.close(closeCQOut=False)
    simulation.runConquest()
    CQr.getTotalEnergy(); CQr.getStress()
    CQr.close(closeCoords=False)
    global funcEvals
    funcEvals += 1
    print("\n\n Function Call: %d" % (funcEvals))
    print("Current Box dims:")
    print(boxDims)
    print("Current stress")
    print(CQr.stress)
    print("Total Energy = %.8f Ha" % (CQr.E))
    return CQr.E, CQr.stress


def E_atomPos(coords):
    # This function takes the coordinates in a flattened format
    CQr = ConquestReader(wd)
    CQr.getCoords()
    CQw = ConquestWriter()
    simulation = ConquestWrapper(binPath, numProc, wd)
    coords = coords.reshape((CQr.numAtoms, 3))
    CQw.writeCoord(writeBoxDims=False, newCoord=coords,
                   latVec=[CQr.rCellX, CQr.rCellY, CQr.rCellZ])
    CQw.close(closeCQOut=False)
    simulation.runConquest()
    CQr.getTotalEnergy(); CQr.getForces()
    forces = -CQr.forces.flatten()
    rmsForce = np.sqrt(np.mean(forces*forces))
    CQr.close(closeCoords=False)
    fracCoords = coords/np.array([CQr.rCellX, CQr.rCellY, CQr.rCellZ])
    global funcEvals
    funcEvals += 1
    print("\n\n Function Call: %d" % (funcEvals))
    print("Current coordinates (fractional):")
    print(fracCoords)
    print("Curent forces [Fx, Fy, Fz] (Ha/Bohr):")
    print(CQr.forces)
    print("RMS force (Ha/Bohr)")
    print(rmsForce)
    print("Total Energy = %.8f Ha" % (CQr.E))
    # return flattened gradient information also
    return CQr.E, forces


def E_atomPosBoxDim(coordsAndBoxDims):
    # This function takes the coordinates in a flattened format
    CQr = ConquestReader(wd)
    CQw = ConquestWriter()
    CQr.getCoords()
    simulation = ConquestWrapper(binPath, numProc, wd)
    coords = coordsAndBoxDims[:-3]
    boxDims = coordsAndBoxDims[-3:]
    coords = coords.reshape((CQr.numAtoms, 3))
    CQw.writeCoord(newCoord=coords, latVec=boxDims)
    CQw.close(closeCQOut=False)
    simulation.runConquest()
    CQr.getTotalEnergy(); CQr.getForces(); CQr.getStress()
    CQr.close(closeCoords=False)
    fracCoords = coords/boxDims
    forces = -CQr.forces.flatten()
    rmsForce = np.sqrt(np.mean(forces*forces))
    global funcEvals
    funcEvals += 1
    print("\n\n Function Call: %d" % (funcEvals))
    print("Current Box dims (Bohr) and coordinates (fractional):")
    print(boxDims)
    print(fracCoords)
    print("Current stress components [Sxx, Syy, Szz] (Ha)):")
    print(CQr.stress)
    print("Current forces [Fx, Fy, Fz] (Ha/Bohr):")
    print(CQr.forces)
    print("RMS force (Ha/Bohr)")
    print(rmsForce)
    print("Total Energy = %.8f Ha" % (CQr.E))
    forcesAndStress = forces
    forcesAndStress = forcesAndStress.tolist()
    forcesAndStress.extend(CQr.stress.tolist())
    forcesAndStress = np.array(forcesAndStress)
    # return flattened gradient information also
    return CQr.E, forcesAndStress


