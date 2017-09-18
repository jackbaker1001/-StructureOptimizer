from src.CQWriter import ConquestWriter
from src.CQReader import ConquestReader
from src.CQRun import ConquestWrapper
from input import *
import numpy as np
import sys
import os

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
    CQw.writeCoord(dynamics=CQr.dynamics, writeAtomPos=False, latVec=boxDims)
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
    sys.stdout.flush()
    return CQr.E, CQr.stress


def E_atomPos(coords):
    # This function takes the coordinates in a flattened format
    global funcEvals
    funcEvals += 1
    CQr = ConquestReader(wd)
    CQr.getCoords()
    CQw = ConquestWriter()
    simulation = ConquestWrapper(binPath, numProc, wd)
    # put coordinates in correct format for writer
    conditCoord = np.empty((CQr.numAtoms, 3), dtype=np.float64)
    count = 0
    for iatom in range(CQr.numAtoms):
        for ipos in range(3):
            if CQr.dynamics[iatom, ipos] == True:
                conditCoord[iatom, ipos] = coords[count]
                count += 1
    coords = conditCoord
    CQw.writeCoord(funcCall=funcEvals, dynamics=CQr.dynamics,
                   writeBoxDims=False, newCoord=coords,
                   latVec=[CQr.rCellX, CQr.rCellY, CQr.rCellZ])
    CQw.close(closeCQOut=False)
    simulation.runConquest()
    CQr.getTotalEnergy(); CQr.getForces()
    forces = CQr.forces
    rmsForce = np.sqrt(np.mean(forces*forces))
    CQr.close(closeCoords=False)
    fracCoords = coords/np.array([CQr.rCellX, CQr.rCellY, CQr.rCellZ])
    print("\n\n Function Call: %d" % (funcEvals))
    print("Curent forces [Fx, Fy, Fz] (Ha/Bohr):")
    print(CQr.allForces)
    print("RMS force (Ha/Bohr)")
    print("Maximum force component on MOVING atom (Ha/Bohr)")
    print(np.abs(forces).max())
    print("RMS force of MOVING atoms (Ha/Bohr)")
    print(rmsForce)
    print("Total Energy = %.8f Ha" % (CQr.E))
    os.system("cat " + wd + "/Conquest_out >> " + wd + "/CQOutHistory")
    # return flattened gradient information also
    sys.stdout.flush()
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
    CQw.writeCoord(dynamics=CQr.dynamics, newCoord=coords, latVec=boxDims)
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
    sys.stdout.flush()
    return CQr.E, forcesAndStress


